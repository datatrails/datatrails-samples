# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings
# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

try:
    # Python < 3.9
    import importlib_resources as res
except ImportError:
    import importlib.resources as res

import logging
from sys import exit as sys_exit
from typing import List, Optional

from .. import archivist as type_helper

from ..testing.assets import make_assets_create, AttachmentDescription

from . import sbom_files


LOGGER = logging.getLogger(__name__)


def attachment_create(arch, attachment_description: AttachmentDescription):
    LOGGER.info("sbom attachment creator: %s", attachment_description.filename)
    with res.files(sbom_files).joinpath(attachment_description.filename).open(
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


sboms_creator = make_assets_create(attachment_creator=attachment_create)


class SoftwarePackageDocument:
    selector_key = "OnboardingSampleID"
    selector_value = "SBOM"

    def __init__(self, arch: "type_helper.Archivist"):
        self._arch = arch
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

    # Asset Creation
    def create(
        self,
        sbom_name: str,
        sbom_description: str,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        attrs = {
            "arc_description": sbom_description,
            "arc_profile": "Document",
            "arc_display_type": "Software Package",
        }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        self._asset, self._existed = sboms_creator(
            self._arch,
            sbom_name,
            attrs,
            attachments=attachments,
            selector_key=self.selector_key,
            selector_value=self.selector_value,
        )
        return self._asset

    # Asset load by unique identity
    def read(
        self,
        identity: str,
    ):
        self._asset = self.arch.assets.read(identity)

    # Asset load by attribute(s)
    def read_by_signature(
        self,
        attributes: Optional[dict],
    ):
        # Hard-wire the Asset type
        newattrs = attributes.copy()
        newattrs["arc_display_type"] = "Software Package"

        # Note: underlying Archivist will raise ArchivistNotFoundError or
        # ArchivistDuplicateError unless this set of attributes points to
        # a single unique asset
        self._asset = self.arch.assets.read_by_signature(attrs=newattrs)

    # Release Events
    def publish(
        self,
        document: dict,
        sbom: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        latest_sbom: Optional[dict] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):
        # sbom_name: str,
        # sbom_description: str,
        # sbom_hash: str,
        # sbom_version: str,
        # sbom_author: str,
        # sbom_supplier: str,
        # sbom_uuid: str,

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }

        if latest_sbom is None:
            latest_sbom = sbom

        author_email = f"{sbom['author']}.com"
        attrs = {
            "arc_description": sbom["description"],
            "arc_evidence": "Release",
            "arc_display_type": "Publish",
            "sbom_component": sbom["name"],
            "sbom_hash": sbom["hash"],
            "sbom_version": sbom["version"],
            "sbom_author": sbom["author"],
            "sbom_supplier": sbom["supplier"],
            "sbom_uuid": sbom["uuid"],
            "document_version_authors": [
                {"display_name": sbom["author"], "email": author_email}
            ],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "arc_display_name": latest_sbom["name"],
            "document_document": document,
            "document_hash_value": latest_sbom["hash"],
            "document_hash_alg": "sha256",
            "document_version": latest_sbom["version"],
            "document_status": "Published",
            "sbom_component": latest_sbom["name"],
            "sbom_version": latest_sbom["version"],
            "sbom_author": latest_sbom["author"],
            "sbom_hash": latest_sbom["hash"],
            "sbom_supplier": latest_sbom["supplier"],
            "sbom_uuid": latest_sbom["uuid"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
        )

    def release_plan(
        self,
        sbom_planned: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_planned["description"],
            "arc_evidence": "Release Plan",
            "arc_display_type": "Release Plan",
            "sbom_planned_date": sbom_planned["date"],
            "sbom_planned_component": sbom_planned["name"],
            "sbom_planned_version": sbom_planned["version"],
            "sbom_planned_reference": sbom_planned["reference"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    def release_accepted(
        self,
        sbom_accepted: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_accepted["description"],
            "arc_evidence": "Release Accepted",
            "arc_display_type": "Release Accepted",
            "sbom_accepted_date": sbom_accepted["date"],
            "sbom_accepted_component": sbom_accepted["name"],
            "sbom_accepted_version": sbom_accepted["version"],
            "sbom_accepted_vuln_reference": sbom_accepted["reference"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    # Patch Events
    def patch(
        self,
        sbom_patch: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_patch["description"],
            "arc_evidence": "Patch",
            "arc_display_type": "Patch",
            "sbom_patch_component": sbom_patch["target_component"],
            "sbom_patch_hash": sbom_patch["hash"],
            "sbom_patch_target_version": sbom_patch["target_version"],
            "sbom_patch_author": sbom_patch["author"],
            "sbom_patch_supplier": sbom_patch["supplier"],
            "sbom_patch_uuid": sbom_patch["uuid"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    def private_patch(
        self,
        sbom_patch: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_patch["description"],
            "arc_evidence": sbom_patch["private_id"] + "_Patch",
            "arc_display_type": sbom_patch["private_id"] + "_Patch",
            "sbom_patch_component": sbom_patch["target_component"],
            "sbom_patch_hash": sbom_patch["hash"],
            "sbom_patch_version": sbom_patch["target_version"],
            "sbom_patch_author": sbom_patch["author"],
            "sbom_patch_supplier": sbom_patch["supplier"],
            "sbom_patch_uuid": sbom_patch["uuid"],
            "sbom_patch_vuln_reference": sbom_patch["reference"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    # Vulnerability Events
    def vuln_disclosure(
        self,
        vuln: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict],
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": vuln["description"],
            "arc_evidence": "Vulnerability Disclosure",
            "arc_display_type": "Vulnerability Disclosure",
            "vuln_name": vuln["name"],
            "vuln_reference": vuln["reference"],
            "vuln_id": vuln["id"],
            "vuln_category": vuln["category"],
            "vuln_severity": vuln["severity"],
            "vuln_status": vuln["status"],
            "vuln_author": vuln["author"],
            "vuln_target_component": vuln["target_component"],
            "vuln_target_version": vuln["target_version"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    def vuln_update(
        self,
        vuln: dict,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": vuln["description"],
            "arc_evidence": "Vulnerability Update",
            "arc_display_type": "Vulnerability Update",
            "vuln_name": vuln["name"],
            "vuln_reference": vuln["reference"],
            "vuln_id": vuln["id"],
            "vuln_category": vuln["category"],
            "vuln_severity": vuln["severity"],
            "vuln_status": vuln["status"],
            "vuln_author": vuln["author"],
            "vuln_target_component": vuln["target_component"],
            "vuln_target_version": vuln["target_version"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )

    # EOL/Deprecation
    def deprecation(
        self,
        sbom_eol: dict,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        custom_attrs: Optional[dict] = None,
    ):
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }

        attrs = {
            "arc_description": sbom_eol["description"],
            "arc_evidence": "Deprecation",
            "arc_display_type": "Deprecation",
            "sbom_eol_target_component": sbom_eol["target_component"],
            "sbom_eol_target_version": sbom_eol["target_version"],
            "sbom_eol_target_uuid": sbom_eol["target_uuid"],
            "sbom_eol_target_date": sbom_eol["target_date"],
        }
        if attachments:
            for attachment in attachments:
                attrs[attachment.attribute_name] = attachment_create(
                    self.arch, attachment
                )

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
        )
