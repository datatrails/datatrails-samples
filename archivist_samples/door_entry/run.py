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


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from copy import copy
import logging
from sys import exit as sys_exit
import uuid

from archivist import about
from archivist.errors import ArchivistNotFoundError

from .images import assets as images_assets
from .images import events as images_events

from ..testing.locations import (
    locations_create_if_not_exists,
)

DOOR_TERMINAL = "Door access terminal"
DOOR_CARD = "Door entry card"

LOGGER = logging.getLogger(__name__)


# Door asset
############


def doors_create(
    doors,
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
        "wavestone_asset_id": ws_id,
    }
    return doors_create_if_not_exists(
        doors,
        attrs,
        confirm=False,  # confirmed elsewhere
    )


def doors_create_if_not_exists(doors, attrs, *, confirm=None):
    door = None
    try:
        door = doors.assets.read_by_signature(
            attrs={
                "arc_display_name": attrs["arc_display_name"],
            },
        )
    except ArchivistNotFoundError:
        door = doors.assets.create(attrs=attrs, confirm=confirm)

    return door


# Card asset
############


def cards_create(cards, idx):
    return cards_create_if_not_exists(
        cards,
        {
            "arc_serial_number": f"sc-x5-{idx}",
            "arc_display_name": f"access_card_{idx}",
            "arc_description": f"Electronic door access card #{idx}",
        },
        confirm=False,  # confirmed elsewhere
    )


def cards_create_if_not_exists(cards, attrs, *, confirm=None):
    card = None
    try:
        card = cards.assets.read_by_signature(
            attrs={
                "arc_display_name": attrs["arc_display_name"],
            },
        )
    except ArchivistNotFoundError:
        card = cards.assets.create(attrs=attrs, confirm=confirm)

    return card


# Create actual door and card assets
####################################


def create_jitsuin_paris_site(doors):
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
    return locations_create_if_not_exists(doors, props, attrs=attrs)


def create_jitsuin_paris_image(doors):
    with pkg_resources.open_binary(images_assets, "entry_terminal.jpg") as fd:
        return doors.attachments.upload(fd)


def create_jitsuin_paris(doors, location, attachments):

    # Unlike the others, which feature images of the whole building,
    # this one is actually a close-up of the connected door terminal
    doors_create(
        doors,
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


def create_cityhall_site(doors):
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
    return locations_create_if_not_exists(doors, props, attrs=attrs)


def create_cityhall_image(doors):
    with pkg_resources.open_binary(images_assets, "cityhall.jpg") as fd:
        return doors.attachments.upload(fd)


def create_cityhall(doors, location, attachments):

    doors_create(
        doors,
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


def create_courts_site(doors):
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
    return locations_create_if_not_exists(doors, props, attrs=attrs)


def create_courts_image(doors):
    with pkg_resources.open_binary(images_assets, "courts.jpg") as fd:
        return doors.attachments.upload(fd)


def create_courts(doors, location, attachments):
    doors_create(
        doors,
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


def create_bastille_site(doors):
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
    return locations_create_if_not_exists(doors, props, attrs=attrs)


def create_bastille_image(doors):
    with pkg_resources.open_binary(images_assets, "bastille.jpg") as fd:
        return doors.attachments.upload(fd)


def create_bastille(doors, location, attachments):

    doors_create(
        doors,
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


def create_gdn_site(doors):
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
    return locations_create_if_not_exists(doors, props, attrs=attrs)


def create_gdn_front_image(doors):
    with pkg_resources.open_binary(images_assets, "gdn_front.jpg") as fd:
        return doors.attachments.upload(fd)


def create_gdn_front(doors, location, attachments):

    doors_create(
        doors,
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


def create_gdn_side_image(doors):
    with pkg_resources.open_binary(images_assets, "gdn_side.jpg") as fd:
        return doors.attachments.upload(fd)


def create_gdn_side(doors, location, attachments):

    doors_create(
        doors,
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


def create_doors(doors):
    LOGGER.info("Creating all doors...")
    # For each chosen building we create a location
    # first and then create the door asset to go in it.
    create_jitsuin_paris(
        doors,
        create_jitsuin_paris_site(doors),
        [create_jitsuin_paris_image(doors)],
    )
    create_cityhall(
        doors,
        create_cityhall_site(doors),
        [create_cityhall_image(doors)],
    )
    create_courts(
        doors,
        create_courts_site(doors),
        [create_courts_image(doors)],
    )
    create_bastille(
        doors,
        create_bastille_site(doors),
        [create_bastille_image(doors)],
    )

    gdn_site = create_gdn_site(doors)
    create_gdn_front(
        doors,
        gdn_site,
        [create_gdn_front_image(doors)],
    )
    create_gdn_side(
        doors,
        gdn_site,
        [create_gdn_side_image(doors)],
    )
    LOGGER.info("All doors created")


def create_cards(cards):
    LOGGER.info("Creating all cards...")
    # We don't create locations for cards - they float free.
    # If there's a natural affinity between cards and home
    # locations/owners in the real world then of course we
    # can add this.
    # Similarly there's no real benefit to creating a
    # Primary_image for them so leave that empty too
    for i in range(5):
        cards_create(cards, i)

    LOGGER.info("All cards created")


# Use case functions
####################


def list_doors(doors):
    LOGGER.info("Listing all doors tracked by the system:")
    for door in doors.assets.list():
        attrs = door["attributes"]
        location = doors.locations.read(attrs["arc_home_location_identity"])
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
                doors.attachments.download(a["arc_attachment_identity"], fd)

        print("-----")


def list_cards(cards):
    LOGGER.info("Listing all cards tracked by the system:")
    for card in cards.assets.list():
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


def list_usage(doors, cards, assetname):
    LOGGER.info("Listing usage of '%s': ", assetname)

    # If it's not already an Archivist identity, try loading it by name
    try:
        asset = doors.assets.read_by_signature(
            attrs={
                "arc_display_name": assetname,
            },
        )

    except ArchivistNotFoundError:
        asset = cards.assets.read_by_signature(
            attrs={
                "arc_display_name": assetname,
            },
        )
        print_fn = print_card_event
        endpoint = cards

    else:
        LOGGER.info("Door found '%s'", asset["identity"])
        print_fn = print_door_event
        endpoint = doors

    # Now get the events
    # Note that using the REST API we could pre-filter this list,
    # but here we just grab all the events to show client-side
    # custom attribute filtering can work too. In this case we're
    # only interested in custom events with wavestone_evt_type set,
    # so we avoid the various firmware, maintenance, and admin
    # events. We'll deal with those in a separate example.
    # Be careful of doing this in production: the lists could get
    # very long and client-side processing could be slow.
    for event in endpoint.events.list(asset_id=asset["identity"]):
        attrs = event["event_attributes"]
        if "wavestone_evt_type" in attrs:
            print_fn(event)


def open_door(doors, doorid, cards, cardid):
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
    door = doors.assets.read_by_signature(
        attrs={
            "arc_display_name": doorid,
        },
    )

    LOGGER.info("cardid %s", cardid)
    card = cards.assets.read_by_signature(
        attrs={
            "arc_display_name": cardid,
        },
    )
    if not door or not card:
        LOGGER.error("One or more required assets is missing")
        return

    # x-reference them
    wsext_cardname = card.name
    wsext_doorname = door.name
    wsext_door_wsid = door["attributes"]["wavestone_asset_id"]
    corval = str(uuid.uuid4())

    # Work out where we are
    location = doors.locations.read(door["attributes"]["arc_home_location_identity"])
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
    with pkg_resources.open_binary(images_events, "dooropen.png") as fd:
        image = doors.attachments.upload(fd)

    # Issue RecordEvidence logs on each.
    unused_door_record_evidence = doors.events.create(
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

    unused_card_record_evidence = cards.events.create(
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

    doors = copy(poc)
    doors.fixtures = {
        "assets": {
            "attributes": {
                "arc_display_type": DOOR_TERMINAL,
            },
        }
    }
    cards = copy(poc)
    cards.fixtures = {
        "assets": {
            "attributes": {
                "arc_display_type": DOOR_CARD,
            },
        }
    }

    number_of_doors = doors.assets.count()
    LOGGER.info("number of doors %d", number_of_doors)
    number_of_cards = cards.assets.count()
    LOGGER.info("number of cards %d", number_of_cards)

    if args.create_assets:
        if number_of_doors == 0:
            create_doors(doors)
            if args.wait_for_confirmation:
                doors.assets.wait_for_confirmed()

        if number_of_cards == 0:
            create_cards(cards)
            if args.wait_for_confirmation:
                cards.assets.wait_for_confirmed()

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
            list_doors(doors)
            list_cards(cards)
        elif spec == "doors":
            list_doors(doors)
        elif spec == "cards":
            list_cards(cards)
        else:
            # Try to interpret it as an asset ID and list the usage
            list_usage(doors, cards, spec)

        LOGGER.info("List %s FINISH", spec)
        sys_exit(0)

    # Open a door using a specified card ?
    if args.doorid_cardid:
        doorid, cardid = args.doorid_cardid
        open_door(doors, doorid, cards, cardid)
        sys_exit(0)
