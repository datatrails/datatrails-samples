#   Copyright 2021 Jitsuin, inc
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


from sys import exit as sys_exit
from sys import stdout as sys_stdout

from archivist.archivist import Archivist

from ..testing.logger import set_logger, LOGGER
from ..testing.parser import common_parser

from .run import run


def main():
    parser, _ = common_parser(
        "Simple SBOM implementation that conforms with NTIA recommendations"
    )
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default=None,
        help="namespace of item population (to enable parallel demos",
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
        "_".join(["sbom", args.namespace]) if args.namespace is not None else "sbom"
    )
    poc.storage_integrity = args.storage_integrity

    run(poc)

    parser.print_help(sys_stdout)
    sys_exit(1)
