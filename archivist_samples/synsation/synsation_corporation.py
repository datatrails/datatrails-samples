# Definitions and data for Synsation Corporation demo data

# pylint: disable=missing-docstring

import logging
import random
import time

from ..testing.assets import (
    make_assets_create,
)

from .util import (
    asset_attachment_upload_from_file,
    locations_from_yaml_file,
)

LOGGER = logging.getLogger(__name__)


def attachment_create(arch, name):
    attachment = asset_attachment_upload_from_file(arch, name, "image/jpg")
    result = {
        "arc_attribute_type": "arc_attachment",
        "arc_blob_identity": attachment["identity"],
        "arc_blob_hash_alg": attachment["hash"]["alg"],
        "arc_blob_hash_value": attachment["hash"]["value"],
        "arc_file_name": name,
    }

    return result


machines_creator = make_assets_create(
    attachment_creator=attachment_create, confirm=False
)


def initialise_asset_types():
    type_map = {}

    type_map["Multifunction Printer"] = "multifunction_printer.jpg"
    type_map["Connected Coffee Machine"] = "coffee_machine.jpg"
    type_map["Security Camera"] = "black_cctv.jpg"

    LOGGER.debug(type_map)

    return type_map


def create_locations():
    corporation_locations = {}

    newlocation = locations_from_yaml_file("grayslake.yaml")
    corporation_locations[newlocation["props"]["display_name"]] = newlocation

    newlocation = locations_from_yaml_file("baltimore.yaml")
    corporation_locations[newlocation["props"]["display_name"]] = newlocation

    newlocation = locations_from_yaml_file("european.yaml")
    corporation_locations[newlocation["props"]["display_name"]] = newlocation

    newlocation = locations_from_yaml_file("asia.yaml")
    corporation_locations[newlocation["props"]["display_name"]] = newlocation

    newlocation = locations_from_yaml_file("za.yaml")
    corporation_locations[newlocation["props"]["display_name"]] = newlocation

    LOGGER.debug(corporation_locations)

    return corporation_locations


def create_assets(arch, asset_types, locations, num_assets, timedelay):
    corporation_assets = {}

    for i in range(num_assets):
        displaytype = random.choice(list(asset_types))
        safetype = displaytype.replace(" ", "").lower()
        displayname = f"synsation.assets.{safetype}_{i}"
        description = (
            f"This is my {displaytype}. There are many like it, "
            f"but this one is #{i}"
        )

        location = "Cape Town"  # reserved location
        while location == "Cape Town":
            location = random.choice(list(locations))
        location = locations[location]

        newasset, _ = machines_creator(
            arch,
            displayname,
            {
                "arc_description": description,
                "arc_firmware_version": "1.0",
                "arc_serial_number": "f867662g.1",
                "arc_display_type": displaytype,
            },
            location=location,
            attachments={
                asset_types[displaytype],
            },
        )
        corporation_assets[displayname] = newasset["identity"]

        time.sleep(timedelay)

    LOGGER.debug(corporation_assets)

    return corporation_assets


def initialise_all(ac, num_assets, timedelay):
    LOGGER.info("Creating data for Synsation Corporation...")
    asset_types = initialise_asset_types()
    locations = create_locations()
    assets = create_assets(ac, asset_types, locations, num_assets, timedelay)
    LOGGER.info(
        "%d assets of %d different types created across %d locations.",
        len(assets),
        len(asset_types),
        len(locations),
    )
