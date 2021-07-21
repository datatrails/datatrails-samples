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

from archivist import about

from . import nuclear_files

from .nuclear import Nuclear


LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, path, name):
    with pkg_resources.open_binary(image_assets, path) as fd:
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

    # Nuclear class encapsulates SBOM object in RKVST
    LOGGER.info("Creating Nuclear Asset...")
    item = Nuclear(arch)

    item.create(
        "Item-12345",
        "Waste Item demo creation",
        "0",
        "pre-treatement",
        attachments=[upload_attachment(arch, "wasteimage.jpeg", "arc_primary_image")],
    )
    LOGGER.info("Nuclear Item Asset Created (Identity=%s)", item.asset["identity"])

    # Characterize
    LOGGER.info("Adding characterization...")
    item.characterize(
        {
            "name": "Item-12345",
            "description": "Charactized",
            "nw_item_activity_group_b1": "7",
            "nw_fissile_particles": "20",
            "nw_active_particles": "0",
            "nw_activity_nonalpha": "3",
            "nw_item_activity_group_a": "0.6",
            "nw_explosives": "0",
            "nw_soluble_solids": "10000",
            "nw_oxidizing_agents": "0",
            "nw_item_activity_group_b2": "124",
            "nw_item_activity_group_c": "766",
            "nw_waste_weight": "32000000",
            "nw_activity_alpha": "1",
            "nw_waste_code": "20234",
            "nw_lifecycle_stage": "characterized",
            "nw_target_stream": "Combustible",
            "nw_free_liquid": "0",
        }
    )
    LOGGER.info("Characterization registered...")
