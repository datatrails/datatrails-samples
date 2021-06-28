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
import datetime
import time
import threading
import uuid

from archivist.logger import LOGGER
from archivist.timestamp import make_timestamp

from . import patch_worker
from .util import make_event_json


def issue_recall(charger_list, cve_str, timewarp):
    # !!! WARNING !!! There is no thread-safety here, make sure you
    # always treat the devices as read-only.
    # The main device thread takes care of updating the variables
    LOGGER.info("!! Issuing recall")

    # Inform everybody...
    for charger in charger_list:
        recall_msg = (
            f"Synsation Industries Large EV Chargers are vulnerable "
            f"to {cve_str}. Upgrade as soon as possible."
        )
        notnow = timewarp.now()
        dtstring = make_timestamp(notnow)
        cve_corval = cve_str + str(uuid.uuid4())
        props, attrs = make_event_json(
            "Firmware",
            "Vulnerability",
            dtstring,
            "VulnBot@synsation-industries.com",
            "FW Vulnerability",
            recall_msg,
            cve_corval,
        )
        attrs["arc_cve_id"] = cve_str
        charger.archivist_client.events.create(
            charger.archivist_asset_identity, props, attrs
        )

        # Schedule the patch
        x = threading.Thread(
            target=patch_worker.threadmain,
            args=(charger, cve_str, cve_corval, timewarp),
            daemon=True,
        )
        x.start()


def threadmain(chargers, timewarp):
    while True:
        time.sleep(60)

        # 1-in-4 chance of finding a vulnerability
        secure = random.randint(0, 3)
        if not secure:
            cve = f"CVE-{str(datetime.datetime.now())}"
            issue_recall(chargers, cve, timewarp)
