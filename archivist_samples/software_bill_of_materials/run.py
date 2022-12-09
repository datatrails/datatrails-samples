#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

import logging
from sys import exit as sys_exit

from archivist import about

from .software_package import SoftwarePackage

LOGGER = logging.getLogger(__name__)


def run(arch, args):

    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # SoftwarePackage class encapsulates SBOM object in RKVST
    package_name = "ACME Detector Coyote SP1"
    LOGGER.info("Creating Software Package Asset...: %s", package_name)
    package = SoftwarePackage(arch)

    package.create(
        package_name,
        "Different box, same great taste!",
        custom_attrs={
            "sbom_license": "www.gnu.org/licenses/gpl.txt",
            "proprietary_secret": "For your eyes only",
        },
        attachments=[("Comp_2.jpeg", "arc_primary_image")],
    )
    if package.existed:
        LOGGER.info("Software Package already Created: %s", package_name)
        sys_exit(0)

    LOGGER.info("Software Package Created (Identity=%s)", package.asset["identity"])

    LOGGER.info("1 Making a release...")
    package.release(
        {
            "name": package_name,
            "description": "v4.1.5 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.5",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0",
        },
        attachments=[("v4_1_5_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    LOGGER.info("2 Making a release...")
    package.release(
        {
            "name": package_name,
            "description": "v4.1.6 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.6",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-0",
        },
        attachments=[("v4_1_6_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    LOGGER.info("3 Making a private patch...")
    package.private_patch(
        {
            "name": package_name,
            "private_id": "special_customer",
            "target_component": "rrdetector",
            "target_version": "v1.4.6",
            "description": "Private patch to v4.1.6 for limited customer set",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-1",
            "reference": "CVE-20210613-1",
        },
        attachments=[("v4_1_6_1_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Private patch registered.")

    LOGGER.info("4 Making a release...")
    package.release(
        {
            "name": package_name,
            "description": "v4.1.7 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.7",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-7-0",
        },
        attachments=[("v4_1_7_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")

    LOGGER.info("5 Plan major upgrade...")
    package.release_plan(
        {
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
        },
        attachments=[("v5_0_0_sbom.xml", "SWID SBOM")],
    )

    LOGGER.info("6 Approve major upgrade...")
    package.release_accepted(
        {
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
            "approver": "Yosemite Sam",
        },
        attachments=[("v5_0_0_sbom.xml", "SWID SBOM")],
    )

    LOGGER.info("7 Release major upgrade...")
    package.release(
        {
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v5-0-0-0",
        },
        attachments=[("v5_0_0_sbom.xml", "SWID SBOM")],
    )
    LOGGER.info("Release registered.")
    sys_exit(0)
