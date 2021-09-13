#   Copyright 2020 Jitsuin, inc
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

#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

import logging
from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist.parser import common_parser

from ..testing.parser import common_endpoint

from .run import run

LOGGER = logging.getLogger(__name__)


def main():
    parser, _ = common_parser("Exercises the various Wavestone door entry use cases")
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default=None,
        help="namespace of item population (to enable parallel demos",
    )

    parser.add_argument(
        "-W",
        "--no-wait",
        dest="wait_for_confirmation",
        action="store_false",
        default=True,
        help="do not wait for assets to confirm before exiting (-z only)",
    )

    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument(
        "-z",
        "--create",
        dest="create_assets",
        action="store_true",
        default=False,
        help="create the locations and assets. DO THIS ONLY ONCE.",
    )
    operations.add_argument(
        "-l",
        "--list",
        type=str,
        dest="listspec",
        action="store",
        help=(
            "List assets and usage of assets. "
            "Use 'all', 'doors', 'cards' or asset_id. "
            "Case-sensitive."
        ),
    )
    operations.add_argument(
        "-o",
        "--open-door",
        type=lambda d: d.split(","),
        dest="doorid_cardid",
        action="store",
        default="",
        help='open "door_id" with "card_id"',
    )

    args = parser.parse_args()

    poc = common_endpoint("door_entry", args)

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
