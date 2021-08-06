#   Copyright 2021 Jitsuin, inc
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
    # Try backported to PY<37 'importlib_resources'.
    import importlib_resources as pkg_resources

import logging
import random
import string

from sys import exit as sys_exit
from archivist import about

from . import wipp_files

from .wipp import Wipp

LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, path, name):
    with pkg_resources.open_binary(wipp_files, path) as fd:
        blob = arch.attachments.upload(fd)
        attachment = {
            "arc_display_name": name,
            "arc_attachment_identity": blob["identity"],
            "arc_hash_value": blob["hash"]["value"],
            "arc_hash_alg": blob["hash"]["alg"],
        }
        return attachment


def run(arch):

    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", arch.namespace)

    # Wipp class encapsulates wipp object in RKVST
    LOGGER.info("Creating Drum Asset...")
    drum = Wipp(arch, storage_integrity=arch.storage_integrity)
    serial_num = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    drumname = 'Drum-' + serial_num

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
    LOGGER.info("Drum Asset Created (Identity=%s)", drum.asset["identity"])

    # Cask Asset
    LOGGER.info("Creating Cask Asset...")
    cask = Wipp(arch, storage_integrity=arch.storage_integrity)
    serial_num = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    caskname = 'Cask-' + serial_num

    cask.caskcreate(
        caskname,
        "NRC certified type-B road shipping container, capacity 3 x 55-gallon drum",
        serial_num,
        attachments=[upload_attachment(arch, "rh72b.png", "arc_primary_image")],
        custom_attrs={
            "wipp_capacity": "3",
        },
    )
    LOGGER.info("Cask Asset Created (Identity=%s)", cask.asset["identity"])

    # Drum Characterization
    LOGGER.info("Adding characterization...")
    drum.characterize(
        {
            "description": "Waste coding characterization: A2 Fraction 2.10E+05",
            "weight": "790300",
            "a2fraction_characterized": "2.10E+05",
            "activity_characterized": "1.69E+02",
            "total_characterized": "2.12E+02",
        },
        attachments=[upload_attachment(arch, "DOE-WIPP-02-3122_Rev_9_FINAL.pdf", "Reference WAC"),
        upload_attachment(arch, "characterization.pdf", "Characterization report")],
    )
    LOGGER.info("Characterization registered...")

    # Drum Tomography
    LOGGER.info("Adding tomography...")
    drum.tomography(
        {
            "description": "Confirming waste coding characterizations",
            "weight": "790300",
            "a2fraction_confirmed": "2.10E+05",
            "activity_confirmed": "1.69E+02",
            "total_confirmed": "2.12E+02",
        },
        attachments=[upload_attachment(arch, "wipp_radiography.jpg", "arc_primary_image"),
        upload_attachment(arch, "DOE-WIPP-02-3122_Rev_9_FINAL.pdf", "Reference WAC")],
    )
    LOGGER.info("Tomography registered...")

    # Loading
    LOGGER.info("Loading drum and cask...")
    drum.loading(
        {
            "description": "Loaded drum into " + cask.asset["attributes"]["arc_display_name"],
            "container": cask.asset["identity"],
        },
        attachments=[upload_attachment(arch, "trupact_loading.jpg", "arc_primary_image")],
    )
    cask.loading(
        {
            "description": "Filled with " + drum.asset["attributes"]["arc_display_name"],
            "container": cask.asset["identity"],
        },
        custom_asset_attrs={
            "wipp_inventory": drum.asset["identity"],
        },
        attachments=[upload_attachment(arch, "trupact_loading.jpg", "arc_primary_image")],
    )
    LOGGER.info("Loading registered...")

    # Pre-shipping
    LOGGER.info("Pre-shipping inspection...")
    drum.preshipping(
        {
            "description": "Inspection inventory " + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[upload_attachment(arch, "preshipment_inspection.jpg", "arc_primary_image")],
    )
    cask.preshipping(
        {
            "description": "Inspected " + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[upload_attachment(arch, "preshipment_inspection.jpg", "arc_primary_image")],
    )
    LOGGER.info("Pre-shipping inspection registered...")

    # Departure
    LOGGER.info("Loading departure...")
    drum.departure(
        {
            "description": "Departed SRS inventory " + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[upload_attachment(arch, "truck_departure.jpg", "arc_primary_image"),
        upload_attachment(arch, "SRS_to_WPP_route_instructions.pdf", "approved_route")],
    )
    cask.departure(
        {
            "description": cask.asset["attributes"]["arc_display_name"] + "departing for WIPP."
        },
        attachments=[upload_attachment(arch, "truck_departure.jpg", "arc_primary_image"),
        upload_attachment(arch, "SRS_to_WPP_route_instructions.pdf", "approved_route")],
    )
    LOGGER.info("Departure registered...")

    # Waypoint
    LOGGER.info("Loading waypoints...")
    cask.waypoint(
        {
            "description": "TRAGIS smart sensors ping: All sensors GREEN",
        },
        custom_attrs={
            "wipp_sensors_shock": "0",
            "wipp_sensors_rad": "45",
        },
        attachments=[upload_attachment(arch, "truck_departure.jpg", "arc_primary_image")],
    )
    LOGGER.info("Waypoint registered...")

    # Arrival
    LOGGER.info("Loading arrival...")
    drum.arrival(
        {
            "description": "At WIPP, inventory" + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[upload_attachment(arch, "truck_arrival.jpg", "arc_primary_image")],
    )
    cask.arrival(
        {
            "description": cask.asset["attributes"]["arc_display_name"] + "arriving at WIPP",
        },
        attachments=[upload_attachment(arch, "truck_arrival.jpg", "arc_primary_image")],
    )
    LOGGER.info("Arrival registered...")

    # Unload
    LOGGER.info("Unloading...")
    drum.unloading(
        {
            "description": "Unloaded drum from cask" + cask.asset["attributes"]["arc_display_name"],
        },
        custom_asset_attrs={
            "wipp_container": "",
        },
        attachments=[upload_attachment(arch, "trupact_unloading.jpg", "arc_primary_image")],
    )
    cask.unloading(
        {
            "description": "Unloaded " + drum.asset["attributes"]["arc_display_name"],
        },
        custom_asset_attrs={
            "wipp_inventory": "",
        },
        attachments=[upload_attachment(arch, "trupact_unloading.jpg", "arc_primary_image")],
    )
    LOGGER.info("Unloading registered...")

    # Emplacement
    LOGGER.info("Loading emplacement...")
    drum.emplacement(
        {
            "description": "Emplacement in location D-32",
            "location": "D-32",
        },
        attachments=[upload_attachment(arch, "waste_placement.jpg", "arc_primary_image")],
    )
    LOGGER.info("Emplacement registered...")
    sys_exit(0)
