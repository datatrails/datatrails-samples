# WARNING: Proof of concept code: Not for release
# Simulates events in the Synsation Industries EV Charger set

# pylint: disable=missing-docstring

import random
import time


def threadmain(charger, cve_str, cve_corval, timewarp):
    # Wait a random time to simulate delays, maintenance window etc
    time.sleep(random.randint(10, 20))

    # 1-in-4 chance of missing the patch
    patch = random.randint(0, 3)
    if patch:
        charger.update_firmware(cve_str, cve_corval, timewarp)
