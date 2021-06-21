# archivist-samples

Sample python code that uses the archivist python SDK to manage particular types of assets
such as 'doors', 'cards', 'containers' etc.

# Running the samples code

Clone this repo and cd into the root directory of the repo.

## Pre-requisites

Python 3.6 and later versions are supported.

A bash shell and the ability to install python code using requirements.txt and pip. Execute
the following command in your virtual environment or user login:

```bash
python3 -m pip install --user -r requirements.txt
```

Add a token to the file credentials/.auth_token and set some environment vars to
specify the archivist endpoint:

```bash
export ARCHIVIST="https://rkvst.poc.jitsuin.io"
export AUTHTOKEN=credentials/.auth_token
export NAMESPACE="unique label"
export VERBOSE=-v
```

If VERBOSE is "-v" debugging output will appear when running the tests. Otherwise leave blank or undefined.

## NAMESPACE

If NAMESPACE is blank or unspecified then each execution of './scripts/samples.sh' will not be
independent. Any assets events, locations will be visible to other users running the same tests
on the same URL.

Each example test creates assets,events,locations that are not visible to other example tests.
For example the door_entry assets,events etc are not visible to the synsation example tests.

Assets and locations are only created if they do not already exist according to namespace.

Due to restrictions attachments are always uploaded during every test execution.

Events are created every execution of a test - currently no check is done if the event already exists.

## TESTS

Move to correct subdirectory:

```bash
cd samples
```

### Door Entry Control

Some commands to simply create and manage doors and cards:

python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --create
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list all
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list doors
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list cards
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list 'Courts of Justice front door'
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list 'access_card_1'

Execute opening doors with a card:

python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_1"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_3"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_4"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_0"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_2"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Bastille front door,access_card_2"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "City Hall front door,access_card_2"
python3 -m door_entry -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Gare du Nord apartments side door,access_card_2"

### Manage assets and events and check for any inconsistencies

python3 -m estate_info -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --quick-count
python3 -m estate_info -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --double-check

### Signed Records

python3 -m signed_records -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --create 'samples'
python3 -m signed_records -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --sign-message 'signature' 'samples'
python3 -m signed_records -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --bad-sign-message 'signature' 'samples'
python3 -m signed_records -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --check 'samples'

### Synsation

python3 -m synsation initialise  -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE --num-assets 100 --wait 1 --await-confirmation
python3 -m synsation analyze     -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE
python3 -m synsation charger     -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE -s 20190909 -S 20190923 -f 9876
python3 -m synsation jitsuinator -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE -n tcl.ccj.001 --wait 1.0
python3 -m synsation wanderer    -u $ARCHIVIST -t ../$AUTHTOKEN $VERBOSE --namespace $NAMESPACE
