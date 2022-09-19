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
import threading
import time
import uuid

from . import maintenance_worker


def threadmain(charger, ev_arch, maint_arch, emp_id, timewarp):
    while True:
        # Wait for a customer to show up
        time.sleep(random.randint(1, 10))

        # Charge up
        charger.charge_job(ev_arch, random.randint(25, 99), timewarp)

        # Check if it needs servicing, and kick off a maintenance worker
        # thread to attend to it if so
        corval = str(uuid.uuid4())
        if charger.service_required(ev_arch, corval, timewarp):
            # Call the maintenance crew
            x = threading.Thread(
                target=maintenance_worker.threadmain,
                args=(charger, maint_arch, corval, emp_id, timewarp),
                daemon=True,
            )
            x.start()
