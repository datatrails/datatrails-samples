# Definitions and data for Synsation Industries demo data
# In this scenario Synsation Industries runs a series of
# electric vehicle charging points
#
# This also demonstrates the capability to make locations and assets 1:1

# pylint: disable=missing-docstring

import logging
import random
import string

from ..testing.assets import assets_create_if_not_exists

from .util import asset_attachment_upload_from_file

LOGGER = logging.getLogger(__name__)


def initialise_asset_types(ac):
    type_map = {}

    newattachment = asset_attachment_upload_from_file(
        ac, "small_ev_charger.jpg", "image/jpg"
    )
    type_map["Small EV Charger"] = newattachment

    newattachment = asset_attachment_upload_from_file(
        ac, "large_ev_charger.jpg", "image/jpg"
    )
    type_map["Large EV Charger"] = newattachment

    LOGGER.debug(type_map)

    return type_map


def make_charger_location(ac, displayname, description, plat, plong):
    props = {
        "display_name": displayname,
        "description": description,
        "latitude": float(plat),
        "longitude": float(plong),
    }
    newlocation = ac.locations.create(props)
    return newlocation


def make_charger_asset(
    ac, displayname, serial, description, image, loc_id, charger_type
):
    attrs = {
        "arc_firmware_version": "1.0",
        "arc_serial_number": serial,
        "arc_display_name": displayname,
        "arc_description": description,
        "arc_home_location_identity": loc_id,
        "arc_display_type": "EV charging station",
        "synsation_ev_charger_type": charger_type,
        "arc_primary_image": {
            "arc_display_name": "arc_primary_image",
            "arc_attribute_type": "arc_attachment",
            "arc_blob_identity": image["identity"],
            "arc_blob_hash_alg": image["hash"]["alg"],
            "arc_blob_hash_value": image["hash"]["value"],
        },
    }
    newasset = assets_create_if_not_exists(ac, attrs)
    return newasset


def create_charging_stations(ac, stations, airport_code, charger_type, attachment):
    serialrand = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(8)
    )
    for i, station in enumerate(stations):
        displayname = f"{airport_code}-{airport_code}-{i}"
        description = f"{charger_type} charging station at {airport_code}, position {i}"
        serial = f"evc-{serialrand}-{i}"
        newlocation = make_charger_location(
            ac, displayname, description, station[0], station[1]
        )
        make_charger_asset(
            ac,
            displayname,
            serial,
            description,
            attachment,
            newlocation["identity"],
            charger_type,
        )


def initialise_all(ac):
    asset_types = initialise_asset_types(ac)

    # San Francisco International
    stations = [
        ["37.635647", "-122.399518"],
        ["37.635536", "-122.399464"],
        ["37.635366", "-122.399389"],
        ["37.635230", "-122.399292"],
        ["37.635089", "-122.399215"],
        ["37.634936", "-122.399140"],
        ["37.634562", "-122.400299"],
        ["37.634825", "-122.400460"],
        ["37.634689", "-122.400374"],
    ]
    create_charging_stations(
        ac, stations, "SFO", "Large EV Charger", asset_types["Large EV Charger"]
    )

    # San Jose
    stations = [
        ["37.362388", "-121.922858"],
        ["37.362264", "-121.922705"],
        ["37.362128", "-121.922576"],
        ["37.362004", "-121.922431"],
        ["37.361873", "-121.922288"],
    ]
    create_charging_stations(
        ac, stations, "SJC", "Large EV Charger", asset_types["Large EV Charger"]
    )

    # JFK
    stations = [
        ["40.661593", "-73.793409"],
        ["40.661567", "-73.792591"],
        ["40.663480", "-73.791990"],
        ["40.663618", "-73.793353"],
    ]
    create_charging_stations(
        ac, stations, "JFK", "Large EV Charger", asset_types["Large EV Charger"]
    )

    # Chicago O'Hare
    stations = [
        ["41.990217", "-87.884960"],
        ["41.990527", "-87.884964"],
        ["41.990539", "-87.884505"],
        ["41.990220", "-87.884505"],
        ["41.990218", "-87.884266"],
        ["41.990527", "-87.884271"],
        ["41.990535", "-87.883828"],
        ["41.990220", "-87.883809"],
    ]
    create_charging_stations(
        ac, stations, "ORD", "Large EV Charger", asset_types["Large EV Charger"]
    )

    # Chicago Midway
    stations = [["41.778129", "-87.749422"], ["41.777948", "-87.749397"]]
    create_charging_stations(
        ac, stations, "MDW", "Small EV Charger", asset_types["Small EV Charger"]
    )

    LOGGER.info("Synsation Industries EV charger data initialized")
