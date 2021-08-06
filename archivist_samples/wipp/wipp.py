# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings

from typing import Optional

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from archivist import archivist as type_helper
from archivist.storage_integrity import StorageIntegrity


class Wipp:
    def __init__(
        self,
        arch: "type_helper.Archivist",
        *,
        storage_integrity=StorageIntegrity.TENANT_STORAGE,
    ):
        self._arch = arch
        self._asset = None
        self._storage_integrity = storage_integrity

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset

    @property
    def storage_integrity(self):
        return self._storage_integrity

    # Drum Asset
    def create(
        self,
        drum_name: str,
        drum_description: str,
        drum_serial: str,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        attrs = {
            "arc_display_name": drum_name,
            "arc_description": drum_description,
            "arc_display_type": "55 gallon drum",
            "arc_serial_number": drum_serial,
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
        self._asset = self.arch.assets.create(
            behaviours, attrs, storage_integrity=self._storage_integrity, confirm=True
        )

        return self._asset

    # Cask Asset
    def caskcreate(
        self,
        cask_name: str,
        cask_description: str,
        cask_serial: str,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        attrs = {
            "arc_display_name": cask_name,
            "arc_description": cask_description,
            "arc_display_type": "TRU RH 72B Cask",
            "arc_serial_number": cask_serial,
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
        self._asset = self.arch.assets.create(
            behaviours, attrs, storage_integrity=self._storage_integrity, confirm=True
        )

        return self._asset

    # Assset load by unique identity
    def read(
        self,
        identity: str,
    ):
        self._asset = self._arch.assets.read(identity)

    # Asset load by attributes(s)
    def read_by_signature(
        self,
        attributes: Optional[dict],
    ):
        # Hard-wire the Asset type
        newattrs = attributes.copy()
        newattrs["arc_display_type"] = "55 gallon drum"

        # Note: underlying Archivist will reaise ArchivistNotFoundError or
        # ArchivistDuplicateError unless this set of attributes points to
        # a single unique asset
        self._asset = self._arch.assets.read_by_signature(attrs=newattrs)

    # Drum Characerize Events
    def characterize(
        self,
        wipp: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Characterize",
            "arc_description": wipp["description"],
            "arc_evidence": "N/A",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "wipp_weight": wipp["weight"],
            "wipp_a2fraction_characterized": wipp["a2fraction_characterized"],
            "wipp_activity_characterized": wipp["activity_characterized"],
            "wipp_total_characterized": wipp["total_characterized"],
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

    # Tomography Events
    def tomography(
        self,
        wipp_tom: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Confirmation",
            "arc_description": wipp_tom["description"],
            "arc_evidence": "Radiograph attached",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "wipp_weight": wipp_tom["weight"],
            "wipp_a2fraction_confirmed": wipp_tom["a2fraction_confirmed"],
            "wipp_activity_confirmed": wipp_tom["activity_confirmed"],
            "wipp_total_confirmed": wipp_tom["total_confirmed"],
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

    # Loading Events
    def loading(
        self,
        wipp_load: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Loading",
            "arc_description": wipp_load["description"],
            "arc_evidence": "Loading placement image attached",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "wipp_container": wipp_load["container"],
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

    # Pre-Shipping Events
    def preshipping(
        self,
        wipp_preship: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Preship Inspection",
            "arc_description": wipp_preship["description"],
            "arc_evidence": "Image attached",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # Departure Events
    def departure(
        self,
        wipp_dep: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Transit",
            "arc_description": wipp_dep["description"],
            "arc_evidence": "Routing instructions in attachments",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # Waypoint Events
    def waypoint(
        self,
        wipp_way: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Transit",
            "arc_description": wipp_way["description"],
            "arc_evidence": "Signature: 0x1234abcd",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # Arrival Events
    def arrival(
        self,
        wipp_arr: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Transit",
            "arc_description": wipp_arr["description"],
            "arc_evidence": "Routing instructions in attachments",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            confirm=True,
        )

    # Unloading Events
    def unloading(
        self,
        wipp_unload: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Unloading",
            "arc_description": wipp_unload["description"],
            "arc_evidence": "Packing image attached",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {}

        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    # Emplacement Events
    def emplacement(
        self,
        wipp_emplace: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
    ):

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_display_type": "WO Emplacement",
            "arc_description": wipp_emplace["description"],
            "arc_evidence": "Packing image attached",
            "arc_attachments": attachments or [],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "wipp_emplacement_location": wipp_emplace["location"],
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
