# Definitions and data for Synsation Manufacturing demo data

# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments

import string
import random

from ..testing.assets import make_assets_create, AttachmentDescription

from .util import asset_attachment_upload_from_file


def attachment_create(arch, attachment_description: AttachmentDescription):
    attachment = asset_attachment_upload_from_file(
        arch, attachment_description.filename, "image/jpg"
    )
    result = {
        "arc_attribute_type": "arc_attachment",
        "arc_blob_identity": attachment["identity"],
        "arc_blob_hash_alg": attachment["hash"]["alg"],
        "arc_blob_hash_value": attachment["hash"]["value"],
        "arc_file_name": attachment_description.filename,
    }

    return result


crates_creator = make_assets_create(attachment_creator=attachment_create, confirm=True)


def initialise_asset_types():
    type_map = {}
    type_map["Shipping Crate"] = "crate.jpg"

    return type_map


def create_locations():
    locations = {}

    # According to wikipedia, the canonical location of
    # Flint, Michigan is 43° 1′ 8″ N, 83° 41′ 36″ W
    displayname = "Flint Manufacturing Center"
    locations[displayname] = {
        "props": {
            "display_name": displayname,
            "description": "Global Headquarters",
            "latitude": 43.018889,
            "longitude": -83.693333,
        },
        "attrs": {
            "address": "Flint 48501, Michigan",
            "Facility Type": "Manufacturing",
            "reception_email": "reception_FM@synsation.io",
            "reception_phone": "+1 (810) 123-4567",
        },
    }

    # According to wikipedia, the canonical location of
    # Stuttgart is 48° 47′ 0″ N, 9° 11′ 0″ E
    displayname = "Stuttgart Finishing Plant"
    locations[displayname] = {
        "props": {
            "display_name": displayname,
            "description": "European Distribution Center",
            "latitude": 48.783333,
            "longitude": 9.183333,
        },
        "attrs": {
            "address": "70173 Stuttgart, Germany",
            "Facility Type": "Manufacturing",
            "reception_email": "reception_ST@synsation.io",
            "reception_phone": "+49 (711) 123-456",
        },
    }
    return locations


def create_shipping_crate(
    arch, name, serial, description, track_id, image, loc_id, capacity
):
    newasset, existed = crates_creator(
        arch,
        name,
        {
            "arc_firmware_version": "1.0",
            "arc_serial_number": serial,
            "arc_description": description,
            "arc_display_type": "Widget shipping crate",
            "synsation_crate_tracking_id": track_id,
            "synsation_crate_capacity": capacity,
        },
        location=loc_id,
        attachments=[
            AttachmentDescription(image, "arc_primary_image"),
        ],
    )
    return newasset, existed


def initialise_all(arch):
    asset_types = initialise_asset_types()
    manufacturing_locations = create_locations()

    # Create a single crate to demonstrate mobile assets use case
    tracking_id = "FLINT-" + "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )
    batch_num = "2019x" + "".join(random.choice(string.digits) for _ in range(8))
    displayname = "Flint-SMC Shipping Crate"
    description = f"Small crate for batch {batch_num}, capacity 500"

    return create_shipping_crate(
        arch,
        displayname,
        batch_num,
        description,
        tracking_id,
        asset_types["Shipping Crate"],
        manufacturing_locations["Flint Manufacturing Center"],
        "500",
    )
