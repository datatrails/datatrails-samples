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

# Definitions and data for Synsation Manufacturing demo data

# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments

import string
import random
import time

from ..testing.assets import assets_create_if_not_exists

from .util import asset_attachment_upload_from_file


def initialise_asset_types(ac):
    type_map = {}

    newattachment = asset_attachment_upload_from_file(
        ac,
        "crate.jpg",
        "image/jpg",
    )
    type_map["Shipping Crate"] = newattachment

    return type_map


def create_locations(ac):
    locations = {}

    # According to wikipedia, the canonical location of
    # Flint, Michigan is 43° 1′ 8″ N, 83° 41′ 36″ W
    displayname = "Flint Manufacturing Center"
    props = {
        "display_name": displayname,
        "description": "Global Headquarters",
        "latitude": 43.018889,
        "longitude": -83.693333,
    }
    attrs = {
        "address": "Flint 48501, Michigan",
        "Facility Type": "Manufacturing",
        "reception_email": "reception_FM@synsation.io",
        "reception_phone": "+1 (810) 123-4567",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    locations[displayname] = newlocation["identity"]
    time.sleep(1)

    # According to wikipedia, the canonical location of
    # Stuttgart is 48° 47′ 0″ N, 9° 11′ 0″ E
    displayname = "Stuttgart Finishing Plant"
    props = {
        "display_name": displayname,
        "description": "European Distribution Center",
        "latitude": 48.783333,
        "longitude": 9.183333,
    }
    attrs = {
        "address": "70173 Stuttgart, Germany",
        "Facility Type": "Manufacturing",
        "reception_email": "reception_ST@synsation.io",
        "reception_phone": "+49 (711) 123-456",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    locations[displayname] = newlocation["identity"]

    return locations


def create_shipping_crate(
    ac, name, serial, description, track_id, image, loc_id, capacity
):
    attrs = {
        "arc_firmware_version": "1.0",
        "arc_serial_number": serial,
        "arc_display_name": name,
        "arc_description": description,
        "arc_home_location_identity": loc_id,
        "arc_display_type": "Widget shipping crate",
        "synsation_crate_tracking_id": track_id,
        "synsation_crate_capacity": capacity,
        "arc_attachments": [
            {
                "arc_display_name": "arc_primary_image",
                "arc_attachment_identity": image["identity"],
                "arc_hash_value": image["hash"]["value"],
                "arc_hash_alg": image["hash"]["alg"],
            }
        ],
    }
    newasset = assets_create_if_not_exists(ac, attrs)
    return newasset


def initialise_all(ac):
    asset_types = initialise_asset_types(ac)
    manufacturing_locations = create_locations(ac)

    # Create a single crate to demonstrate mobile assets use case
    tracking_id = "FLINT-" + "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )
    batch_num = "2019x" + "".join(random.choice(string.digits) for _ in range(8))
    displayname = f"Flint-SMC-{batch_num}"
    description = f"Small crate for batch {batch_num}, capacity 500"

    create_shipping_crate(
        ac,
        displayname,
        batch_num,
        description,
        tracking_id,
        asset_types["Shipping Crate"],
        manufacturing_locations["Flint Manufacturing Center"],
        "500",
    )

    return True
