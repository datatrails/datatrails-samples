#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from ..testing.archivist_parser import common_parser
from ..testing.parser import common_endpoint

from .run import run

LOGGER = logging.getLogger(__name__)


def main():
    parser = common_parser("Sample Waste Isolation Pilot Plant (WIPP) Integration")
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default="wipp",
        help="namespace of item population (to enable parallel demos)",
    )

    args = parser.parse_args()

    poc = common_endpoint("wipp", args)

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
