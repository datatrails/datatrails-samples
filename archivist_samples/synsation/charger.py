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

import argparse
import datetime
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import threading
import time

from archivist import about
from archivist.archivist import Archivist
from archivist.logger import set_logger, LOGGER

from ..testing.time_warp import TimeWarp

from ..testing.namespace import (
    assets_count,
    assets_list,
)

from . import ev_charger_device
from . import device_worker
from . import recall_worker


def initialize_devices(conn, airport):
    ev_chargers = []

    number_of_chargers = assets_count(
        conn,
        attrs={"arc_display_type": "EV charging station"},
    )

    debugstr = (
        f"Found {number_of_chargers} total chargers. "
        f"Looking for any in site '{airport}'..."
    )
    LOGGER.debug(debugstr)

    chargers_list = assets_list(
        conn,
        attrs={"arc_display_type": "EV charging station"},
    )
    # Whittle it down to just San Jose
    for charger in chargers_list:
        try:
            candidate = charger.name
            LOGGER.debug("Checking '%s'", candidate)
            if candidate.startswith(airport):
                evc = ev_charger_device.EVDevice(candidate, charger["identity"])
                evc.init_archivist_client(conn)
                ev_chargers.append(evc)
        except KeyError:
            # Some devices won't have these properties.  Just ignore failures.
            LOGGER.debug("This asset doesn't have valid attributes. Ignoring.")

    LOGGER.debug(
        "Found %d devices in %s " "from %d total devices",
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


def run(ac, args):
    """logic goes here"""
    # Stretch the timestamps in logs
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Creating time warp...")
    tw = TimeWarp(args.start_date, args.fast_forward)

    # Find all hte devices we're interested in
    LOGGER.info("Initializing chargers...")
    chargers = initialize_devices(ac, args.airport)
    if not chargers:
        LOGGER.info("No chargers found at airport %s.  Aborting.", args.airport)
        sys_exit(1)

    # Create worker threads:
    #  - One thread for each of the devices to do their thing
    #  - One thread to issue firmware recalls every now and again
    # Separate worker threads are kicked off for each maintenance
    # or firmware activity
    for c in chargers:
        x = threading.Thread(target=device_worker.threadmain, args=(c, tw), daemon=True)
        x.start()

    x = threading.Thread(
        target=recall_worker.threadmain, args=(chargers, tw), daemon=True
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
    parser = argparse.ArgumentParser(
        description="Simulates usage and maintenance of electric vehicle chargers"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="print verbose debugging",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        dest="url",
        action="store",
        default="https://rkvst.poc.jitsuin.io",
        help="location of Archivist service",
    )
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default=None,
        help="namespace of item population (to enable parallel demos",
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
        "-p",
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

    security = parser.add_mutually_exclusive_group(required=True)
    security.add_argument(
        "-t",
        "--auth-token",
        type=str,
        dest="auth_token_file",
        action="store",
        default=".auth_token",
        help="FILE containing API authentication token",
    )
    security.add_argument(
        "-c",
        "--clientcert",
        type=str,
        dest="client_cert_name",
        action="store",
        help=(
            "name of TLS client cert (.key and .pem with matching name"
            "must be in current directory)"
        ),
    )

    args = parser.parse_args()

    if args.verbose:
        set_logger("DEBUG")
    else:
        set_logger("INFO")

    # Initialise connection to Archivist
    LOGGER.info("Initialising connection to Jitsuin Archivist...")
    if args.auth_token_file:
        with open(args.auth_token_file, mode="r") as tokenfile:
            authtoken = tokenfile.read().strip()

        poc = Archivist(args.url, auth=authtoken, verify=False)

    elif args.client_cert_name:
        poc = Archivist(args.url, cert=args.client_cert_name, verify=False)

    if poc is None:
        LOGGER.error("Critical error.  Aborting.")
        sys_exit(1)

    poc.namespace = (
        "_".join(["synsation", args.namespace]) if args.namespace is not None else None
    )

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
