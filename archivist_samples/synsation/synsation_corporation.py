# Definitions and data for Synsation Corporation demo data

# pylint: disable=missing-docstring

import logging
import random
import time

from ..testing.assets import make_assets_create, AttachmentDescription

from .util import (
    asset_attachment_upload_from_file,
)

LOGGER = logging.getLogger(__name__)


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


machines_creator = make_assets_create(
    attachment_creator=attachment_create,
)


def initialise_asset_types():
    type_map = {}

    type_map["Multifunction Printer"] = "multifunction_printer.jpg"
    type_map["Connected Coffee Machine"] = "coffee_machine.jpg"
    type_map["Security Camera"] = "black_cctv.jpg"

    LOGGER.debug(type_map)

    return type_map


def create_assets(arch, asset_types, num_assets, timedelay):
    corporation_assets = {}

    for i in range(num_assets):
        displaytype = random.choice(list(asset_types))
        safetype = displaytype.replace(" ", "").lower()
        displayname = f"synsation.assets.{safetype}_{i}"
        description = (
            f"This is my {displaytype}. There are many like it, "
            f"but this one is #{i}"
        )

        newasset, _ = machines_creator(
            arch,
            displayname,
            {
                "arc_description": description,
                "arc_firmware_version": "1.0",
                "arc_serial_number": "f867662g.1",
                "arc_display_type": displaytype,
            },
            attachments=[
                AttachmentDescription(asset_types[displaytype], "arc_primary_image"),
            ],
        )
        corporation_assets[displayname] = newasset["identity"]

        time.sleep(timedelay)

    LOGGER.debug(corporation_assets)

    return corporation_assets


def initialise_all(ac, num_assets, timedelay):
    LOGGER.info("Creating data for Synsation Corporation...")
    asset_types = initialise_asset_types()
    assets = create_assets(ac, asset_types, num_assets, timedelay)
    LOGGER.info(
        "%d assets of %d different types created.",
        len(assets),
        len(asset_types),
    )
