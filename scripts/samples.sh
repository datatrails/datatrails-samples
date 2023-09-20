#!/bin/bash
#
# run samples tests
#
TASK=${1:-samples}
SAMPLESCMD="task ${TASK}"
if [ -z "${TEST_ARCHIVIST}" ]
then
    echo "TEST_ARCHIVIST is undefined"
    exit 1
fi
if [ -z "${TEST_AUTHTOKEN_FILENAME}" ]
then
    echo "TEST_AUTHTOKEN_FILENAME is undefined"
    exit 1
fi
if [ ! -s "${TEST_AUTHTOKEN_FILENAME}" ]
then
    echo "${TEST_AUTHTOKEN_FILENAME} does not exist"
    exit 1
fi

if [ -z "${TEST_SELECTOR}" -o "$TEST_SELECTOR" = 'help' ]
then
    echo "Available functional tests are:"
    echo ""
    echo "    TEST_SELECTOR=c2pa ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=door_entry ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=estate_info ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=signed_records ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_initialise ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_charger ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_simulator ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_wanderer ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_analyze ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=sbom ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=wipp ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=document ${SAMPLESCMD}"
    echo ""
    echo "To run more than one test use a comma-separated list:"
    echo ""
    echo "    TEST_SELECTOR=door_entry,estate_info ${SAMPLESCMD}"
    echo ""
    echo "To run all tests:"
    echo ""
    echo "    TEST_SELECTOR=all ${SAMPLESCMD}"
    echo ""
    echo "Additionally:"
    echo ""
    echo "    TEST_NAMESPACE=$TEST_NAMESPACE"
    echo "    TEST_VERBOSE=$TEST_VERBOSE"
    echo ""
    exit 0
fi

# work out selection criteria - the colon (:) is the bash equivalent of a 
# noop and effectively does **not** run the selected test when set.
#
TEST_NO=':'
if [ "$TEST_SELECTOR" = all ]
then
    TEST_NO=''
fi

TEST_NO_C2PA=${TEST_NO}
TEST_NO_DOOR_ENTRY=${TEST_NO}
TEST_NO_ESTATE_INFO=${TEST_NO}
TEST_NO_SIGNED_RECORDS=${TEST_NO}
TEST_NO_SYNSATION_INITIALISE=${TEST_NO}
TEST_NO_SYNSATION_ANALYZE=${TEST_NO}
TEST_NO_SYNSATION_CHARGER=${TEST_NO}
TEST_NO_SYNSATION_SIMULATOR=${TEST_NO}
TEST_NO_SYNSATION_WANDERER=${TEST_NO}
TEST_NO_SBOM=${TEST_NO}
TEST_NO_WIPP=${TEST_NO}
TEST_NO_DOCUMENT=${TEST_NO}

IFS=',' read -r -a SELECTION_LIST <<< "$TEST_SELECTOR"
for selection in "${SELECTION_LIST[@]}"
do
    sel=$( echo $selection | tr '[:lower:]' '[:upper:]')
    eval "TEST_NO_$sel="
done

export PYTHONWARNINGS="ignore:Unverified HTTPS request"
ARGS="-u $TEST_ARCHIVIST -t $TEST_AUTHTOKEN_FILENAME $TEST_VERBOSE $TEST_PROOF_MECHANISM"

# namespacing ensures that each run  of the tests is independent.
if [ -n "$TEST_NAMESPACE" ]
then
    if [ "$TEST_NAMESPACE" = "date" ]
    then
        NS=$(date +%s)
    else
        NS=$( echo ${TEST_NAMESPACE} | tr -s '[:blank:]' | tr '[:blank:]' '_' )
    fi
    echo "NAMESPACE is ${NS}"
    NAMESPACE="--namespace ${NS}"
else
    echo "No NAMESPACE specified - may share assets etc with someone else on same URL"
fi

# emit command if executing tests against the docker image or the installed wheel
command() {
    if [ "${TASK}" == "samples" ]
    then
        echo "python3 -m archivist_samples.$1"
    else
        echo "archivist_samples_$1"
    fi
}

# archivist_samples_c2pa
C2PA="${TEST_NO_C2PA} $(command c2pa) ${ARGS} ${NAMESPACE}"
${C2PA}

# archivist_samples_door_entry
DOOR_ENTRY="${TEST_NO_DOOR_ENTRY} $(command door_entry) ${ARGS} ${NAMESPACE}"
${DOOR_ENTRY} --create
${DOOR_ENTRY} --list all
${DOOR_ENTRY} --list doors
${DOOR_ENTRY} --list cards
${DOOR_ENTRY} --list 'Courts of Justice front door'
${DOOR_ENTRY} --list 'access_card_1'

OPEN="${DOOR_ENTRY} --open"
${OPEN} "Courts of Justice front door,access_card_1"
${OPEN} "Courts of Justice front door,access_card_3"
${OPEN} "Courts of Justice front door,access_card_4"
${OPEN} "Courts of Justice front door,access_card_0"
${OPEN} "Courts of Justice front door,access_card_2"
${OPEN} "Bastille front door,access_card_2"
${OPEN} "City Hall front door,access_card_2"
${OPEN} "Gare du Nord apartments side door,access_card_2"

# archivist_samples_estate_info
ESTATE_INFO="${TEST_NO_ESTATE_INFO} $(command estate_info) ${ARGS}"
${ESTATE_INFO} --quick-count
${ESTATE_INFO} --double-check

# archivist_samples_signed_records
SIGNED_RECORDS="${TEST_NO_SIGNED_RECORDS} $(command signed_records) ${ARGS} ${NAMESPACE}"
${SIGNED_RECORDS} --create 'samples'
${SIGNED_RECORDS} --sign-message 'signature' 'samples'
${SIGNED_RECORDS} --bad-sign-message 'signature' 'samples'
${SIGNED_RECORDS} --check 'samples'

# archivist_samples_synsation
SYNSATION=$(command synsation)
SYNSATION_INITIALISE="${TEST_NO_SYNSATION_INITIALISE} ${SYNSATION} initialise ${ARGS} ${NAMESPACE}"
${SYNSATION_INITIALISE} --num-assets 100 --wait 1 --await-confirmation

SYNSATION_CHARGER="${TEST_NO_SYNSATION_CHARGER} ${SYNSATION} charger ${ARGS} ${NAMESPACE}"
${SYNSATION_CHARGER} --start-date 20190909 --stop-date 20190923 --fast-forward 9876

SYNSATION_SIMULATOR="${TEST_NO_SYNSATION_SIMULATOR} ${SYNSATION} simulator ${ARGS} ${NAMESPACE}"
${SYNSATION_SIMULATOR} --asset-name tcl.ccj.001 --wait 1.0

SYNSATION_WANDERER="${TEST_NO_SYNSATION_WANDERER} ${SYNSATION} wanderer ${ARGS} ${NAMESPACE}"
${SYNSATION_WANDERER}

SYNSATION_ANALYZE="${TEST_NO_SYNSATION_ANALYZE} ${SYNSATION} analyze ${ARGS} ${NAMESPACE}"
${SYNSATION_ANALYZE}

# archivist_samples_software_bill_of_materials
SBOM="${TEST_NO_SBOM} $(command software_bill_of_materials) ${ARGS} ${NAMESPACE}"
${SBOM}

# archivist_samples_wipp
WIPP="${TEST_NO_WIPP} $(command wipp) ${ARGS} ${NAMESPACE}"
${WIPP}

# archivist_samples_document
DOCUMENT="${TEST_NO_DOCUMENT} $(command document) ${ARGS} ${NAMESPACE}"
${DOCUMENT}

