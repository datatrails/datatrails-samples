# archivist-samples

Sample python code that uses the archivist python SDK to manage particular types of assets
such as 'doors', 'cards', 'containers' etc.

# Installing the samples code

Python 3.6 and later versions are supported.

Use the standard python pip utility:

```bash
python3 -m pip install --user jitsuin-archivist-samples
```

and this will create 4 entry points:

      - archivist_samples_door_entry
      - archivist_samples_estate_info
      - archivist_samples_signed_records
      - archivist_samples_synsation


## Pre-requisites

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

### Door Entry Control

Some commands to simply create and manage doors and cards:

archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --create
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list all
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list doors
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list cards
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list 'Courts of Justice front door'
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --list 'access_card_1'

Execute opening doors with a card:

archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_1"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_3"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_4"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_0"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Courts of Justice front door,access_card_2"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Bastille front door,access_card_2"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "City Hall front door,access_card_2"
archivist_samples_door_entry -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --open "Gare du Nord apartments side door,access_card_2"

### Manage assets and events and check for any inconsistencies

archivist_samples_estate_info -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --quick-count
archivist_samples_estate_info -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --double-check

### Signed Records

archivist_samples_signed_records -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --create 'samples'
archivist_samples_signed_records -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --sign-message 'signature' 'samples'
archivist_samples_signed_records -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --bad-sign-message 'signature' 'samples'
archivist_samples_signed_records -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --check 'samples'

### Synsation

archivist_samples_synsation initialise  -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE --num-assets 100 --wait 1 --await-confirmation
archivist_samples_synsation analyze     -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE
archivist_samples_synsation charger     -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE -s 20190909 -S 20190923 -f 9876
archivist_samples_synsation jitsuinator -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE -n tcl.ccj.001 --wait 1.0
archivist_samples_synsation wanderer    -u $ARCHIVIST -t $AUTHTOKEN $VERBOSE --namespace $NAMESPACE
