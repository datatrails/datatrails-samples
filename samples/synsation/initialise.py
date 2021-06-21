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

"""Initialise dataset for synsation"""

# pylint:  disable=missing-docstring


import argparse
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about
from archivist.archivist import Archivist
from archivist.logger import set_logger, LOGGER

from testing.namespace import assets_wait_for_confirmed

from . import synsation_corporation
from . import synsation_industries
from . import synsation_manufacturing
from . import synsation_smartcity

# Main app
##########


def run(ac, args):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    if args.create_corporation:
        synsation_corporation.initialise_all(ac, args.num_assets, args.wait)

    if args.create_industries:
        synsation_industries.initialise_all(ac)

    if args.create_manufacturing:
        synsation_manufacturing.initialise_all(ac)

    if args.create_smartcity:
        synsation_smartcity.initialise_all(ac)

    # Wait for all assets to confirm before we do anything with them
    if args.await_confirmation:
        assets_wait_for_confirmed(ac, attrs={"company": "synsation"})

    sys_exit(0)


def entry():
    parser = argparse.ArgumentParser(
        description="Populates a clean Archivist with Synsation test data"
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

    parser.add_argument(
        "-C",
        "--no-corporation",
        dest="create_corporation",
        action="store_false",
        default=True,
        help="don't create the Synsation Corporation locations and assets",
    )
    parser.add_argument(
        "-M",
        "--no-manufacturing",
        dest="create_manufacturing",
        action="store_false",
        default=True,
        help="don't create the Synsation Manufacturing locations and assets",
    )
    parser.add_argument(
        "-I",
        "--no-industries",
        dest="create_industries",
        action="store_false",
        default=True,
        help="don't create the Synsation Industries locations and assets",
    )
    parser.add_argument(
        "-S",
        "--no-smartcity",
        dest="create_smartcity",
        action="store_false",
        default=True,
        help="don't create the Synsation Smart City locations and assets",
    )
    parser.add_argument(
        "-n",
        "--num-assets",
        type=int,
        dest="num_assets",
        action="store",
        default=50,
        help="total number of assets to create in Synsation Corporation",
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        dest="wait",
        action="store",
        default=0.0,
        help="add a delay between API calls (corporation only)",
    )
    parser.add_argument(
        "--await-confirmation",
        dest="await_confirmation",
        action="store_true",
        default=False,
        help="wait for all assets to be confirmed before exit",
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
