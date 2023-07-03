#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

import logging
from sys import exit as sys_exit

from archivist import about

from .software_package import SoftwarePackageDocument, attachment_create
from ..testing.assets import AttachmentDescription

LOGGER = logging.getLogger(__name__)


def run(arch, args):
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # SoftwarePackage class encapsulates SBOM object in RKVST
    package_name = "ACME Detector Coyote SP1"
    LOGGER.info("Creating Software Package Asset...: %s", package_name)
    package = SoftwarePackageDocument(arch)

    package.create(
        package_name,
        "Software release history for ACME Roadrunner Detector 2013 Coyote Edition SP1",
        custom_attrs={
            "sbom_license": "www.gnu.org/licenses/gpl.txt",
            "document_hash_value": (
                "75c5579badc3a77b4941deee620ae4ed4e7d4ce853b0cf7f08608e399bff1571"
            ),
            "document_hash_alg": "sha256",
            "document_version": "v4.1.5",
            "document_document": attachment_create(
                arch, AttachmentDescription("v4_1_5_sbom.xml", "SWID SBOM")
            ),
            "sbom_author": "The ACME Corporation",
            "sbom_supplier": "Coyote Services, Inc.",
            "sbom_uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0",
        },
        attachments=[AttachmentDescription("Comp_2.jpeg", "arc_primary_image")],
    )

    if package.existed:
        LOGGER.info("Software Package already Created: %s", package_name)
        sys_exit(0)

    LOGGER.info("Software Package Created (Identity=%s)", package.asset["identity"])

    LOGGER.info("1 Making a release...")
    package.publish(
        document=attachment_create(
            arch, AttachmentDescription("v4_1_6_sbom.xml", "SWID SBOM")
        ),
        sbom={
            "name": package_name,
            "description": "v4.1.6 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "55ac16bf4f8099d87084c33d14ca49917d08d624c59186d762705acb91b9de3e",
            "version": "v4.1.6",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-0",
        },
    )
    LOGGER.info("Release registered.")

    LOGGER.info("2 Making a release...")
    package.publish(
        document=attachment_create(
            arch, AttachmentDescription("v4_1_7_sbom.xml", "SWID SBOM")
        ),
        sbom={
            "name": package_name,
            "description": "v4.1.7 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "65218dd26b9f89992d0931f925cfac6f96f7722d8ba0317cc4e8061bc497b279",
            "version": "v4.1.7",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-7-0",
        },
    )
    LOGGER.info("Release registered.")

    LOGGER.info("3 Plan major upgrade...")
    package.release_plan(
        {
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
        },
        attachments=[AttachmentDescription("v5_0_0_sbom.xml", "SWID SBOM")],
    )

    LOGGER.info("4 Approve major upgrade...")
    package.release_accepted(
        {
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
        },
        attachments=[AttachmentDescription("v5_0_0_sbom.xml", "SWID SBOM")],
    )

    LOGGER.info("5 Release major upgrade...")
    package.publish(
        document=attachment_create(
            arch, AttachmentDescription("v5_0_0_sbom.xml", "SWID SBOM")
        ),
        sbom={
            "name": package_name,
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "5ecf83857f0ae1986dc793edc9110f04ee324d228b1ed90259460f565936a3aa",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v5-0-0-0",
        },
    )
    LOGGER.info("Release registered.")
    sys_exit(0)
