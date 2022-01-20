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
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    synsation_corporation.initialise_all(arch, 10, True)
    synsation_industries.initialise_all(arch)
    synsation_manufacturing.initialise_all(arch)
    synsation_smartcity.initialise_all(arch)

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
        default=None,
        help="namespace of item population (to enable parallel demos",
    )

    args = parser.parse_args()

    arch = common_endpoint("synsation", args)

    run(arch, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
