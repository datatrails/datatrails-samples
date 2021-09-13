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

import datetime
import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import time

from archivist import about
from archivist.errors import ArchivistNotFoundError
from archivist.parser import common_parser

from ..testing.asset import MyAsset
from ..testing.parser import common_endpoint
from ..testing.time_warp import TimeWarp

LOGGER = logging.getLogger(__name__)


# Archivist utilities
#####################


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

    # who moves it and type of movement
    asset = MyAsset(
        ac,
        crate_id,
        tw,
        "1944.smarttags.synsation.io",
    )
    asset.move(
        f"Crate sealed in {start[0]} with 448 units on board",
        start[1],
        start[2],
    )
    time.sleep(delay)

    for point in waypoints:
        LOGGER.info(f"Asset arriving at {point[0]}")
        asset.move(
            f"Crate transferred by shipping agent at {point[0]} for onward forwarding",
            point[1],
            point[2],
        )
        time.sleep(delay)

    LOGGER.info(f"Asset ending its journey at {end[0]}")
    asset.move(
        f"Crate unsealed in {end[0]} with 448 units on board",
        end[1],
        end[2],
    )


def run(ac, args):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    # Find the asset record
    crate_id = None
    if args.asset_name:
        LOGGER.info(f"Looking for smart shipping crate '{args.asset_name}'...")
        try:
            crate = ac.assets.read_by_signature(
                attrs={"arc_display_name": args.asset_name}
            )
        except ArchivistNotFoundError:
            pass
        else:
            crate_id = crate["identity"]
    else:
        LOGGER.info("No crate specified...searching for one...")
        crates = list(
            ac.assets.list(
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
    parser, _ = common_parser(
        "Populates an Archivist install with devices from an Azure IoT Hub"
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

    args = parser.parse_args()

    poc = common_endpoint("synsation", args)
    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
