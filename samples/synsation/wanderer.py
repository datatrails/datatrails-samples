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
# Simulates events in a mobile asset

# pylint: disable=missing-docstring
# pylint: disable=logging-fstring-interpolation

import argparse
import datetime
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import time

from archivist import about
from archivist.archivist import Archivist
from archivist.errors import ArchivistNotFoundError
from archivist.logger import set_logger, LOGGER
from archivist.timestamp import make_timestamp

from testing.namespace import (
    assets_list,
    assets_read_by_signature,
    events_create,
)
from testing.time_warp import TimeWarp

from .util import make_event_json


# Archivist utilities
#####################


def make_event_json_template(
    unused_asset_identity, what_str, who_str, message, lat, lng, tw
):
    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "RecordEvidence", "Record", dtstring, who_str, what_str, message, ""
    )
    attrs["arc_evidence"] = message
    attrs["arc_gis_lat"] = lat
    attrs["arc_gis_lng"] = lng
    return props, attrs


def shipit(ac, crate_id, delay, tw):
    # Simulate a journey from Manufacturing home to regional plant
    # Flint -> Chicago -> Newark Liberty -> Heathrow T4 -> Munich -> Stuttgart -> plant
    start = ["Synsation Flint Manufacturing", "43.018889", "-83.693333"]
    waypoints = [
        ["Chicago Freight Hub", "41.978611", "-87.904722"],
        ["Newark Freight Intl", "40.692500", "-74.168611"],
        ["London Heathrow T4", "51.459455", "-0.446953"],
        ["Munich Forwarding", "48.353889", "11.786111"],
        ["Stuttgart Hub", "48.690000", "9.221944"],
    ]
    end = ["Synsation Stuttgart Finishing Plant", "48.783333", "9.183333"]

    # Crate smart tag is the reporting entity in each case
    who_str = "1944.smarttags.synsation.io"

    LOGGER.info(f"Asset starting its journey at {start[0]}")
    props, attrs = make_event_json_template(
        crate_id,
        "Shipping Movement",
        who_str,
        f"Crate sealed in {start[0]} with 448 units on board",
        start[1],
        start[2],
        tw,
    )
    events_create(ac, crate_id, props, attrs)
    time.sleep(delay)

    for point in waypoints:
        LOGGER.info(f"Asset arriving at {point[0]}")
        props, attrs = make_event_json_template(
            crate_id,
            "Shipping Movement",
            who_str,
            f"Crate transferred by shipping agent at {point[0]} for onward forwarding",
            point[1],
            point[2],
            tw,
        )
        events_create(ac, crate_id, props, attrs)
        time.sleep(delay)

    LOGGER.info(f"Asset ending its journey at {end[0]}")
    props, attrs = make_event_json_template(
        crate_id,
        "Shipping Movement",
        who_str,
        f"Crate unsealed in {end[0]} with 448 units on board",
        end[1],
        end[2],
        tw,
    )
    events_create(ac, crate_id, props, attrs)


def run(ac, args):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    # Find the asset record
    crate_id = None
    if args.asset_name:
        LOGGER.info(f"Looking for smart shipping crate '{args.asset_name}'...")
        try:
            crate = assets_read_by_signature(
                ac, attrs={"arc_display_name": args.asset_name}
            )
        except ArchivistNotFoundError:
            pass
        else:
            crate_id = crate["identity"]
    else:
        LOGGER.info("No crate specified...searching for one...")
        crates = list(
            assets_list(
                ac,
                attrs={"arc_display_type": "Widget shipping crate"},
            )
        )
        if len(crates) > 0:
            LOGGER.info(f"Using '{crates[0]['attributes']['arc_display_name']}'")
            crate_id = crates[0]["identity"]

    if not crate_id:
        LOGGER.info("Could not find target crate.  Aborting.")
        sys_exit(1)

    LOGGER.info("Creating time warp...")
    tw = TimeWarp(args.start_date, args.fast_forward)

    LOGGER.info("Beginning journey simulation...")
    shipit(ac, crate_id, args.wait, tw)

    LOGGER.info("Done.")
    sys_exit(0)


def entry():
    parser = argparse.ArgumentParser(
        description="Populates an Archivist install with devices from an Azure IoT Hub"
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
        default=0.5,
        help="add a delay between API calls",
    )
    parser.add_argument(
        "-n",
        "--asset_name",
        type=str,
        dest="asset_name",
        action="store",
        help="Name of the asset to ship",
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
