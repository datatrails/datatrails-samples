# WARNING: Proof of concept code: Not for release
# Simulates events in the Synsation Industries EV Charger set

# pylint: disable=missing-docstring


import random
import time


def threadmain(charger, timewarp):
    while True:
        # Wait for a customer to show up
        time.sleep(random.randint(1, 10))

        # Charge up
        charger.charge_job(random.randint(25, 99), timewarp)

        # Check if it needs servicing, and kick off a maintenance worker
        # thread to attend to it if so
        charger.service(timewarp)
