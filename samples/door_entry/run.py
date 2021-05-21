#   Copyright 2020 Jitsuin, inc
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring


from sys import exit as sys_exit
import uuid

from archivist import about
from archivist.errors import ArchivistNotFoundError
from archivist.logger import LOGGER

from testing.namespace import (
    assets_create,
    assets_count,
    assets_list,
    assets_read_by_signature,
    assets_wait_for_confirmed,
    events_create,
    locations_create_if_not_exists,
)

DOOR_TERMINAL = "Door access terminal"
DOOR_CARD = "Door entry card"

BEHAVIOURS = [
    "Attachments",
    "Firmware",
    "LocationUpdate",
    "Maintenance",
    "RecordEvidence",
]

IMAGEDIR = "door_entry/images"


# Door asset
############


def doors_create(
    arch,
    ws_id,
    displayname,
    serial,
    description,
    location,
    attachments,
):

    attrs = {
        "arc_attachments": [
            {
                "arc_display_name": "arc_primary_image",
                "arc_attachment_identity": attachment["identity"],
                "arc_hash_value": attachment["hash"]["value"],
                "arc_hash_alg": attachment["hash"]["alg"],
            }
            for attachment in attachments
        ],
        "arc_firmware_version": "1.0",
        "arc_serial_number": serial,
        "arc_display_name": displayname,
        "arc_description": description,
        "arc_home_location_identity": location["identity"],
        "arc_display_type": DOOR_TERMINAL,
        "wavestone_asset_id": ws_id,
    }
    return doors_create_if_not_exists(
        arch,
        BEHAVIOURS,
        attrs,
        confirm=False,  # confirmed elsewhere
    )


def doors_create_if_not_exists(arch, behaviours, attrs, *, confirm=None):
    door = None
    try:
        door = assets_read_by_signature(
            arch,
            {
                "arc_display_name": attrs["arc_display_name"],
                "arc_display_type": DOOR_TERMINAL,
            },
        )
    except ArchivistNotFoundError:
        door = assets_create(arch, behaviours, attrs, confirm=confirm)

    return door


def doors_count(arch):
    return assets_count(arch, attrs={"arc_display_type": DOOR_TERMINAL})


def doors_list(arch):
    return assets_list(arch, attrs={"arc_display_type": DOOR_TERMINAL})


def doors_wait_for_confirmed(arch):
    LOGGER.info("Wait for doors creation to confirm")
    assets_wait_for_confirmed(
        arch,
        attrs={
            "arc_display_type": DOOR_TERMINAL,
        },
    )


def doors_read_by_name(arch, name):
    """get door by display name"""
    return assets_read_by_signature(
        arch,
        attrs={
            "arc_display_name": name,
            "arc_display_type": DOOR_TERMINAL,
        },
    )


# Card asset
############


def cards_create(arch, idx):
    return cards_create_if_not_exists(
        arch,
        BEHAVIOURS,
        {
            "arc_serial_number": f"sc-x5-{idx}",
            "arc_display_name": f"access_card_{idx}",
            "arc_description": f"Electronic door access card #{idx}",
            "arc_display_type": DOOR_CARD,
        },
        confirm=False,  # confirmed elsewhere
    )


def cards_create_if_not_exists(arch, behaviours, attrs, *, confirm=None):
    card = None
    try:
        card = assets_read_by_signature(
            arch,
            {
                "arc_display_name": attrs["arc_display_name"],
                "arc_display_type": DOOR_CARD,
            },
        )
    except ArchivistNotFoundError:
        card = assets_create(arch, behaviours, attrs, confirm=confirm)

    return card


def cards_count(arch):
    return assets_count(arch, attrs={"arc_display_type": DOOR_CARD})


def cards_list(arch):
    return assets_list(arch, attrs={"arc_display_type": DOOR_CARD})


def cards_wait_for_confirmed(arch):
    LOGGER.info("Wait for cards creation to confirm")
    assets_wait_for_confirmed(
        arch,
        attrs={
            "arc_display_type": DOOR_CARD,
        },
    )


def cards_read_by_name(arch, name):
    """get card by display name"""
    return assets_read_by_signature(
        arch,
        attrs={
            "arc_display_name": name,
            "arc_display_type": DOOR_CARD,
        },
    )


# Create actual door and card assets
####################################


def create_jitsuin_paris_site(arch):
    props = {
        "display_name": "Jitsuin Paris",
        "description": "Sales and sales support for the French region",
        "latitude": 48.8339211,
        "longitude": 2.371345,
    }
    attrs = {
        "address": "5 Parvis Alan Turing, 75013 Paris, France",
        "wavestone_ext": "managed",
    }
    return locations_create_if_not_exists(arch, props, attrs=attrs)


def create_jitsuin_paris_image(arch):
    with open(f"{IMAGEDIR}/assets/entry_terminal.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_jitsuin_paris(arch, location, attachments):

    # Unlike the others, which feature images of the whole building,
    # this one is actually a close-up of the connected door terminal
    doors_create(
        arch,
        "paris.france.jitsuin.das",
        "Jitsuin front door",
        "das-j1-01",
        (
            "Electronic door entry system controlling the main "
            "staff entrance to Jitsuin France"
        ),
        location,
        attachments,
    )


def create_cityhall_site(arch):
    props = {
        "display_name": "Paris City Hall",
        "description": "Seat of Paris local city adminstration",
        "latitude": 48.856389,
        "longitude": 2.352222,
    }
    attrs = {
        "address": "Place de l'Hôtel de Ville, 75004 Paris, France",
        "wavestone_ext": "managed",
    }
    return locations_create_if_not_exists(arch, props, attrs=attrs)


def create_cityhall_image(arch):
    with open(f"{IMAGEDIR}/assets/cityhall.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_cityhall(arch, location, attachments):

    doors_create(
        arch,
        "cityhall.paris.wavestonedas",
        "City Hall front door",
        "das-x4-01",
        (
            "Electronic door entry system controlling the main "
            "staff entrance to Paris City Hall"
        ),
        location,
        attachments,
    )


def create_courts_site(arch):
    props = {
        "display_name": "Paris Courts of Justice",
        "description": ("Public museum in the former Palais de Justice"),
        "latitude": 48.855722,
        "longitude": 2.345051,
    }
    attrs = {
        "address": "10 Boulevard du Palais, 75001 Paris, France",
        "wavestone_ext": "managed",
    }
    return locations_create_if_not_exists(arch, props, attrs=attrs)


def create_courts_image(arch):
    with open(f"{IMAGEDIR}/assets/courts.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_courts(arch, location, attachments):
    doors_create(
        arch,
        "courts.paris.wavestonedas",
        "Courts of Justice front door",
        "das-x4-02",
        (
            "Electronic door entry system controlling the main "
            "staff entrance to Paris Courts of Justice"
        ),
        location,
        attachments,
    )


def create_bastille_site(arch):
    props = {
        "display_name": "Bastille",
        "description": ("Medieval fortress, made famous by the " "French Revolution"),
        "latitude": 48.85333,
        "longitude": 2.36917,
    }
    attrs = {
        "address": "Place de la Bastille, 75011 Paris, France",
        "wavestone_ext": "managed",
    }
    return locations_create_if_not_exists(arch, props, attrs=attrs)


def create_bastille_image(arch):
    with open(f"{IMAGEDIR}/assets/bastille.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_bastille(arch, location, attachments):

    doors_create(
        arch,
        "bastille.paris.wavestonedas",
        "Bastille front door",
        "das-x4-03",
        (
            "Electronic door entry system controlling the main "
            "staff entrance to Bastille"
        ),
        location,
        attachments,
    )


def create_gdn_site(arch):
    props = {
        "display_name": "Apartements du Gare du Nord",
        "description": (
            "Residential apartment building in new complex " "above GdN station"
        ),
        "latitude": 48.8809,
        "longitude": 2.3553,
    }
    attrs = {
        "address": "18 Rue de Dunkerque, 75010 Paris, France",
        "wavestone_ext": "managed",
    }
    return locations_create_if_not_exists(arch, props, attrs=attrs)


def create_gdn_front_image(arch):
    with open(f"{IMAGEDIR}/assets/gdn_front.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_gdn_front(arch, location, attachments):

    doors_create(
        arch,
        "front.gdn.paris.wavestonedas",
        "Gare du Nord apartments front door",
        "das-x4-04",
        (
            "Electronic door entry system controlling the front "
            "residential entrance to Apartements du Gare du Nord"
        ),
        location,
        attachments,
    )


def create_gdn_side_image(arch):
    with open(f"{IMAGEDIR}/assets/gdn_side.jpg", "rb") as fd:
        return arch.attachments.upload(fd)


def create_gdn_side(arch, location, attachments):

    doors_create(
        arch,
        "side.gdn.paris.wavestonedas",
        "Gare du Nord apartments side door",
        "das-x4-05",
        (
            "Electronic door entry system controlling the side "
            "residential entrance to Apartements du Gare du Nord"
        ),
        location,
        attachments,
    )


def create_doors(arch):
    LOGGER.info("Creating all doors...")
    # For each chosen building we create a location
    # first and then create the door asset to go in it.
    create_jitsuin_paris(
        arch,
        create_jitsuin_paris_site(arch),
        [create_jitsuin_paris_image(arch)],
    )
    create_cityhall(
        arch,
        create_cityhall_site(arch),
        [create_cityhall_image(arch)],
    )
    create_courts(
        arch,
        create_courts_site(arch),
        [create_courts_image(arch)],
    )
    create_bastille(
        arch,
        create_bastille_site(arch),
        [create_bastille_image(arch)],
    )

    gdn_site = create_gdn_site(arch)
    create_gdn_front(
        arch,
        gdn_site,
        [create_gdn_front_image(arch)],
    )
    create_gdn_side(
        arch,
        gdn_site,
        [create_gdn_side_image(arch)],
    )
    LOGGER.info("All doors created")


def create_cards(arch):
    LOGGER.info("Creating all cards...")
    # We don't create locations for cards - they float free.
    # If there's a natural affinity between cards and home
    # locations/owners in the real world then of course we
    # can add this.
    # Similarly there's no real benefit to creating a
    # Primary_image for them so leave that empty too
    for i in range(5):
        cards_create(arch, i)

    LOGGER.info("All cards created")


# Use case functions
####################


def list_doors(arch):
    LOGGER.info("Listing all doors tracked by the system:")
    for door in doors_list(arch):
        attrs = door["attributes"]
        location = arch.locations.read(attrs["arc_home_location_identity"])
        attachments = attrs["arc_attachments"] or []

        print(f"\tAsset name:\t{attrs['arc_display_name']}")
        print(f"\tAsset type:\t{attrs['arc_display_type']}")
        print(f"\tAsset location:\t{location['display_name']}")
        print(f"\tAsset address:\t{location['attributes']['address']}")
        print(f"\tArchivist ID:\t{door['identity']}")
        for a in attachments:
            print(f"\tAttachment identity: \t{a['arc_attachment_identity']}")
            print(f"\tAttachment name: \t{a['arc_display_name']}")
            with open("/tmp/xxx", "wb") as fd:
                attachment = arch.attachments.download(a["arc_attachment_identity"], fd)
                print(f"\tAttachment: \t{attachment}")

        print("-----")


def list_cards(arch):
    LOGGER.info("Listing all cards tracked by the system:")
    for card in cards_list(arch):
        attrs = card["attributes"]
        print(f"\tAsset name:\t{attrs['arc_display_name']}")
        print(f"\tAsset type:\t{attrs['arc_display_type']}")
        print(f"\tArchivist ID:\t{card['identity']}")
        print("-----")


def print_door_event(event):
    attrs = event["event_attributes"]

    when = event.when  # use a property on the event
    who = event.who  # use a property on the event
    if "wavestone_card_name" in attrs:
        card = attrs["wavestone_card_name"]
    else:
        card = "Unknown Card"

    print(f"Details of {attrs['wavestone_evt_type']} event:")
    print(f"\tWho:\t{who}")
    print(f"\tWhen:\t{when}")
    print(f"\tCard:\t{card}")
    print(f"\tDetails:\t{attrs['arc_description']}")
    print("-----")


def print_card_event(event):
    attrs = event["event_attributes"]
    who = event.who  # use a property of the event
    when = event.when  # use a property of the event
    if "wavestone_door_name" in attrs:
        where = attrs["wavestone_door_name"]
    else:
        where = "Unknown Door"

    print(f"Details of {attrs['wavestone_evt_type']} event:")
    print(f"\tWho:\t{who}")
    print(f"\tWhen:\t{when}")
    print(f"\tWhere:\t{where}")
    print(f"\tDetails:\t{attrs['arc_description']}")
    print("-----")


def list_usage(arch, assetspec):
    LOGGER.info("Listing usage of '%s': ", assetspec)

    # If it's not already an Archivist identity, try loading it by name
    try:
        asset = doors_read_by_name(arch, assetspec)

    except ArchivistNotFoundError:
        asset = cards_read_by_name(arch, assetspec)
        print_fn = print_card_event
    else:
        LOGGER.info("Door found '%s'", asset["identity"])
        print_fn = print_door_event

    # Now get the events
    # Note that using the REST API we could pre-filter this list,
    # but here we just grab all the events to show client-side
    # custom attribute filtering can work too. In this case we're
    # only interested in custom events with wavestone_evt_type set,
    # so we avoid the various firmware, maintenance, and admin
    # events. We'll deal with those in a separate example.
    # Be careful of doing this in production: the lists could get
    # very long and client-side processing could be slow.
    props = {"asset_identity": asset["identity"]}
    for event in arch.events.list(props=props):
        attrs = event["event_attributes"]
        if "wavestone_evt_type" in attrs:
            print_fn(event)


def open_door(arch, doorid, cardid):
    # Note: We will not be checking any kind of access control
    # on the cards<->doors permissions in this example - that's
    # a different test. All door accesses will work, and will
    # be logged.
    LOGGER.info("Opening door '%s' with card '%s': START", doorid, cardid)

    # Fetch both assets
    # Note that for other purposes in this example we already
    # got the whole list of doors and cards and could simply
    # find them in our local copy, but we want to show different
    # techniques so here we'll fetch them the 'proper' way,
    # including safety for fetching by UID or friendly name.
    # the read method will try getting by name if doorid is not
    # an identity
    LOGGER.info("doorid %s", doorid)
    door = doors_read_by_name(arch, doorid)
    LOGGER.info("cardid %s", cardid)
    card = cards_read_by_name(arch, cardid)
    if not door or not card:
        LOGGER.error("One or more required assets is missing")
        return

    # x-reference them
    wsext_cardname = card.name
    wsext_doorname = door.name
    wsext_door_wsid = door["attributes"]["wavestone_asset_id"]
    corval = str(uuid.uuid4())

    # Work out where we are
    location = arch.locations.read(door["attributes"]["arc_home_location_identity"])
    if not location:
        LOGGER.error("Door location is missing")
        return

    # Capture a picture of the building entrance
    # In this example we just dig out the main image of the building
    # but the principle here is that the operative could snap it from
    # their smartphone or similar to prove they were there, much like
    # delivery people take photos of parcels left in safe places
    door_image = door.primary_image
    if not door_image:
        LOGGER.error("Door location is missing")
        return

    # Capture a picture from the built-in camera on the door
    # entry device
    # Note that doing this will create a new attachment every time
    # this is called, even though in this example it's always the
    # same image. This simulates having a unique image captured each
    # time but if the use case demands it is perfectly possible to
    # attach the same attachment ID to multiple assets/events rather
    # than duplicating them
    with open(f"{IMAGEDIR}/events/dooropen.png", "rb") as fd:
        image = arch.attachments.upload(fd)

    # Issue RecordEvidence logs on each.
    unused_door_record_evidence = events_create(
        arch,
        door["identity"],
        {
            # Simple evidence event - not interpreted by the
            # Archivist system but can be analysed externally
            "operation": "Record",
            "behaviour": "RecordEvidence",
            # Masquerade as an independent device. This allows the single
            # script to superficially appear like multiple actors, and this
            # functionality is genueinely useful in the case of mobile apps
            # or shared terminals where the actual app credential is less
            # interesting than the logged in user, but note that the system
            # WILL record the actual user from the JWT as well.
            "principal_declared": {
                "subject": f"{wsext_door_wsid}",
                "email": f"{wsext_door_wsid}@iot.wavestone.com",
                "display_name": f"{wsext_doorname} machine credential",
            },
        },
        {
            # Required properties for the Archivist system
            "arc_description": f"Door opened by authorised key card '{wsext_cardname}'",
            "arc_display_type": "Door Open",
            "arc_evidence": "ARQC: 0x12345678",
            # Optional property allows us to link events together
            "arc_correlation_value": corval,
            # Extended properties - can be anything, these are
            # just an example that are convenient to the
            # example use case
            "wavestone_card_name": wsext_cardname,
            "wavestone_card_archivist_id": card["identity"],
            "wavestone_evt_type": "door_open",
            # Attachments list is optional, and allows attaching extra evidence
            # such as photographs, scans, PDFs etc to the event record. Adding
            # one with dispaly name arc_primary_image will instruct the UI to
            # display it (although it's not required)
            "arc_attachments": [
                {
                    "arc_display_name": "arc_primary_image",
                    "arc_attachment_identity": image["identity"],
                    "arc_hash_value": image["hash"]["value"],
                    "arc_hash_alg": image["hash"]["alg"],
                }
            ],
        },
        confirm=True,
    )

    unused_card_record_evidence = events_create(
        arch,
        card["identity"],
        {
            "operation": "Record",
            "behaviour": "RecordEvidence",
            # In our model the cards are not capable of running code
            # or reporting anything, so some other agent has to do it.
            # In this example the door access unit reports both events
            # but we could equally use an app on the PC in the building
            # manager's broom closet if that's more realistic.
            "principal_declared": {
                "subject": f"{wsext_door_wsid}",
                "email": f"{wsext_door_wsid}@iot.wavestone.com",
                "display_name": f"{wsext_doorname} machine credential",
            },
        },
        {
            "arc_description": f"Opened door '{wsext_doorname}'",
            "arc_display_type": "Door Open",
            "arc_evidence": "ARQC: 0x12345678",
            "arc_correlation_value": corval,
            # Events take optional GIS coordinates to record where
            # they happened and trace movements. In this case things
            # are very simple - we just record the fixed location of
            # the door being opened - but it can be used for any
            # mobile asset such as a self-driving car, a drone, or a
            # container in supply chain events
            "arc_gis_lat": f"{location['latitude']}",
            "arc_gis_lng": f"{location['longitude']}",
            "wavestone_door_name": wsext_doorname,
            "wavestone_door_archivist_id": door["identity"],
            "wavestone_evt_type": "door_open",
            "arc_attachments": [door_image],
        },
        confirm=True,
    )
    LOGGER.info("Opening door '%s' with card '%s': FINISHED", doorid, cardid)


# Main app
##########


def run(poc, args):

    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", poc.namespace)

    number_of_doors = doors_count(poc)
    LOGGER.info("number of doors %d", number_of_doors)
    number_of_cards = cards_count(poc)
    LOGGER.info("number of cards %d", number_of_cards)

    if args.create_assets:
        if number_of_doors == 0:
            create_doors(poc)
            if args.wait_for_confirmation:
                doors_wait_for_confirmed(poc)

        if number_of_cards == 0:
            create_cards(poc)
            if args.wait_for_confirmation:
                cards_wait_for_confirmed(poc)

        sys_exit(0)

    if number_of_doors == 0:
        LOGGER.error("Could not find door entry assets. Please create them first.")
        sys_exit(1)

    if number_of_cards == 0:
        LOGGER.error("Could not find card assets. Please create them first.")
        sys_exit(1)

    # Show info about the system ?
    if args.listspec:
        spec = args.listspec
        LOGGER.info("List %s START", spec)
        if spec == "all":
            list_doors(poc)
            list_cards(poc)
        elif spec == "doors":
            list_doors(poc)
        elif spec == "cards":
            list_cards(poc)
        else:
            # Try to interpret it as an asset ID and list the usage
            list_usage(poc, spec)

        LOGGER.info("List %s FINISH", spec)
        sys_exit(0)

    # Open a door using a specified card ?
    if args.doorid_cardid:
        doorid, cardid = args.doorid_cardid
        open_door(poc, doorid, cardid)
        sys_exit(0)
