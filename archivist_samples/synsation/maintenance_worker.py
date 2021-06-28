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

import random
import time

from archivist.logger import LOGGER
from archivist.timestamp import make_timestamp

from .util import make_event_json


def service_device(charger, job_id, timewarp):
    # !!! WARNING !!! There is no thread-safety here, make sure you
    # always treat the device as read-only.
    # The main device thread takes care of updating the variables
    LOGGER.info("!! Agent responding to service request on %s", charger.name)

    # The maintenance is done...inform Archivist
    maint_msg = (
        f"Maintenance agent serviced device after "
        f"{charger.total_charge} units charged.  Next service "
        f"at {charger.next_service}."
    )
    notnow = timewarp.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "Maintenance",
        "Maintenance",
        dtstring,
        "Phil@evcservicing.com",
        "Service RP",
        maint_msg,
        job_id,
    )
    charger.archivist_client.events.create(
        charger.archivist_asset_identity, props, attrs
    )


def threadmain(charger, job_id, timewarp):
    # Wait a random time to simulate delays, travel etc
    time.sleep(random.randint(5, 20))

    # Do the service
    service_device(charger, job_id, timewarp)
