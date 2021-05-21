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
# Simple event analyser for compliance/SLA verification

# pylint:  disable=missing-docstring
# pylint: disable=logging-fstring-interpolation


import argparse
from datetime import datetime, timezone
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about
from archivist.archivist import Archivist
from archivist.logger import set_logger, LOGGER
from archivist.timestamp import parse_timestamp

from testing.namespace import (
    assets_list,
    events_count,
    events_list,
)


def analyze_matched_pairs(label, p1, p2, events):
    if p1 in events and p2 in events:
        matched = set(events[p1]).intersection(set(events[p2]))
        unmatched = set(events[p1]).difference(set(events[p2]))

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
    number_of_events = events_count(conn, asset_id=aid)
    if number_of_events == 0:
        LOGGER.debug("No events found for asset")
        LOGGER.info("No events to analyse.")
        return

    allevents = events_list(conn, asset_id=aid)
    # Sort the events into paired buckets that we care about, keyed on
    # the events' "correlation_value". Only works for unique pairs of
    # correlation values, which is the suggested convention but not
    # enforced by Archivist services
    sortedevents = {}
    for event in allevents:
        try:
            etype = event["operation"]
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
    analyze_matched_pairs(
        "maintenance", "MaintenanceRequired", "Maintenance", sortedevents
    )
    analyze_matched_pairs("firmware", "Vulnerability", "Update", sortedevents)

    # Summarize TBD
    LOGGER.info("---")


def run(archivist):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Analyzing devices for namespace %s", archivist.namespace)
    for asset in assets_list(archivist):
        analyze_asset(archivist, asset)

    LOGGER.info("Done.")
    sys_exit(0)


def entry():
    parser = argparse.ArgumentParser(
        description="Checks maintenance and update performance for assets"
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
        default="https://playground-avid.engineering-k8s-poc-1.dev.poc.jitsuin.io",
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

    run(poc)

    parser.print_help(sys_stdout)
    sys_exit(1)
