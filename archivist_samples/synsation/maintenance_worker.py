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
# Simulates events in the Synsation Industries EV Charger set

# pylint: disable=missing-docstring

import logging
import random
import time

from .qualifications import check_qualification
from ..testing.asset import MyAsset

LOGGER = logging.getLogger(__name__)


def service_device(charger, arch, job_id, emp_id, timewarp):
    # !!! WARNING !!! There is no thread-safety here, make sure you
    # always treat the device as read-only.
    # The main device thread takes care of updating the variables
    LOGGER.info("!! Agent %s responding to service request on %s", emp_id, charger.name)

    # First check that this employee is qualified
    if not check_qualification(arch, emp_id, "maintenance qualification", charger.archivist_asset_identity):
        LOGGER.info("!! %s is NOT qualified! Not proceeding.", emp_id)
        return

    # The maintenance is done...inform Archivist
    MyAsset(
        arch,
        charger.archivist_asset_identity,
        timewarp,
        "Phil@evcservicing.com",
    ).service(
        (
            f"Maintenance agent serviced device after "
            f"{charger.total_charge} units charged.  Next service "
            f"at {charger.next_service}."
        ),
        job_id,
    )


def threadmain(charger, arch, job_id, emp_id, timewarp):
    # Wait a random time to simulate delays, travel etc
    time.sleep(random.randint(5, 20))

    # Do the service
    service_device(charger, arch, job_id, emp_id, timewarp)
