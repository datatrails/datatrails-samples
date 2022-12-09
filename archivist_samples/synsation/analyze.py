# WARNING: Proof of concept code: Not for release
# Simple event analyser for compliance/SLA verification

# pylint:  disable=missing-docstring
# pylint: disable=logging-fstring-interpolation


from datetime import datetime, timezone
import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about
from archivist.timestamp import parse_timestamp

from ..testing.archivist_parser import common_parser
from ..testing.asset import (
    MAINTENANCE_PERFORMED,
    MAINTENANCE_REQUEST,
    VULNERABILITY_ADDRESSED,
    VULNERABILITY_REPORT,
)
from ..testing.parser import common_endpoint

LOGGER = logging.getLogger(__name__)


def analyze_matched_pairs(label, p1, p2, events):
    if p1 in events and p2 in events:
        matched = set(events[p1]).intersection(events[p2])
        unmatched = set(events[p1]).difference(events[p2])

        LOGGER.info(f"There are {len(matched)} completed {label} events")

        for cv in matched:
            # Check how long it was outstanding
            time_req = parse_timestamp(events[p1][cv]["timestamp_declared"])
            time_resp = parse_timestamp(events[p2][cv]["timestamp_declared"])

            response_time = time_resp - time_req
            LOGGER.info(f" --> Response time: {response_time}")

        LOGGER.info(
            f"There are {len(unmatched)} uncompleted {label} events outstanding"
        )
        # Check how long it has been outstanding
        now = datetime.now(timezone.utc)
        for cv in unmatched:
            time_req = parse_timestamp(events[p1][cv]["timestamp_declared"])

            outstanding_time = now - time_req
            LOGGER.info(f" --> Outstanding for {outstanding_time}")

    else:
        LOGGER.info(f"There are NO {label} events to analyse")


def analyze_asset(conn, asset):
    # Fetch basic asset info. If any of these fields is missing it's fatal...
    try:
        aid = asset["identity"]
        attrs = asset["attributes"]
        aname = attrs["arc_display_name"]
        atype = attrs["arc_display_type"]
        aversion = attrs["arc_firmware_version"]
        aserial = attrs["arc_serial_number"]
        adesc = attrs["arc_description"]
    except KeyError:
        # Some devices won't have this property.  Just ignore failures.
        LOGGER.error("Malformed Asset.")
        return

    LOGGER.info("<---------------------------------------->")
    LOGGER.info(f"Analyzing {atype} '{aname}' (serial # {aserial})")
    LOGGER.info(f'"{adesc}"')
    LOGGER.info(f"Current Firmware Version: {aversion}")

    # Get all the events for this device
    number_of_events = conn.events.count(asset_id=aid)
    if number_of_events == 0:
        LOGGER.debug("No events found for asset")
        LOGGER.info("No events to analyse.")
        return

    allevents = conn.events.list(asset_id=aid)
    # Sort the events into paired buckets that we care about, keyed on
    # the events' "correlation_value". Only works for unique pairs of
    # correlation values, which is the suggested convention but not
    # enforced by Archivist services
    sortedevents = {}
    for event in allevents:
        try:
            etype = event["event_attributes"]["arc_display_type"]
            corval = event["event_attributes"]["arc_correlation_value"]
        except KeyError:
            LOGGER.debug("Couldn't get essential info for this event.")
            continue

        if etype not in sortedevents:
            sortedevents[etype] = {}

        sortedevents[etype][corval] = event

    # Now we've got them all we can do the analysis
    #  + Which events weren't fixed at all?
    #  + For events that were fixed, how long did it take?

    # maintenance events
    analyze_matched_pairs(
        "maintenance", MAINTENANCE_REQUEST, MAINTENANCE_PERFORMED, sortedevents
    )

    # vulnerability events
    analyze_matched_pairs(
        "firmware", VULNERABILITY_REPORT, VULNERABILITY_ADDRESSED, sortedevents
    )

    # Summarize TBD
    LOGGER.info("---")


def run(arch, args):
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)
    for asset in arch.assets.list():
        analyze_asset(arch, asset)

    LOGGER.info("Done.")
    sys_exit(0)


def entry():
    parser = common_parser("Checks maintenance and update performance for assets")
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default="synsation",
        help="namespace of item population (to enable parallel demos",
    )

    args = parser.parse_args()

    arch = common_endpoint("synsation", args)

    run(arch, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
