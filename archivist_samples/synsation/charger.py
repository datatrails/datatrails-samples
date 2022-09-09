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
# including firmware issues


# pylint:  disable=fixme
# pylint:  disable=missing-docstring

import datetime
import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import threading
import time

from archivist import about

from ..testing.archivist_parser import common_parser
from ..testing.parser import common_endpoint
from ..testing.time_warp import TimeWarp

from . import ev_charger_device
from . import device_worker
from . import recall_worker

LOGGER = logging.getLogger(__name__)


def initialize_devices(arch, airport):
    ev_chargers = []

    number_of_chargers = arch.assets.count(
        attrs={"arc_display_type": "EV charging station"},
    )

    debugstr = (
        f"Found {number_of_chargers} total chargers. "
        f"Looking for any in site '{airport}'..."
    )
    LOGGER.debug(debugstr)

    chargers_list = arch.assets.list(
        attrs={"arc_display_type": "EV charging station"},
    )
    # Whittle it down to just San Jose
    for charger in chargers_list:
        try:
            candidate = charger.name
            LOGGER.debug("Checking '%s'", candidate)
            if candidate.startswith(airport):
                evc = ev_charger_device.EVDevice(candidate, charger["identity"])
                ev_chargers.append(evc)
        except KeyError:
            # Some devices won't have these properties.  Just ignore failures.
            LOGGER.debug("This asset doesn't have valid attributes. Ignoring.")

    LOGGER.debug(
        "Found %d devices in %s from %d total devices",
        len(ev_chargers),
        airport,
        number_of_chargers,
    )
    return ev_chargers


def interrupt_listener_run_until(tw, stop):
    try:
        while True:
            # The worker threads are doing everything, so just leave this
            # one to wait for keyboard interrupts and kill the daemons
            time.sleep(1)

            # TODO: this is inefficient - in theory we could pre-calculate
            # when the timewarp will hit this value rather than checking it
            # every time
            if stop and tw.now() > stop:
                LOGGER.info("Jitsuin EV Charger example reached end time")
                break

    except KeyboardInterrupt:
        LOGGER.info("Jitsuin EV Charger example stopped")


def run(ev_arch, maint_arch, fw_arch, args):
    """logic goes here"""
    # Stretch the timestamps in logs
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    LOGGER.info("Creating time warp...")

    tw = TimeWarp(args.start_date, args.fast_forward)

    # Find all hte devices we're interested in
    LOGGER.info("Initializing chargers...")
    chargers = initialize_devices(ev_arch, args.airport)
    if not chargers:
        LOGGER.info("No chargers found at airport %s.  Aborting.", args.airport)
        sys_exit(1)

    # Create worker threads:
    #  - One thread for each of the devices to do their thing
    #  - One thread to issue firmware recalls every now and again
    # Separate worker threads are kicked off for each maintenance
    # or firmware activity
    for c in chargers:
        x = threading.Thread(target=device_worker.threadmain, args=(c, ev_arch, maint_arch, tw), daemon=True)
        x.start()

    x = threading.Thread(
        target=recall_worker.threadmain, args=(chargers, fw_arch, tw), daemon=True
    )
    x.start()

    LOGGER.info("Beginning telemetry run")
    if args.stop_date:
        LOGGER.info(
            "Press Ctrl-C to exit, or will stop automatically at %s", args.stop_date
        )
    else:
        LOGGER.info("Press Ctrl-C to exit")

    interrupt_listener_run_until(tw, args.stop_date)
    sys_exit(0)


def entry():
    parser = common_parser(
        "Simulates usage and maintenance of electric vehicle chargers"
    )

    # per example options here ....
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        dest="wait",
        action="store",
        default=0.0,
        help="add a delay between API calls",
    )
    parser.add_argument(
        "-a",
        "--airport",
        type=str,
        dest="airport",
        action="store",
        default="SJC",
        help="Airport site to use",
    )
    parser.add_argument(
        "-s",
        "--start-date",
        type=lambda d: datetime.datetime.strptime(d, "%Y%m%d"),
        dest="start_date",
        action="store",
        default=datetime.date.today() - datetime.timedelta(days=1),
        help="Start date for event series (format: yyyymmdd)",
    )
    parser.add_argument(
        "-S",
        "--stop-date",
        type=lambda d: datetime.datetime.strptime(d, "%Y%m%d"),
        dest="stop_date",
        action="store",
        help="Stop when timewarp reaches this date (format: yyyymmdd)",
    )
    parser.add_argument(
        "-f",
        "--fast-forward",
        type=float,
        dest="fast_forward",
        action="store",
        default=3600,
        help="Fast forward time in event series (default: 1 second = 1 hour)",
    )
    parser.add_argument(
        "--maint-client-id",
        type=str,
        dest="maint_client_id",
        action="store",
        default=None,
        help="Client ID from appregistrations for maintenance worker",
    )
    parser.add_argument(
        "--maint-client-secret",
        type=str,
        dest="maint_client_secret",
        action="store",
        default=None,
        help="Client secret from appregistrations for maintenance worker",
    )
    parser.add_argument(
        "--fw-client-id",
        type=str,
        dest="fw_client_id",
        action="store",
        default=None,
        help="Client ID from appregistrations for firmware worker",
    )
    parser.add_argument(
        "--fw-client-secret",
        type=str,
        dest="fw_client_secret",
        action="store",
        default=None,
        help="Client secret from appregistrations for firmware worker",
    )

    args = parser.parse_args()

    ev_arch = common_endpoint("synsation", args)
    if args.maint_client_id:
        args.client_id = args.maint_client_id
        args.client_secret = args.maint_client_secret
    maint_arch = common_endpoint("synsation", args)
    if args.fw_client_id:
        args.client_id = args.fw_client_id
        args.client_secret = args.fw_client_secret
    fw_arch = common_endpoint("synsation", args)

    print("Testing connections...")
    n_ev = ev_arch.assets.count(
        attrs={"arc_display_type": "EV charging station"},
    )
    n_maint = maint_arch.assets.count(
        attrs={"arc_display_type": "EV charging station"},
    )
    n_fw = fw_arch.assets.count(
        attrs={"arc_display_type": "EV charging station"},
    )
    print(f'Connection test complete: ${n_ev} : ${n_maint} : ${n_fw}')
    if n_ev != n_maint or n_ev != n_fw:
        print("Incorrect permissions. Aborting.")
        exit()

    run(ev_arch, maint_arch, fw_arch, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
