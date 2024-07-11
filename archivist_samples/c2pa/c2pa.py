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

from . import c2pa_files
from ..testing.assets import make_assets_create, AttachmentDescription

if TYPE_CHECKING:
    from ..archivist import Archivist

LOGGER = logging.getLogger(__name__)


def upload_attachment(arch, attachment_description: AttachmentDescription):
    with res.files(c2pa_files).joinpath(attachment_description.filename).open(
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
    with res.files(c2pa_files).joinpath(attachment_description.filename).open(
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


class C2PADocument:
    selector_key = "OnboardingSampleID"
    selector_value = "C2PA"

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
        identity: str,
        *,
        attachments: "list|None" = None,
        custom_attrs: "dict|None" = None,
    ):
        attrs = {
            "arc_description": description,
            "arc_profile": "Document",
            "id": identity,
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
    #
    # authors is a list in the form {'display_name': 'Bob', 'email':'Bob@example.com'}
    #
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

    # info_report
    def info_report(self, document: dict):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Info Report",
            "arc_description": "Information List",
            "info_report": document,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # ingredients
    #
    # we are using a premade ingredients list
    # it was created using the c2patool https://github.com/contentauth/c2patool
    # using the following command:
    #
    # $> c2patool c2pa_files/signed_{image} --ingredient --force --output ./ingredient
    def ingredients(self, document: dict):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Ingredients",
            "arc_description": "Ingredients List",
            "ingredient_list": document,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # external_manifest
    #
    # we are using a premade external manifest for 'definition' and 'signed_image'
    # it was created using the c2patool https://github.com/contentauth/c2patool
    # using the following command:
    #
    # $> c2patool cp2a_files/{image} -m c2pa_files/{definition} -f -o c2pa_files/signed_{image}
    #
    # definition = represents the json file used to create the manifest
    # signed_image = represents the output file that contains the manifest
    def external_manifest(self, definition: dict, signed_image: dict):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "External Manifest",
            "arc_description": "Generated External Manifest",
            "c2pa_signed": definition,
            "signed_image": signed_image,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # details_report
    #
    # we are using a premade detailed manifest report for 'detailed' and 'manifest_store'
    # it was created using the c2patool https://github.com/contentauth/c2patool
    # using the following command:
    #
    # $> c2patool cp2a_files/signed_{image} -d --force --output ./c2pa_files
    #
    # detailed = represents info about the format of c2pa file
    # manifest_store = represents  the manifest(s) info related to the signed image file
    def details_report(self, detailed: dict, manifest_store: dict):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Details Report",
            "arc_description": "Generated Details Report",
            "detail_report": detailed,
            "manifest_report": manifest_store,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # parent
    #
    # we are using a premade parent manifest for 'parent_definition' and 'signed_image'
    # it was created using the c2patool https://github.com/contentauth/c2patool
    # using the following command:
    #
    # $> c2patool c2pa_files/{image} -m c2pa_files/{definition} -p ./ingredient -f \
    #    -o c2pa_files/signed_{image}
    #
    # parent_defintion = represents the output file that contains the manifest
    # signed_image = the signed parent image
    def parent(self, parent_definition: dict, signed_image: dict):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Parent File",
            "arc_description": "Generating Parent File",
            "parent_image": signed_image,
            "parentc2pa_signed": parent_definition,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # edit_manifest
    #
    # uses a premade edited manifest for `edited_manifest`
    def edit_manifest(
        self,
        description: str,
        edited_manifest: dict,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "Manifest Edit",
            "arc_description": description,
            "edited_signed_image": edited_manifest,
        }

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )
