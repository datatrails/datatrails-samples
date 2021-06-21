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

"""Gives basic information about an Archivist estate"""

# pylint:  disable=missing-docstring


import argparse
from collections import Counter
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about
from archivist.archivist import Archivist
from archivist.logger import set_logger, LOGGER

# Main app
##########


def run(poc, args):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    # NB: a non-null namespace will print warnings as there are some internally generated
    # events that will not be namespaced.
    namespace = (
        {"functests_namespace": poc.namespace} if poc.namespace is not None else None
    )
    LOGGER.info("Namespace is %s", namespace)
    if args.quick_count:
        LOGGER.info("Number of events is %d", poc.events.count(attrs=namespace))
        LOGGER.info("Number of assets is %d", poc.assets.count(attrs=namespace))
        LOGGER.info("Number of locations is %d", poc.locations.count(attrs=namespace))
        sys_exit(0)

    if args.double_check:
        # for around 550 events and 250 assets this can take about a 90s...
        LOGGER.info("Performing double-check... START")

        event_ids = Counter(e["identity"] for e in poc.events.list(attrs=namespace))
        duplicate_event_ids = {k: v for k, v in event_ids.items() if v > 1}
        for k, v in duplicate_event_ids.items():
            LOGGER.info("!! Event id %s DUPLICATED %d times!", k, v)

        event_ids_from_asset = Counter(
            e["identity"]
            for a in poc.assets.list(attrs=namespace)
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

        num_events = poc.events.count(attrs=namespace)
        num_assets = poc.assets.count(attrs=namespace)
        num_locations = poc.locations.count(attrs=namespace)

        LOGGER.info(
            (
                "%s: There are %s events registered against %s assets"
                " in the system spread over %s locations."
            ),
            poc.namespace,
            num_events,
            num_assets,
            num_locations,
        )

        LOGGER.info("Performing double-check... FINISH")
        sys_exit(0)


def main():
    parser = argparse.ArgumentParser(description="Some title")
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
        help="namespace of item population (to enable parallel demos)",
    )

    # per example options here

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

    poc.namespace = None  # ignore namespacing for the time being

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)


if __name__ == "__main__":
    # execute only if run as a script
    main()
