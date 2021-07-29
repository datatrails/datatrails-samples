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

from archivist import about

from . import nuclear_files

from .nuclear import Nuclear

LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, path, name):
    with pkg_resources.open_binary(nuclear_files, path) as fd:
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

    # Nuclear class encapsulates nuclear object in RKVST
    LOGGER.info("Creating Nuclear Asset...")
    item = Nuclear(arch)
    serial_num = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    itemname = 'Item-' + serial_num

    item.create(
        itemname,
        "Waste Item demo creation",
        attachments=[upload_attachment(arch, "wasteimage.jpeg", "arc_primary_image")],
        custom_attrs={
            "nw_waste_code": "20234",
            "nw_lifecycle_stage": "pre-treatment",
        },
    )
    LOGGER.info("Nuclear Item Asset Created (Identity=%s)", item.asset["identity"])

    # Container Asset
    LOGGER.info("Creating Container Asset...")
    container = Nuclear(arch)
    serial_num = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    conname = 'Container-' + serial_num

    container.concreate(
        conname,
        "Container Item demo creation",
        attachments=[upload_attachment(arch, "container.jpeg", "arc_primary_image")],
        custom_attrs={
            "nw_waste_code": "20234",
            "nw_lifecycle_stage": "pre-buffer",
        },
    )
    LOGGER.info("Container Item Asset Created (Identity=%s)", container.asset["identity"])

    # Characterize
    LOGGER.info("Adding characterization...")
    item.characterize(
        {
            "name": itemname,
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

    # Package
    LOGGER.info("Adding packaging...")
    item.package(
        {
            "description": "Packaged in " + container.asset["attributes"]["arc_display_name"],
            "nw_in_container": container.asset["identity"],
            "nw_lifecycle_stage": "packaged",
        }
    )
    LOGGER.info("Packaging registered...")

    # Buffer
    LOGGER.info("Adding buffering...")
    container.buffer(
        {
            "description": "Moved to " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "bufferstorage",
            "evidence": "No evidence provided",
        }
    )
    item.buffer(
        {
            "description": "Buffer storage " + container.asset["attributes"]["arc_display_name"],
            "evidence": "See buffer event for " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "bufferstorage",
        }
    )
    LOGGER.info("Buffer registered...")

    # Treat
    LOGGER.info("Adding treatment...")
    container.treat(
        {
            "description": "Treated " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "treated",
            "nw_waste_inventory": item.asset["identity"],
        }
    )
    LOGGER.info("Treatment registered...")

    # Condition
    LOGGER.info("Adding conditioning...")
    container.condition(
        {
            "description": "Conditioned " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "conditioned",
            "nw_waste_code": "20234",
        }
    )
    LOGGER.info("Conditioning registered...")

    # Iterim Storage
    LOGGER.info("Adding iterim storage...")
    container.iterim(
        {
            "description": "Iterim Storage " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "iterimstorage",
            "evidence": "No evidence provided"
        }
    )
    item.iterim(
        {
            "description": "Iterim storage " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "interimstorage",
            "evidence": "Interimstorage event " + container.asset["attributes"]["arc_display_name"],
        }
    )
    LOGGER.info("Iterim Storage registered...")

    # Sentence Container
    LOGGER.info("Adding sentencing...")
    container.sentence(
        {
            "description": "Sentenced " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "sentenced",
            "nw_waste_stream": "stream",
            "evidence": "No evidence provided",
        }
    )
    item.sentence(
        {
            "description": "Waste stream " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "sentenced",
            "nw_waste_stream": "stream",
            "evidence": "Sentence event " + container.asset["attributes"]["arc_display_name"],
        }
    )
    LOGGER.info("Sentencing registered...")

    # Commit Container
    LOGGER.info("Adding commit...")
    container.commit(
        {
            "description": "Committed " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "commit",
            "evidence": "No evidence provided",
        }
    )
    item.commit(
        {
            "description": "Commited item to " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "commit",
            "evidence": "See commit event for " + container.asset["attributes"]["arc_display_name"],
        }
    )
    LOGGER.info("Commit registered...")

    # Transport Container
    LOGGER.info("Adding transport...")
    container.transport(
        {
            "description": "Transport " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "final_transport",
            "evidence": "No evidence provided"
        }
    )
    item.transport(
        {
            "description": "Transport in " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "final_transport",
            "evidence": "Transport event " + container.asset["attributes"]["arc_display_name"],
        }
    )
    LOGGER.info("Transport registered...")

    # Accept Container
    LOGGER.info("Adding acceptance...")
    container.accept(
        {
            "description": container.asset["attributes"]["arc_display_name"] + " accepted",
            "nw_lifecycle_stage": "disposed",
            "evidence": "No evidence provided",
        }
    )
    item.accept(
        {
            "description": "Disposed item in " + container.asset["attributes"]["arc_display_name"],
            "nw_lifecycle_stage": "disposed",
            "evidence": "See accept event for " + container.asset["attributes"]["arc_display_name"],
        }
    )
    LOGGER.info("Acceptance registered...")
