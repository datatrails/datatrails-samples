#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

import logging

from ..testing.archivist_parser import common_parser
from ..testing.parser import common_endpoint

from .run import run

LOGGER = logging.getLogger(__name__)


def main():
    parser = common_parser("Document Sample")
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default="document",
        help="namespace of item population (to enable parallel demos)",
    )

    args = parser.parse_args()

    poc = common_endpoint("document", args)

    run(poc, args)
