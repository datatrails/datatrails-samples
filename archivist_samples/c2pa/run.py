#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring
# pylint:  disable=too-many-statements

import logging

from sys import exit as sys_exit
from archivist import about

from .c2pa import C2PADocument, upload_attachment
from ..testing.assets import AttachmentDescription

LOGGER = logging.getLogger(__name__)


def run(arch, args):
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # remove the trailing / on the url if it exists
    url = args.url
    if url.endswith("/"):
        url = url[:-1]

    LOGGER.info("Creating C2PA Asset ...")
    c2pa_document = C2PADocument(arch, "C2PA")

    c2pa_document.create(
        "Adobe C2PA Image",
        "Adobe C2PA Image",
        "hou3dpw07k3t",
        custom_attrs={
            "arc_primary_image": upload_attachment(
                arch,
                AttachmentDescription("image.jpg", "arc_primary_image"),
            ),
            "document_hash_value": (
                "f999fd78bfe8a83c96e468a078830ba94485bc1bc6fd086fb94a43bd29dd0f23"
            ),
            "document_hash_alg": "sha256",
            "document_version": "1.0.0",
            "document_document": upload_attachment(
                arch,
                AttachmentDescription(
                    "image.jpg",
                    "C2PA Image",
                ),
            ),
        },
    )

    if c2pa_document.existed:
        LOGGER.info(
            "C2PA Document %s already exists (Identity=%s)",
            "C2PA Image",
            c2pa_document.asset["identity"],
        )
        sys_exit(0)

    LOGGER.info("C2PA Document Created (Identity=%s)", c2pa_document.asset["identity"])

    LOGGER.info("Creating Info Report ...")
    # info report
    c2pa_document.info_report(
        document=upload_attachment(
            arch, AttachmentDescription("info.txt", "Info Report")
        )
    )
    LOGGER.info("Info Report Created")

    LOGGER.info("Creating Ingredients ...")
    # ingredients
    c2pa_document.ingredients(
        document=upload_attachment(
            arch, AttachmentDescription("ingredient.json", "Ingredients")
        )
    )
    LOGGER.info("Ingredients Created")

    LOGGER.info("Creating External Manifest ...")
    # external manifest
    c2pa_document.external_manifest(
        definition=upload_attachment(
            arch, AttachmentDescription("signed_image.c2pa", "Signed Definition")
        ),
        signed_image=upload_attachment(
            arch, AttachmentDescription("signed_image.jpg", "Signed Image")
        ),
    )

    LOGGER.info("External Manifest Created")

    LOGGER.info("Publishing V1.1.M ...")
    c2pa_document.publish(
        document=upload_attachment(
            arch,
            AttachmentDescription("signed_image.c2pa", "Signed Definition"),
        ),
        authors=[
            {"display_name": "Zorro", "email": "zorro@example.com"},
        ],
        description="Publishing External Manifest",
        doc_hash="4c4e615eef9cce37d3754ca58d4bcf9bb4362bf64cd91224bffaea1c55b38ad7",
        version="1.1.M",
        name="Adobe C2PA Image",
    )
    LOGGER.info("V1.1.M published")

    LOGGER.info("Creating Details Report ...")
    # external manifest
    c2pa_document.details_report(
        detailed=upload_attachment(
            arch, AttachmentDescription("detailed.json", "Detailed Report")
        ),
        manifest_store=upload_attachment(
            arch, AttachmentDescription("manifest_store.json", "Manifest Report")
        ),
    )

    LOGGER.info("Details Report Created")

    LOGGER.info("Creating Parent File ...")
    # parent
    c2pa_document.parent(
        parent_definition=upload_attachment(
            arch, AttachmentDescription("parent_signed_image.c2pa", "Parent Definition")
        ),
        signed_image=upload_attachment(
            arch, AttachmentDescription("signed_image.jpg", "Parent Image")
        ),
    )

    LOGGER.info("Parent File Created")

    LOGGER.info("Publishing V1.2.PM ...")
    c2pa_document.publish(
        document=upload_attachment(
            arch,
            AttachmentDescription("parent_signed_image.c2pa", "Parent Definition"),
        ),
        description="Publishing Parent File.",
        authors=[
            {"display_name": "Don Diego", "email": "dondiego@example.com"},
        ],
        doc_hash="b0a73726a72f00346048ee4c89bb0b214469025757a1f70b890c68f71429ea72",
        version="1.2.PM",
        name="Adobe C2PA Image",
    )
    LOGGER.info("V1.2.PM published")

    LOGGER.info("Creating Edited Manifest ...")
    # edited manifest
    c2pa_document.edit_manifest(
        description="Removing Data From Manifest",
        edited_manifest=upload_attachment(
            arch,
            AttachmentDescription("edited_signed_image.c2pa", "Edited Definition"),
        ),
    )

    LOGGER.info("edited Manifest Created")

    LOGGER.info("Publishing V1.3.ME ...")
    c2pa_document.publish(
        document=upload_attachment(
            arch,
            AttachmentDescription("edited_signed_image.c2pa", "Edited Definition"),
        ),
        description="Publishing Edited Manifest.",
        authors=[
            {"display_name": "Don Diego", "email": "dondiego@example.com"},
        ],
        doc_hash="637535f55d2db76cd44b7a98fff2032b711fe8ddbc65ce92a02848c65a57cf04",
        version="1.3.ME",
        name="Adobe C2PA Image",
        custom_attrs={
            "OnboardingFinalEventMarker": "true",
        },
    )
    LOGGER.info("V1.3.ME published")
