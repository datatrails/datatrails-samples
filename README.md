# archivist-samples

Sample python code that uses the archivist python SDK to manage particular types of assets
such as 'doors', 'cards', 'containers' etc.

# Installing the samples code

Python 3.6 and later versions are supported.

Use the standard python pip utility:

```bash
python3 -m pip install --user jitsuin-archivist-samples
```

and this will create 6 entry points:

      - archivist_samples_door_entry
      - archivist_samples_estate_info
      - archivist_samples_signed_records
      - archivist_samples_synsation
      - archivist_samples_sbom
      - archivist_samples_wipp


## Pre-requisites

Add a token to the file credentials/.auth_token and set some environment vars to
specify the archivist endpoint:

```bash
export ARCHIVIST="https://rkvst.poc.jitsuin.io"
export AUTHTOKEN_FILENAME=credentials/.auth_token
export NAMESPACE="unique label"
export VERBOSE=-v
export PROOF_MECHANISM="--proof-mechanism=SIMPLE_HASH"
```

If VERBOSE is "-v" debugging output will appear when running the examples. Otherwise leave blank or undefined.

PROOF_MECHANISM should be "KHIPU" or "SIMPLE_HASH". If unspecified the default is "SIMPLE_HASH"

## NAMESPACE

If NAMESPACE is blank or unspecified, any assets events, locations will be visible to other users running the same examples
on the same URL.

Each example creates assets,events,locations that are not visible to other examples.
For example the door_entry assets,events etc are not visible to the synsation example.

Assets and locations are only created if they do not already exist according to namespace.

Due to restrictions attachments are always uploaded during every example execution.

Events are created every execution of an example - currently no check is done if the event already exists.

## EXAMPLES

All examples use a common set of arguments:

```bash
export AUTH="-u $ARCHIVIST -t $AUTHTOKEN_FILENAME $VERBOSE $PROOF_MECHANISM"
export ARGS="$AUTH --namespace $NAMESPACE"
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
archivist_samples_synsation charger     $ARGS -s 20190909 -S 20200909 -f 9876
archivist_samples_synsation jitsuinator $ARGS -n tcl.ccj.001 --wait 1.0
archivist_samples_synsation wanderer    $ARGS
archivist_samples_synsation analyze     $ARGS 
```

### Software Bill of Materials

```bash
archivist_samples_sbom $ARGS
```

### WIPP

```bash
archivist_samples_wipp $ARGS
```
