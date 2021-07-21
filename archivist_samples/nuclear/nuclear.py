# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings
from operator import floordiv
from typing import Optional
from random import random

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from archivist import archivist as type_helper


class Nuclear:
    def __init__(self, arch: "type_helper.Archivist"):
        self._arch = arch
        self._asset = None
        # self._attachments = None

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset

    # @property
    # def attachements(self):
    #    return self._attachments

    # Asset Creation
    def create(
        self,
        nw_name: str,
        nw_description: str,
        nw_code: str,
        nw_lifecycle,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        attrs = {
            "arc_display_name": nw_name,
            "arc_description": nw_description,
            "arc_display_type": "Nuclear Waste Item",
            "nw_waste_code": nw_code,
            "nw_lifecycle_stage": nw_lifecycle,
            "nw_namespace": random(),
            "attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        behaviours = [
            "Attachments",
            "Firmware",
            "LocationUpdate",
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
        attachments: Optional[list] = None,
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
            "arc_evidence": "Characterize",
            "arc_display_type": "Characterize",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            atrrs.update(custom_attrs)

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
            asset_atrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_atrs,
            confirm=True,
        )

    # def _add_attachments(self, attachements: list):
    #    self._attachments = []
    #    for attachment in attachments:
    #        with open(f"{attachment}", "rb") as fd:
    #            self._attachments.append(self.arch.attachements.upload(fd))
