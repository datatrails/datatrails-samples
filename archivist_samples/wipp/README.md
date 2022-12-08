# Nuclear Waste Handling Lifecycle Sample

Tracking the Nuclear Waste Management lifecycle is an important aspect to ensure that all safety protocols and procedures have been successfully executed.  Fragmented communication and manual checks can lead to honest mistakes and redundancy.  Digitizing the lifecycle and exposing data to the right parties at the right time can decrease honest mistakes and increase effective communication.  

RKVST Continuous Assurance Hub offers a solution to fragmented communication and manual checks. Parties have near real-time access to data increasing seamless and effective communication in addition stakeholders can control the sharing of data ensuring one can view information that is relevant.  Policies, procedures and images can be included/attached thus reducing multiple checks and providing persons with the most recent documentation.
 
This sample uses publicly-available information about WIPP (Waste Isolation Pilot Plant) and how to quickly get started with integrating Nuclear Waste Management lifecycle with RKVST Continuous Assurance Hub.


## Pre-requisites

* Python 3.7 and later versions are supported.

* Install the [RKVST samples Python package](https://pypi.org/project/jitsuin-archivist-samples/ "PyPi package page")

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [RKVST documentation](https://docs.rkvst.com/docs/rkvst-basics/getting-access-tokens-using-app-registrations/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The sample registers nuclear waste assets and uploads images, policies and procedures relevant to certain events.  The events simulate Nuclear Waste Disposal lifecycle from waste characterization through emplacement. Thus providing a "Continuous Assurance" example of Nuclear Waste Managment.

To run it: 

```bash
archivist_samples_wipp [-v]
```

## Using the WIPP class

The WIPP class creates two Assets: Drum and Cask. The Drum is an item that contains nuclear waste which is loaded into the Cask for transportation.

This Python class makes it easy to create the above assets and related events in RKVST.  Providing an assurance hub with trusted data.

### Creating a Drum and Cask

To create a brand new WIPP Asset and begin tracking and sharing Nuclear Waste lifecycle, use `Wipp.create()`:

```python
    # Binaries such as images need to be uploaded to RKVST first
    def upload_attachment(arch, path, name):
        with open(f"wipp_files/{path}", "rb") as fd:
            blob = arch.attachments.upload(fd)
            attachment = {
                "arc_display_name": name,
                "arc_attachment_identity": blob["identity"],
                "arc_hash_value": blob["hash"]["value"],
                "arc_hash_alg": blob["hash"]["alg"],
            }
            return attachment

    # Instantiate WIPP object and create an RKVST record to begin
    # tracing and publishing its lifecycle
    # Drum Asset
    drum = Wipp(arch)
    serial_num = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )
    drumname = "Drum-" + serial_num

    drum.create(
        drumname,
        "Standard non-POC 55 gallon drum",
        serial_num,
        attachments=[upload_attachment(arch, "55gallon.jpg", "arc_primary_image")],
        custom_attrs={
            "wipp_capacity": "55",
            "wipp_package_id": serial_num,
        },
    )

    # Cask Asset
    cask = Wipp(arch)
    serial_num = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )
    caskname = "Cask-" + serial_num

    cask.caskcreate(
        caskname,
        "NRC certified type-B road shipping container, capacity 3 x 55-gallon drum",
        serial_num,
        attachments=[upload_attachment(arch, "rh72b.png", "arc_primary_image")],
        custom_attrs={
            "wipp_capacity": "3",
        },
    )
```


### Loading data for an existing Wipp object

If you know the RKVST Asset Identity you can load data directly
to the Drum and/or Cask Assset using `Wipp.read()`:

```python
# Assume Archivist connection already initialized in `arch`
Drum = Wipp(arch)
drum.read("assets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
```

If you do not know the RKVST Asset Identity then you can load data based on any unique set of attributes using `Wipp.read_by_signature()`:

```python
# Assume Archivist connection already initialized in `arch`
Drum = Wipp(arch)
drum.read_by_signature({"wipp_package_id": "gklh588i8wd9"})
```


### Loading Characterization

When adding characterization, update the Drum Asset in RKVST with
`Wipp.characterization()`:

```python
# Assume Archivist connection already initialized in `arch`
drum = Wipp(arch)

drum.characterize(
        {
            "description": "Waste coding characterization: A2 Fraction 2.10E+05",
            "weight": "790300",
            "a2fraction_characterized": "2.10E+05",
            "activity_characterized": "1.69E+02",
            "total_characterized": "2.12E+02",
        },
        attachments=[
            upload_attachment(
                arch, "DOE-WIPP-02-3122_Rev_9_FINAL.pdf", "Reference WAC"
            ),
            upload_attachment(arch, "characterization.pdf", "Characterization report"),
        ],
    )
```


### Other functions

* `tomography()`: Characterization has been excuted however not confirmed. Use this to signal confirmation of characterization to stakeholders who need evidence prior to loading drum into cask. 

* `loading()`: Characterization has been executed and confirmed. Use this to signal cask is being loaded with drum to stakeholders who need evidence prior to pre-shipment inspection.

* `preshipping()`: Before departure the cask (and it's contents) have to pass pre-shipping inspection.  Use this to signal that pre-shipping inpsection has been executed to stakeholders who need evidence prior to cask departure.

* `departure()`: Cask has passed pre-shipping inspection and is ready to depart.  Use this to signal that the Cask is departing and route instructions have been attached to stackholders who need evidence prior to transport.

* `waypoint()`: The Cask (and contents) are in transit.  Use this to signal any intermediate points on a route to stakeholders who need evidence of stops or change of course.

* `arrival()`: Use this to signal contents have arrived to stakeholders who need evidence that materials appeared at expected destination.

* `unloading()`: Use this to signal unloading of Cask (and contents) to stakeholders who need evidence waste has been safely unpacked.

* `emplacement()`: Use this to signal the placement of contents to stakeholders who need evidence that waste has been properly stored.


## Access policies

In order to control data sharing one can restrict access allowing certain parties view to relevant data, create an Access Policy like this (substituting for real Subject IDs of your value chain partners):

```json
    {
      "identity": "access_policies/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "display_name": "Drum-gklh588i8wd9",
      "filters": [
        {
          "or": [ "attributes.arc_display_type=55 gallon drum" ]
        }
      ],
      "access_permissions": [
        {
          "subjects": [ "subjects/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" ],
          "behaviours": [ "RecordEvidence" ],
          "include_attributes": [],
          "user_attributes": [],
          "asset_attributes_read": [
            "arc_display_type",
            "arc_display_name",
            "arc_description",
            "arc_attachments",
            "wipp_a2fraction_characterized",
            "wipp_a2fraction_confirmed",
            "wipp_activity_characterized",
            "wipp_activity_confirmed",
            "wipp_capacity",
            "wipp_total_characterized",
            "wipp_total_confirmed"
          ],
          "asset_attributes_write": [],
          "event_arc_display_type_read": [
            "WO Characterize",
            "WO Confirmation",
            "WO Loading"
          ],
          "event_arc_display_type_write": []
        }
      ],
      "tenant": "tenant/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "description": "Publish characterization and confirmation to stakeholders"
    }

```
