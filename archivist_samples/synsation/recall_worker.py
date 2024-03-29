# WARNING: Proof of concept code: Not for release
# Simulates events in the Synsation Industries EV Charger set

# pylint: disable=missing-docstring

import datetime
import logging
import random
import time
import threading
import uuid

from ..testing.asset import MyAsset

from . import patch_worker

LOGGER = logging.getLogger(__name__)


def issue_recall(charger_list, cve_id, timewarp):
    # !!! WARNING !!! There is no thread-safety here, make sure you
    # always treat the devices as read-only.
    # The main device thread takes care of updating the variables
    LOGGER.info("!! Issuing recall")

    # Inform everybody...
    for charger in charger_list:
        cve_corval = cve_id + str(uuid.uuid4())
        MyAsset(
            charger.archivist_client,
            charger.archivist_asset_identity,
            timewarp,
            "VulnBot@synsation-industries.com",
        ).report_vulnerability(
            (
                "Synsation Industries Large EV Chargers are vulnerable "
                f"to {cve_id}. Upgrade as soon as possible."
            ),
            cve_id,
            cve_corval,
        )
        # Schedule the patch
        x = threading.Thread(
            target=patch_worker.threadmain,
            args=(charger, cve_id, cve_corval, timewarp),
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
