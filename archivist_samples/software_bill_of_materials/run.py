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
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import logging

from archivist import about

from . import sbom_files

from .software_package import SoftwarePackage

LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, path, name):
    with pkg_resources.open_binary(sbom_files, path) as fd:
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

    # SoftwarePackage class encapsulates SBOM object in RKVST
    LOGGER.info("Creating Software Package Asset...")
    package = SoftwarePackage(arch)

    package.create(
        "ACME Roadrunner Detector 2013 Coyote Edition SP1",
        "Different box, same great taste!",
        attachments=[upload_attachment(arch , "Comp_2.jpeg", "arc_primary_image")],
        custom_attrs={
            "sbom_license": "www.gnu.org/licenses/gpl.txt",
            "proprietary_secret": "For your eyes only",
        },
    )
    LOGGER.info("Software Package Created (Identity=%s)", package.asset["identity"])

    # Make a release
    LOGGER.info("Making a release...")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.5 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.5",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0",
        },
        attachments=[upload_attachment(arch , "v4_1_5_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    # Make a release
    LOGGER.info("Making a release...")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.6 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.6",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-0",
        },
        attachments=[upload_attachment(arch , "v4_1_6_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    # Private patch
    LOGGER.info("Making a private patch...")
    package.private_patch(
        {
            "private_id": "special_customer",
            "target_component": "rrdetector",
            "target_version": "v1.4.6",
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "Private patch to v4.1.6 for limited customer set",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-1",
            "reference": "CVE-20210613-1",
        },
        attachments=[upload_attachment(arch , "v4_1_6_1_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Private patch registered.")

    # Make a release
    LOGGER.info("Making a release...")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.7 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.7",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-7-0",
        },
        attachments=[upload_attachment(arch , "v4_1_7_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    # Plan major upgrade
    package.release_plan(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
        },
        attachments=[upload_attachment(arch , "v5_0_0_sbom.xml", "SWID SBOM")],
    )

    # Approve major upgrade
    package.release_accepted(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
            "approver": "Yosemite Sam",
        },
        attachments=[upload_attachment(arch , "v5_0_0_sbom.xml", "SWID SBOM")],
    )

    # Release major upgrade
    LOGGER.info("Making a release...")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v5-0-0-0",
        },
        attachments=[upload_attachment(arch , "v5_0_0_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")
