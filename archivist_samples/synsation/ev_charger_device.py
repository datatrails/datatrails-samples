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
# Simulates an EV Charger device with integrated Archivist endpoint

# pylint: disable=missing-docstring


import logging
import threading
import uuid

from ..testing.asset import MyAsset

LOGGER = logging.getLogger(__name__)


class EVDevice:
    def __init__(self, name, aid):
        self._name = name
        self._archivist_asset_identity = aid

        self._fw_version = [1, 0]
        self._next_service = 1000
        self._total_charge = 0

        self._writelock = threading.RLock()

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._archivist_asset_identity

    @property
    def total_charge(self):
        return self._total_charge

    @property
    def next_service(self):
        return self._next_service

    @property
    def archivist_asset_identity(self):
        return self._archivist_asset_identity

    def charge_job(self, arch, units, timewarp):
        # Simulate charging: simply keep a record of how many units charged
        LOGGER.info("Device %s charging %s units", self._name, units)
        self._total_charge += units

        MyAsset(
            arch,
            self._archivist_asset_identity,
            timewarp,
            f"{self._archivist_asset_identity[7:]}@evc.m2m.synsation.io",
        ).charge(
            f"Device {self._name} charging {units} units",
            "Attestation receipt: 0xa765dd854b57334ab1f7322d2",
        )

    def service_required(self, arch, corval, timewarp):
        if self._total_charge < self._next_service:
            return False

        # Clear the flag and update the service interval
        self._next_service += 1000

        # Log our request
        LOGGER.info(
            "!! %s Service interval reached (%s)", self.name, self._total_charge
        )

        MyAsset(
            arch,
            self._archivist_asset_identity,
            timewarp,
            f"{self._archivist_asset_identity[7:]}@evc.m2m.synsation.io",
        ).service_required(
            (
                f"Service interval reached after {self._total_charge} "
                f"units charged. Please service."
            ),
            corval,
        )

        return True

    def update_firmware(self, arch, cve_str, cve_corval, timewarp):
        LOGGER.info("!! %s patching vulnerable firmware", self.name)

        with self._writelock:
            # Simple Red-Hat style versioning
            if self._fw_version[1] == 3:
                self._fw_version[0] += 1
                self._fw_version[1] = 0
            else:
                self._fw_version[1] += 1

            version = f"v{self._fw_version[0]}.{self._fw_version[1]}"
            MyAsset(
                arch,
                self._archivist_asset_identity,
                timewarp,
                "otaService@evcservicing.com",
            ).update_firmware(
                f"Responding to vulnerability '{cve_str}' with patch '{version}'",
                version,
                cve_corval,
            )
