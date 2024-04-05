# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings

try:
    # Python < 3.9
    import importlib_resources as res
except ImportError:
    import importlib.resources as res

import logging

from copy import copy

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from typing import TYPE_CHECKING

from . import document_files
from ..testing.assets import make_assets_create, AttachmentDescription

if TYPE_CHECKING:
    from archivist.archivist import Archivist

LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, attachment_description: AttachmentDescription):
    with res.files(document_files).joinpath(attachment_description.filename).open(
        "rb"
    ) as fd:
        blob = arch.attachments.upload(fd)
        attachment = {
            # sample-specific attr to relay attachment name
            "datatrails_samples_display_name": attachment_description.attribute_name,
            "arc_file_name": attachment_description.filename,
            "arc_attribute_type": "arc_attachment",
            "arc_blob_identity": blob["identity"],
            "arc_blob_hash_alg": blob["hash"]["alg"],
            "arc_blob_hash_value": blob["hash"]["value"],
        }
        return attachment


def attachment_create(arch, attachment_description: AttachmentDescription):
    with res.files(document_files).joinpath(attachment_description.filename).open(
        "rb"
    ) as fd:
        attachment = arch.attachments.upload(fd)
        result = {
            "arc_attribute_type": "arc_attachment",
            "arc_blob_identity": attachment["identity"],
            "arc_blob_hash_alg": attachment["hash"]["alg"],
            "arc_blob_hash_value": attachment["hash"]["value"],
            "arc_display_name": attachment_description.attribute_name,
            "arc_file_name": attachment_description.filename,
        }

        return result


document_creator = make_assets_create(
    attachment_creator=attachment_create, confirm=True
)


class Document:
    selector_key = "OnboardingSampleID"
    selector_value = "DocumentLineage"

    def __init__(
        self,
        arch: "Archivist",
        display_type: str,
    ):
        arch_ = copy(arch)
        arch_.fixtures = {
            "assets": {
                "attributes": {
                    "arc_display_type": display_type,
                },
            },
        }

        self._arch = arch_
        self._asset = None
        self._existed = False

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset

    @property
    def existed(self):
        return self._existed

    def create(
        self,
        name: str,
        description: str,
        *,
        attachments: "list|None" = None,
        custom_attrs: "dict|None" = None,
    ):
        attrs = {
            "arc_description": description,
            "arc_profile": "Document",
        }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        self._asset, self._existed = document_creator(
            self.arch,
            name,
            attrs,
            attachments=attachments,
            selector_key=self.selector_key,
            selector_value=self.selector_value,
        )

        return self._asset

    # Publish new version of the document
    # pylint: disable=too-many-arguments
    def publish(
        self,
        document: dict,
        version: str,
        description: str,
        doc_hash: str,
        authors: "list[dict]",
        name: str,
        custom_attrs: "dict|None" = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Publish",
            "arc_description": description,
            "document_version_authors": authors,
        }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "arc_display_name": name,
            "document_document": document,
            "document_hash_value": doc_hash,
            "document_hash_alg": "sha256",
            "document_version": version,
            "document_status": "Published",
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Withdraw version of the document
    def withdraw(self, document: dict, version: str, doc_hash: str, name: str):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {"arc_display_type": "Withdraw", "document_status": "Withdrawn"}

        asset_attrs = {
            "arc_display_name": name,
            "document_document": document,
            "document_hash_value": doc_hash,
            "document_version": version,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )
