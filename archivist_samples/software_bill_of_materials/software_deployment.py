# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings
from typing import Optional

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from archivist import archivist as type_helper

from .software_package import sboms_creator


class SoftwareDeployment:
    def __init__(
        self,
        arch: "type_helper.Archivist",
    ):
        self._arch = arch
        self._asset = None
        self._attachments = None
        self._environment = None

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset

    @property
    def attachments(self):
        return self._attachments

    @property
    def environment(self):
        return self._environment

    # Create Software Deployment

    def create(
        self,
        sbom_name: str,
        sbom_description: str,
        *,
        sbom_environment: Optional[str],
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        if sbom_environment is not None:
            self._environment = sbom_environment
        else:
            sbom_environment = self._environment

        attrs = {
            "arc_description": sbom_description,
            "arc_display_type": "Software Deployment",
            "sbom_environment": sbom_environment,
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        self._asset = sboms_creator(
            self.arch,
            sbom_name,
            attrs,
            attachments=attachments,
        )
        return self._asset

    # Installation Event
    def installation(
        self,
        sbom_installation: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        if sbom_installation["environment"] is not None:
            self._environment = sbom_installation["environment"]
        else:
            sbom_installation["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_installation["description"],
            "arc_evidence": "Installation",
            "arc_display_type": "Installation",
            "sbom_installation_component": sbom_installation["name"],
            "sbom_installation_hash": sbom_installation["hash"],
            "sbom_installation_version": sbom_installation["version"],
            "sbom_installation_author": sbom_installation["author"],
            "sbom_installation_supplier": sbom_installation["supplier"],
            "sbom_installation_uuid": sbom_installation["uuid"],
            "sbom_installation_environment": sbom_installation["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_installation["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        asset_attrs = {
            "sbom_component": sbom_installation["name"],
            "sbom_hash": sbom_installation["hash"],
            "sbom_version": sbom_installation["version"],
            "sbom_author": sbom_installation["author"],
            "sbom_supplier": sbom_installation["supplier"],
            "sbom_uuid": sbom_installation["uuid"],
            "sbom_environment": sbom_installation["environment"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    def decommission(
        self,
        sbom_decomission: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        if sbom_decomission["environment"] is not None:
            self._environment = sbom_decomission["environment"]
        else:
            sbom_decomission["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_decomission["description"],
            "arc_evidence": "Decomission",
            "arc_display_type": "Decomission",
            "sbom_decomission_component": sbom_decomission["name"],
            "sbom_decomission_version": sbom_decomission["version"],
            "sbom_decomission_author": sbom_decomission["author"],
            "sbom_decomission_supplier": sbom_decomission["supplier"],
            "sbom_decomission_uuid": sbom_decomission["uuid"],
            "sbom_decomission_target_date": sbom_decomission["target_date"],
            "sbom_decomission_status": sbom_decomission["status"],
            "sbom_decomission_environment": sbom_decomission["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_decomission["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        asset_attrs = {
            "sbom_decomission_target_date": sbom_decomission["target_date"],
            "sbom_decomission_status": sbom_decomission["status"],
            "sbom_environment": sbom_decomission["environment"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, asset_attrs=asset_attrs
        )

    # Upgrade Events
    def upgrade(
        self,
        sbom_upgrade: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        if sbom_upgrade["environment"] is not None:
            self._environment = sbom_upgrade["environment"]
        else:
            sbom_upgrade["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_upgrade["description"],
            "arc_evidence": "Upgrade",
            "arc_display_type": "Upgrade",
            "sbom_upgrade_component": sbom_upgrade["name"],
            "sbom_upgrade_hash": sbom_upgrade["hash"],
            "sbom_upgrade_version": sbom_upgrade["version"],
            "sbom_upgrade_author": sbom_upgrade["author"],
            "sbom_upgrade_supplier": sbom_upgrade["supplier"],
            "sbom_upgrade_uuid": sbom_upgrade["uuid"],
            "sbom_upgrade_environment": sbom_upgrade["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_upgrade["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        asset_attrs = {
            "sbom_component": sbom_upgrade["name"],
            "sbom_hash": sbom_upgrade["hash"],
            "sbom_version": sbom_upgrade["version"],
            "sbom_author": sbom_upgrade["author"],
            "sbom_supplier": sbom_upgrade["supplier"],
            "sbom_uuid": sbom_upgrade["uuid"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    def upgrade_plan(
        self,
        sbom_planned: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        if sbom_planned["environment"] is not None:
            self._environment = sbom_planned["environment"]
        else:
            sbom_planned["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_planned["description"],
            "arc_evidence": "Upgrade Plan",
            "arc_display_type": "Upgrade Plan",
            "sbom_planned_date": sbom_planned["date"],
            "sbom_planned_captain": sbom_planned["captain"],
            "sbom_planned_component": sbom_planned["name"],
            "sbom_planned_version": sbom_planned["version"],
            "sbom_planned_reference": sbom_planned["reference"],
            "sbom_planned_environment": sbom_planned["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_planned["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def upgrade_accepted(
        self,
        sbom_accepted: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        if sbom_accepted["environment"] is not None:
            self._environment = sbom_accepted["environment"]
        else:
            sbom_accepted["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_accepted["description"],
            "arc_evidence": "Upgrade Accepted",
            "arc_display_type": "Upgrade Accepted",
            "sbom_accepted_date": sbom_accepted["date"],
            "sbom_accepted_captain": sbom_accepted["captain"],
            "sbom_accepted_component": sbom_accepted["name"],
            "sbom_accepted_version": sbom_accepted["version"],
            "sbom_accepted_reference": sbom_accepted["reference"],
            "sbom_accepted_environment": sbom_accepted["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_accepted["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    # Rollback Events
    def rollback(
        self,
        sbom_rollback: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        if sbom_rollback["environment"] is not None:
            self._environment = sbom_rollback["environment"]
        else:
            sbom_rollback["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_rollback["description"],
            "arc_evidence": "Rollback",
            "arc_display_type": "Rollback",
            "sbom_rollback_component": sbom_rollback["name"],
            "sbom_rollback_hash": sbom_rollback["hash"],
            "sbom_rollback_version": sbom_rollback["version"],
            "sbom_rollback_author": sbom_rollback["author"],
            "sbom_rollback_supplier": sbom_rollback["supplier"],
            "sbom_rollback_uuid": sbom_rollback["uuid"],
            "sbom_rollback_environment": sbom_rollback["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_rollback["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        asset_attrs = {
            "sbom_component": sbom_rollback["name"],
            "sbom_hash": sbom_rollback["hash"],
            "sbom_version": sbom_rollback["version"],
            "sbom_author": sbom_rollback["author"],
            "sbom_supplier": sbom_rollback["supplier"],
            "sbom_uuid": sbom_rollback["uuid"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self._asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    def rollback_plan(
        self,
        sbom_planned: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        if sbom_planned["environment"] is not None:
            self._environment = sbom_planned["environment"]
        else:
            sbom_planned["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_planned["description"],
            "arc_evidence": "Rollback Plan",
            "arc_display_type": "Rollback Plan",
            "sbom_planned_date": sbom_planned["date"],
            "sbom_planned_captain": sbom_planned["captain"],
            "sbom_planned_component": sbom_planned["name"],
            "sbom_planned_version": sbom_planned["version"],
            "sbom_planned_reference": sbom_planned["reference"],
            "sbom_planned_environment": sbom_planned["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_planned["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def rollback_accepted(
        self,
        sbom_accepted: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        if sbom_accepted["environment"] is not None:
            self._environment = sbom_accepted["environment"]
        else:
            sbom_accepted["environment"] = self._environment

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": sbom_accepted["description"],
            "arc_evidence": "Rollback Accepted",
            "arc_display_type": "Rollback Accepted",
            "sbom_accepted_date": sbom_accepted["date"],
            "sbom_accepted_captain": sbom_accepted["captain"],
            "sbom_accepted_component": sbom_accepted["name"],
            "sbom_accepted_version": sbom_accepted["version"],
            "sbom_accepted_reference": sbom_accepted["reference"],
            "sbom_accepted_environment": sbom_accepted["environment"],
        }

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": sbom_accepted["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)
        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    # Vulnerability Events

    def vuln_disclosure(
        self,
        vuln: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        self._add_attachments(attachments)

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

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": vuln["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def vuln_update(
        self,
        vuln: dict,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

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

        for i, attachment in enumerate(self._attachments):
            attrs[f"attachment_attr_{i}"] = {
                "arc_display_name": vuln["description"],
                "arc_attribute_type": "arc_attachment",
                "arc_blob_identity": attachment["identity"],
                "arc_blob_hash_alg": attachment["hash"]["alg"],
                "arc_blob_hash_value": attachment["hash"]["value"],
            }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def _add_attachments(self, attachments: list):
        self._attachments = []
        for attachment in attachments:
            with open(f"{attachment}", "rb") as fd:
                self._attachments.append(self.arch.attachments.upload(fd))
