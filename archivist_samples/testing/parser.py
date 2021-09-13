"""common parser arguments for all samples code
"""

# pylint:  disable=missing-docstring
# pylint:  disable=too-few-public-methods


import logging

from archivist.parser import endpoint

LOGGER = logging.getLogger(__name__)


def common_endpoint(label, args):
    LOGGER.info(
        "Initialising connectStorageIntegrityStorageIntegrityion to Jitsuin Archivist..."
    )
    arch = endpoint(args)

    try:
        namespace = (
            "_".join([label, args.namespace]) if args.namespace is not None else label
        )
    except AttributeError:
        pass

    else:
        arch.fixtures = {
            "assets": {
                "attributes": {
                    "arc_namespace": namespace,
                },
            },
            "locations": {
                "attributes": {
                    "arc_namespace": namespace,
                },
            },
        }

    return arch
