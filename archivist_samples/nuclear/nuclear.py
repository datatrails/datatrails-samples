# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings

from typing import Optional
#from random import random

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from archivist import archivist as type_helper


class Nuclear:
    def __init__(self, arch: "type_helper.Archivist"):
        self._arch = arch
        self._asset = None

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset

    # Waste Item Asset Creation
    def create(
        self,
        nw_name: str,
        nw_description: str,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        attrs = {
            "arc_display_name": nw_name,
            "arc_description": nw_description,
            "arc_display_type": "Nuclear Waste Item",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        behaviours = [
            "Attachments",
            "Firmware",
            "Maintenance",
            "RecordEvidence",
        ]
        self._asset = self.arch.assets.create(behaviours, attrs, confirm=True)
        return self._asset

    # Container Asset Creation
    def concreate(
        self,
        cw_name: str,
        cw_description: str,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        attrs = {
            "arc_display_name": cw_name,
            "arc_description": cw_description,
            "arc_display_type": "Nuclear Disposal Container",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        behaviours = [
            "Attachments",
            "Firmware",
            "Maintenance",
            "RecordEvidence",
        ]
        self._asset = self.arch.assets.create(behaviours, attrs, confirm=True)
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
        newattrs["arc_display_type"] = "Nuclear Waste Item"

        # Note: underlying Archivist will raise ArchivistNotFoundError or
        # ArchivistDuplicateError unless this set of attributes points to
        # a single unique asset
        self._asset = self.arch.assets.read_by_signature(attrs=newattrs)

    # Characterize Events
    def characterize(
        self,
        nw: dict,
        *,
        latest_nw: Optional[dict] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }

        if latest_nw is None:
            latest_nw = nw
        attrs = {
            "arc_description": nw["description"],
            "arc_evidence": "No evidence provided",
            "arc_display_type": "Characterize",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "arc_display_name": latest_nw["name"],
            "nw_item_activity_group_b1": latest_nw["nw_item_activity_group_b1"],
            "nw_fissile_particles": latest_nw["nw_fissile_particles"],
            "nw_active_particles": latest_nw["nw_active_particles"],
            "nw_activity_nonalpha": latest_nw["nw_activity_nonalpha"],
            "nw_item_activity_group_a": latest_nw["nw_item_activity_group_a"],
            "nw_explosives": latest_nw["nw_explosives"],
            "nw_soluble_solids": latest_nw["nw_soluble_solids"],
            "nw_oxidizing_agents": latest_nw["nw_oxidizing_agents"],
            "nw_item_activity_group_b2": latest_nw["nw_item_activity_group_b2"],
            "nw_item_activity_group_c": latest_nw["nw_item_activity_group_c"],
            "nw_waste_weight": latest_nw["nw_waste_weight"],
            "nw_activity_alpha": latest_nw["nw_activity_alpha"],
            "nw_waste_code": latest_nw["nw_waste_code"],
            "nw_lifecycle_stage": latest_nw["nw_lifecycle_stage"],
            "nw_target_stream": latest_nw["nw_target_stream"],
            "nw_free_liquid": latest_nw["nw_free_liquid"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Package Events
    def package(
        self,
        nw_packaged: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_packaged["description"],
            "arc_evidence": "No evidence provided",
            "arc_display_type": "Package",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_in_container": nw_packaged["nw_in_container"],
            "nw_lifecycle_stage": nw_packaged["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Buffer Storage
    def buffer(
        self,
        nw_buffered: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_buffered["description"],
            "arc_evidence": nw_buffered["evidence"],
            "arc_display_type": "BufferStore",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_buffered["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Treatment
    def treat(
        self,
        nw_treated: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_treated["description"],
            "arc_evidence": "No evidence provided",
            "arc_display_type": "Treat",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_treated["nw_lifecycle_stage"],
            "nw_waste_inventory": nw_treated["nw_waste_inventory"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Condition
    def condition(
        self,
        nw_condition: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_condition["description"],
            "arc_evidence": "No evidence provided",
            "arc_display_type": "Condition",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_condition["nw_lifecycle_stage"],
            "nw_waste_code": nw_condition["nw_waste_code"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Iterim Storage
    def iterim(
        self,
        nw_interim: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_interim["description"],
            "arc_evidence": nw_interim["evidence"],
            "arc_display_type": "InterimStore",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_interim["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Sentence Container
    def sentence(
        self,
        nw_sentence: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_sentence["description"],
            "arc_evidence": nw_sentence["evidence"],
            "arc_display_type": "Sentence",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_sentence["nw_lifecycle_stage"],
            "nw_waste_stream": nw_sentence["nw_waste_stream"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Commit Container
    def commit(
        self,
        nw_commit: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_commit["description"],
            "arc_evidence": nw_commit["evidence"],
            "arc_display_type": "Commit",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_commit["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Transport Container
    def transport(
        self,
        nw_transport: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_transport["description"],
            "arc_evidence": nw_transport["evidence"],
            "arc_display_type": "Transport",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_transport["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Accept Container
    def accept(
        self,
        nw_accept: dict,
        *,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": nw_accept["description"],
            "arc_evidence": nw_accept["evidence"],
            "arc_display_type": "Dispose",
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "nw_lifecycle_stage": nw_accept["nw_lifecycle_stage"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )
