# datatrails-samples

Sample python code that uses the datatrails python SDK to manage particular types of assets
such as 'doors', 'cards', 'containers' etc.

Only supplied as examples of python code that accesses the datatrails archivist.

No tests - released 'AS-IS'

# Installing the samples code

Python 3.9 and later versions are supported.

Use the standard python pip utility:

```bash
python3 -m pip install --user datatrails-samples
```

and this will create 7 entry points:

      - archivist_samples_document
      - archivist_samples_door_entry
      - archivist_samples_estate_info
      - archivist_samples_signed_records
      - archivist_samples_synsation
      - archivist_samples_software_bill_of_materials
      - archivist_samples_wipp


## Pre-requisites

Add a token to the file credentials/.auth_token and set some environment vars to
specify the archivist endpoint:

```bash
export TEST_ARCHIVIST="https://app.datatrails.ai"
export TEST_AUTHTOKEN_FILENAME=credentials/.auth_token
export TEST_NAMESPACE="unique label"
export TEST_PARTNER_ID="acmecorp"
export TEST_VERBOSE=-v
```

If TEST_VERBOSE is "-v" debugging output will appear when running the examples. Otherwise leave blank or undefined.

Windows using Powershell - at the command prompt set values for environment variables:

```bash
$Env:TEST_ARCHIVIST="https://app.datatrails.ai"
$Env:TEST_AUTHTOKEN_FILENAME = '<path of token location>'
$Env:TEST_NAMESPACE = Get-Date -UFormat %s
$Env:TEST_PARTNER_ID = 'acmecorp'
$Env:TEST_VERBOSE = '-v'
```

TEST_NAMESPACE is set to the date and time value in Unix format, thus providing a unique id upon execution.

## TEST_NAMESPACE

If TEST_NAMESPACE is blank or unspecified, any assets or events will be visible to other users running the same examples
on the same URL.

Each example creates assets,events that are not visible to other examples.
For example the door_entry assets,events etc are not visible to the synsation example.

***Note: Assets are only created if they do not already exist according to namespace.  If one wants to execute a sample multiple 
times, feel free to set TEST_NAMESPACE to a different unique id.***

Due to restrictions attachments are always uploaded during every example execution.

Events are created every execution of an example - currently no check is done if the event already exists.

## EXAMPLES

All examples use a common set of arguments:

```bash
export AUTH="-u $TEST_ARCHIVIST -t $TEST_AUTHTOKEN_FILENAME $TEST_VERBOSE"
export ARGS="$AUTH --namespace $TEST_NAMESPACE --partner_id=$TEST_PARTNER_ID"
```

### Door Entry Control

Some commands to simply create and manage doors and cards:

```bash
archivist_samples_door_entry $ARGS --create
archivist_samples_door_entry $ARGS --list all
archivist_samples_door_entry $ARGS --list doors
archivist_samples_door_entry $ARGS --list cards
archivist_samples_door_entry $ARGS --list 'Courts of Justice front door'
archivist_samples_door_entry $ARGS --list 'access_card_1'
```

Execute opening doors with a card:

```bash
archivist_samples_door_entry $ARGS --open "Courts of Justice front door,access_card_1"
archivist_samples_door_entry $ARGS --open "Courts of Justice front door,access_card_3"
archivist_samples_door_entry $ARGS --open "Courts of Justice front door,access_card_4"
archivist_samples_door_entry $ARGS --open "Courts of Justice front door,access_card_0"
archivist_samples_door_entry $ARGS --open "Courts of Justice front door,access_card_2"
archivist_samples_door_entry $ARGS --open "Bastille front door,access_card_2"
archivist_samples_door_entry $ARGS --open "City Hall front door,access_card_2"
archivist_samples_door_entry $ARGS --open "Gare du Nord apartments side door,access_card_2"
```

### Manage assets and events and check for any inconsistencies

NB no namespace required ...

```bash
archivist_samples_estate_info $AUTH --quick-count
archivist_samples_estate_info $AUTH --double-check
```

### Signed Records

```bash
archivist_samples_signed_records $ARGS --create 'samples'
archivist_samples_signed_records $ARGS --sign-message 'signature' 'samples'
archivist_samples_signed_records $ARGS --bad-sign-message 'signature' 'samples'
archivist_samples_signed_records $ARGS --check 'samples'
```

### Synsation

```bash
archivist_samples_synsation initialise  $ARGS --num-assets 100 --wait 1 --await-confirmation
archivist_samples_synsation charger     $ARGS --start-date 20190909 --stop-date 20191009 --fast-forward 9876
archivist_samples_synsation simulator   $ARGS --asset-name tcl.ccj.001 --wait 1.0
archivist_samples_synsation wanderer    $ARGS
archivist_samples_synsation analyze     $ARGS 
```

### Software Bill of Materials

```bash
archivist_samples_software_bill_of_materials $ARGS
```

### WIPP

```bash
archivist_samples_wipp $ARGS
```
