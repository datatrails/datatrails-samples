#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring
# pylint:  disable=too-many-statements

import logging

from archivist import about

from .document import Document, upload_attachment
from ..testing.assets import AttachmentDescription

LOGGER = logging.getLogger(__name__)


def run(arch, args):
    """
    runs the sample and returns the system error code.
    """
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # remove the trailing / on the url if it exists
    url = args.url
    if url.endswith("/"):
        url = url[:-1]

    LOGGER.info("Creating Document Asset ...")
    document = Document(arch, "Invoice")

    document.create(
        "Asteroid Mining Inc Invoice",
        "Invoice for the purchase of an asteroid mining space ship",
        custom_attrs={
            "arc_primary_image": upload_attachment(
                arch,
                AttachmentDescription("DocumentPrimaryImage.jpg", "arc_primary_image"),
            ),
            "document_hash_value": (
                "aa914e5c64a0671de5c5f21c76ca3734004dd62c006b1644370a64200ca233aa"
            ),
            "document_hash_alg": "sha256",
            "document_version": "V1",
            "document_document": upload_attachment(
                arch,
                AttachmentDescription(
                    "AsteroidMiningIncOriginalInvoice.pdf",
                    "Asteroid Mining Inc Invoice",
                ),
            ),
        },
    )

    if document.existed:
        LOGGER.info(
            "Document Asset %s already exists (Identity=%s)",
            "Asteroid Mining Inc Invoice",
            document.asset["identity"],
        )
        LOGGER.info(
            "Public URL: %s/archivist/public%s", args.url, document.asset["identity"]
        )

        return 0

    LOGGER.info("Invoice Asset Created (Identity=%s)", document.asset["identity"])

    LOGGER.info("Publishing V2 ...")
    document.publish(
        document=upload_attachment(
            arch,
            AttachmentDescription(
                "AsteroidMiningIncOrderNumber.pdf", "Asteroid Mining Inc Invoice"
            ),
        ),
        authors=[
            {"display_name": "Frankie Jupiter", "email": "frankiejupiter@example.com"},
            {"display_name": "Jennie Titan", "email": "jennietitan@example.com"},
        ],
        description="Added order number.",
        doc_hash="a9a154fb3fb54edd74c17b60b9efd3b7cf35fbcc15026f473a56d1add2dafa36",
        version="V2",
        name="Asteroid Mining Inc Invoice",
    )
    LOGGER.info("V2 published, with order number")

    LOGGER.info("Publishing V3 ...")
    document.publish(
        document=upload_attachment(
            arch,
            AttachmentDescription(
                "AsteroidMiningIncDiscount.pdf", "Asteroid Mining Inc Invoice"
            ),
        ),
        description="Applied agreed discount.",
        authors=[
            {"display_name": "Frankie Jupiter", "email": "frankiejupiter@example.com"},
            {"display_name": "Cassie Oort", "email": "cassieoort@example.com"},
        ],
        doc_hash="84ffc357a12491f7313b25cfdec0efb97929c87b411ef28586e62d7330c8cd77",
        version="V3",
        name="Asteroid Mining Inc Invoice",
        custom_attrs={
            "OnboardingFinalEventMarker": "true",
        },
    )
    LOGGER.info("V3 published, with discount applied")

    return 0
