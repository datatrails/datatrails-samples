#   Copyright 2019 Jitsuin, inc
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

# Definitions and data for Synsation Corporation demo data

# pylint: disable=missing-docstring

import random
import time

from archivist.logger import LOGGER

from testing.namespace import (
    locations_create_from_yaml_file,
)

from .util import (
    assets_create_if_not_exists,
    attachments_read_from_file,
)


def initialise_asset_types(ac, timedelay):
    type_map = {}

    newattachment = attachments_read_from_file(
        ac, "assets/multifunction_printer.jpg", "image/jpg"
    )
    type_map["Multifunction Printer"] = newattachment
    time.sleep(timedelay)

    newattachment = attachments_read_from_file(
        ac, "assets/coffee_machine.jpg", "image/jpg"
    )
    type_map["Connected Coffee Machine"] = newattachment
    time.sleep(timedelay)

    newattachment = attachments_read_from_file(ac, "assets/black_cctv.jpg", "image/jpg")
    type_map["Security Camera"] = newattachment
    time.sleep(timedelay)

    LOGGER.debug(type_map)

    return type_map


def create_locations(ac, timedelay):
    corporation_locations = {}

    newlocation = locations_create_from_yaml_file(
        ac, "synsation/locations/grayslake.yaml"
    )
    corporation_locations[newlocation["display_name"]] = newlocation["identity"]
    time.sleep(timedelay)

    newlocation = locations_create_from_yaml_file(
        ac, "synsation/locations/baltimore.yaml"
    )
    corporation_locations[newlocation["display_name"]] = newlocation["identity"]
    time.sleep(timedelay)

    newlocation = locations_create_from_yaml_file(
        ac, "synsation/locations/european.yaml"
    )
    corporation_locations[newlocation["display_name"]] = newlocation["identity"]
    time.sleep(timedelay)

    newlocation = locations_create_from_yaml_file(ac, "synsation/locations/asia.yaml")
    corporation_locations[newlocation["display_name"]] = newlocation["identity"]
    time.sleep(timedelay)

    newlocation = locations_create_from_yaml_file(ac, "synsation/locations/za.yaml")
    corporation_locations[newlocation["display_name"]] = newlocation["identity"]
    time.sleep(timedelay)

    LOGGER.debug(corporation_locations)

    return corporation_locations


def create_assets(ac, asset_types, locations, num_assets, timedelay):
    corporation_assets = {}

    for i in range(num_assets):
        displaytype = random.choice(list(asset_types.keys()))
        safetype = displaytype.replace(" ", "").lower()
        displayname = f"synsation.assets.{safetype}_{i}"
        description = (
            f"This is my {displaytype}. There are many like it, "
            f"but this one is #{i}"
        )

        location = "Cape Town"  # reserved location
        while location == "Cape Town":
            location = random.choice(list(locations.keys()))
        location_id = locations[location]

        attrs = {
            "arc_firmware_version": "1.0",
            "arc_serial_number": "f867662g.1",
            "arc_display_name": displayname,
            "arc_description": description,
            "arc_home_location_identity": location_id,
            "arc_display_type": displaytype,
            "arc_attachments": [
                {
                    "arc_display_name": "arc_primary_image",
                    "arc_attachment_identity": asset_types[displaytype]["identity"],
                    "arc_hash_value": asset_types[displaytype]["hash"]["value"],
                    "arc_hash_alg": asset_types[displaytype]["hash"]["alg"],
                }
            ],
        }
        behaviours = [
            "Attachments",
            "Firmware",
            "LocationUpdate",
            "Maintenance",
            "RecordEvidence",
        ]
        newasset = assets_create_if_not_exists(ac, behaviours, attrs)
        corporation_assets[displayname] = newasset["identity"]

        time.sleep(timedelay)

    LOGGER.debug(corporation_assets)

    return corporation_assets


def initialise_all(ac, num_assets, timedelay):
    LOGGER.info("Creating data for Synsation Corporation...")
    asset_types = initialise_asset_types(ac, timedelay)
    locations = create_locations(ac, timedelay)
    assets = create_assets(ac, asset_types, locations, num_assets, timedelay)
    LOGGER.info(
        "%d assets of %d different types " "created across %d locations.",
        len(assets),
        len(asset_types),
        len(locations),
    )
