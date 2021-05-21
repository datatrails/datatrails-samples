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


def threadmain(charger, cve_str, cve_corval, timewarp):
    # Wait a random time to simulate delays, maintenance window etc
    time.sleep(random.randint(10, 20))

    # 1-in-4 chance of missing the patch
    patch = random.randint(0, 3)
    if patch:
        charger.update_firmware(cve_str, cve_corval, timewarp)
