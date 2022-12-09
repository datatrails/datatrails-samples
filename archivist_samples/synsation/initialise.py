# WARNING: Proof of concept code: Not for release

"""Initialise dataset for synsation"""

# pylint:  disable=missing-docstring

import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist import about

from ..testing.archivist_parser import common_parser
from ..testing.parser import common_endpoint

from . import synsation_corporation
from . import synsation_industries
from . import synsation_manufacturing
from . import synsation_smartcity

LOGGER = logging.getLogger(__name__)


# Main app
##########


def run(arch, args):
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    if args.create_corporation:
        synsation_corporation.initialise_all(arch, args.num_assets, args.wait)

    if args.create_industries:
        synsation_industries.initialise_all(arch)

    if args.create_manufacturing:
        synsation_manufacturing.initialise_all(arch)

    if args.create_smartcity:
        synsation_smartcity.initialise_all(arch)

    # Wait for all assets to confirm before we do anything with them
    if args.await_confirmation:
        LOGGER.info("Wait for confirmation")
        arch.assets.wait_for_confirmed()

    sys_exit(0)


def entry():
    parser = common_parser("Populates a clean RKVST tenancy with Synsation test data")
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default="synsation",
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

    args = parser.parse_args()

    arch = common_endpoint("synsation", args)

    run(arch, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
