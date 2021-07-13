#   Copyright 2019 Jitsuin, inc
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# WARNING: Proof of concept code: Not for release
# Copies the flow of the Jitsuinator demo script

"""Class that implements common actions on an asset. This is the secret sauce
   and this code may be added to the python SDK at some later date...
"""

# pylint:  disable=missing-docstring

from archivist.timestamp import make_timestamp

from .namespace import (
    events_create,
)

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
        events_create(
            self.ac,
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
            confirm=True,
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

        events_create(
            self.ac,
            self.crate_id,
            {
                **self.base_props,
                **{
                    "timestamp_declared": make_timestamp(self.tw.now()),
                },
            },
            attrs,
            confirm=True,
        )

    def move(self, desc, lat, lng):
        """Move asset from one place to another"""
        events_create(
            self.ac,
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
            confirm=True,
        )

    def patch_vulnerability(self, desc, evidence):
        """Patch  vulnerability"""
        events_create(
            self.ac,
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
            confirm=True,
        )

    def report_vulnerability(self, desc, cve_id, cve_corval):
        """Report vulnerability"""
        events_create(
            self.ac,
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
            confirm=True,
        )

    def service_required(self, desc, corval):
        """Indicate that maintenance must been done"""
        events_create(
            self.ac,
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
            confirm=True,
        )

    def service(self, desc, corval):
        """Indicate that maintenance has been done"""
        events_create(
            self.ac,
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
            confirm=True,
        )

    def update_firmware(self, desc, fw_version, corval):
        """Update firmware"""
        events_create(
            self.ac,
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
            confirm=True,
        )
