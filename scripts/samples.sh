#!/bin/bash
#
# run samples tests
#
SAMPLESCMD="task samples"
if [ -z "${TEST_ARCHIVIST}" ]
then
    echo "TEST_ARCHIVIST is undefined"
    exit 1
fi
if [ -z "${TEST_AUTHTOKEN}" ]
then
    echo "TEST_AUTHTOKEN is undefined"
    exit 1
fi
if [ ! -s "${TEST_AUTHTOKEN}" ]
then
    echo "${TEST_AUTHTOKEN} does not exist"
    exit 1
fi

if [ -z "${TEST_SELECTOR}" -o "$TEST_SELECTOR" = 'help' ]
then
    echo "Available functional tests are:"
    echo ""
    echo "    TEST_SELECTOR=door_entry ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=estate_info ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=signed_records ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_initialise ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_analyze ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_charger ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_jitsuinator ${SAMPLESCMD}"
    echo "    TEST_SELECTOR=synsation_wanderer ${SAMPLESCMD}"
    echo ""
    echo "To run more than one test use a comma-separated list:"
    echo ""
    echo "    TEST_SELECTOR=door_entry,estate_info ${SAMPLESCMD}"
    echo ""
    echo "To run all tests:"
    echo ""
    echo "    TEST_SELECTOR=all ${SAMPLESCMD}"
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

TEST_NO_DOOR_ENTRY=${TEST_NO}
TEST_NO_ESTATE_INFO=${TEST_NO}
TEST_NO_SIGNED_RECORDS=${TEST_NO}
TEST_NO_SYNSATION_INITIALISE=${TEST_NO}
TEST_NO_SYNSATION_ANALYZE=${TEST_NO}
TEST_NO_SYNSATION_CHARGER=${TEST_NO}
TEST_NO_SYNSATION_JITSUINATOR=${TEST_NO}
TEST_NO_SYNSATION_WANDERER=${TEST_NO}

IFS=',' read -r -a SELECTION_LIST <<< "$TEST_SELECTOR"
for selection in "${SELECTION_LIST[@]}"
do
    sel=$( echo $selection | tr '[:lower:]' '[:upper:]')
    eval "TEST_NO_$sel="
done

cd samples

export PYTHONWARNINGS="ignore:Unverified HTTPS request"
ARGS="-u $TEST_ARCHIVIST -t ../$TEST_AUTHTOKEN ${TEST_VERBOSE}"

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

DOOR_ENTRY="${TEST_NO_DOOR_ENTRY} python3 -m door_entry ${ARGS} ${NAMESPACE}"
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

# namespacing not required here
ESTATE_INFO="${TEST_NO_ESTATE_INFO} python3 -m estate_info ${ARGS}"
${ESTATE_INFO} --quick-count
${ESTATE_INFO} --double-check

SIGNED_RECORDS="${TEST_NO_SIGNED_RECORDS} python3 -m signed_records ${ARGS} ${NAMESPACE}"
${SIGNED_RECORDS} --create 'samples'
${SIGNED_RECORDS} --sign-message 'signature' 'samples'
${SIGNED_RECORDS} --bad-sign-message 'signature' 'samples'
${SIGNED_RECORDS} --check 'samples'

SYNSATION_INITIALISE="${TEST_NO_SYNSATION_INITIALISE} python3 -m synsation initialise ${ARGS} ${NAMESPACE}"
${SYNSATION_INITIALISE} --num-assets 100 --wait 1 --await-confirmation

SYNSATION_ANALYZE="${TEST_NO_SYNSATION_ANALYZE} python3 -m synsation analyze ${ARGS} ${NAMESPACE}"
${SYNSATION_ANALYZE}

SYNSATION_CHARGER="${TEST_NO_SYNSATION_CHARGER} python3 -m synsation charger ${ARGS} ${NAMESPACE}"
${SYNSATION_CHARGER} -s 20190909 -S 20190923 -f 9876

SYNSATION_JITSUINATOR="${TEST_NO_SYNSATION_JITSUINATOR} python3 -m synsation jitsuinator ${ARGS} ${NAMESPACE}"
${SYNSATION_JITSUINATOR} -n tcl.ccj.001 --wait 1.0

SYNSATION_WANDERER="${TEST_NO_SYNSATION_WANDERER} python3 -m synsation wanderer ${ARGS} ${NAMESPACE}"
${SYNSATION_WANDERER}
