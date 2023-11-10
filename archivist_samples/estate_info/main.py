# WARNING: Proof of concept code: Not for release

"""Gives basic information about an Archivist estate"""

# pylint:  disable=missing-docstring


from collections import Counter
import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about

from ..testing.archivist_parser import common_parser
from ..testing.parser import common_endpoint

LOGGER = logging.getLogger(__name__)

# Main app
##########


def run(poc, args):
    """
    runs the sample and returns the system error code.
    """
    LOGGER.info("Using version %s of datatrails-archivist", about.__version__)
    if args.quick_count:
        LOGGER.info("Number of events is %d", poc.events.count())
        LOGGER.info("Number of assets is %d", poc.assets.count())
        LOGGER.info("Number of locations is %d", poc.locations.count())
        return 0

    if args.double_check:
        # for around 550 events and 250 assets this can take about a 90s...
        LOGGER.info("Performing double-check... START")

        event_ids = Counter(e["identity"] for e in poc.events.list())
        duplicate_event_ids = {k: v for k, v in event_ids.items() if v > 1}
        for k, v in duplicate_event_ids.items():
            LOGGER.info("!! Event id %s DUPLICATED %d times!", k, v)

        event_ids_from_asset = Counter(
            e["identity"]
            for a in poc.assets.list()
            for e in poc.events.list(asset_id=a["identity"])
        )

        duplicate_event_ids_from_asset = {
            k: v for k, v in event_ids_from_asset.items() if v > 1
        }
        for k, v in duplicate_event_ids_from_asset.items():
            LOGGER.info("!! Event id from asset %s DUPLICATED %d times!", k, v)

        for o in set(event_ids).difference(event_ids_from_asset):
            LOGGER.info("!! Event id %s is not in any asset", o)

        for o in set(event_ids_from_asset).difference(event_ids):
            LOGGER.info("!! Event id %s is in an asset but not in main list", o)

        num_events = poc.events.count()
        num_assets = poc.assets.count()
        num_locations = poc.locations.count()

        LOGGER.info(
            (
                "There are %s events registered against %s assets"
                " in the system spread over %s locations."
            ),
            num_events,
            num_assets,
            num_locations,
        )

        LOGGER.info("Performing double-check... FINISH")
        return 0

    return 1


def main():
    parser = common_parser("Get basic information about your DataTrails estate")

    # per example exclusive options here
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument(
        "-q",
        "--quick-count",
        dest="quick_count",
        action="store_true",
        default=False,
        help="just quick count resources. Do not analyse the records.",
    )
    operations.add_argument(
        "-d",
        "--double-check",
        dest="double_check",
        action="store_true",
        default=False,
        help="cross-check total event count against assets",
    )

    args = parser.parse_args()

    poc = common_endpoint("estate_info", args)

    err_code = run(poc, args)

    if err_code != 0:
        parser.print_help(sys_stdout)
        sys_exit(err_code)
