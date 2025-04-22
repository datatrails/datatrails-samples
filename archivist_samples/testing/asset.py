# WARNING: Proof of concept code: Not for release

"""Class that implements common actions on an asset. This is the secret sauce
and this code may be added to the python SDK at some later date...
"""

# pylint:  disable=missing-docstring

from archivist.timestamp import make_timestamp

CONFIG_MANAGEMENT = "Config Management"
OPERATIONAL_REPORT = "Operational Report"
MAINTENANCE_PERFORMED = "Maintenance Performed"
MAINTENANCE_REQUEST = "Maintenance Request"
SHIPPING_MOVEMENT = "Shipping Movement"
VULNERABILITY_ADDRESSED = "Vulnerability Addressed"
VULNERABILITY_REPORT = "Vulnerability Report"


class MyAsset:
    def __init__(self, ac, crate_id, tw, who):
        self.ac = ac
        self.crate_id = crate_id
        self.tw = tw
        self.base_props = {
            "behaviour": "RecordEvidence",
            "operation": "Record",
            "principal_declared": {
                "issuer": "job.idp.server/1234",
                "subject": who,
                "display_name": who,
            },
        }

    def charge(self, desc, evidence):
        """Charge device"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": OPERATIONAL_REPORT,
                "arc_description": desc,
                "arc_evidence": evidence,
            },
        )

    def certify_patch(self, desc, evidence, attachments, extra_attrs=None):
        """Certify issued patch"""
        attrs = {
            **{
                "arc_display_type": CONFIG_MANAGEMENT,
                "arc_description": desc,
                "arc_evidence": evidence,
            },
            **attachments,
        }
        if extra_attrs is not None:
            attrs.update(extra_attrs)

        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            attrs,
        )

    def move(self, desc, lat, lng):
        """Move asset from one place to another"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": SHIPPING_MOVEMENT,
                "arc_description": desc,
                "arc_gis_lat": lat,
                "arc_gis_lng": lng,
            },
        )

    def patch_vulnerability(self, desc, evidence):
        """Patch  vulnerability"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": CONFIG_MANAGEMENT,
                "arc_description": desc,
                "arc_evidence": evidence,
            },
        )

    def report_vulnerability(self, desc, cve_id, cve_corval):
        """Report vulnerability"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": VULNERABILITY_REPORT,
                "arc_description": desc,
                "arc_cve_id": cve_id,
                "arc_correlation_value": cve_corval,
            },
        )

    def service_required(self, desc, corval):
        """Indicate that maintenance must been done"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": MAINTENANCE_REQUEST,
                "arc_description": desc,
                "arc_correlation_value": corval,
            },
        )

    def service(self, desc, corval):
        """Indicate that maintenance has been done"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": MAINTENANCE_PERFORMED,
                "arc_description": desc,
                "arc_correlation_value": corval,
            },
        )

    def update_firmware(self, desc, fw_version, corval):
        """Update firmware"""
        self.ac.events.create(
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            {
                "arc_display_type": VULNERABILITY_ADDRESSED,
                "arc_description": desc,
                "arc_firmware_version": fw_version,
                "arc_correlation_value": corval,
            },
            asset_attrs={"arc_firmware_version": fw_version},
        )
