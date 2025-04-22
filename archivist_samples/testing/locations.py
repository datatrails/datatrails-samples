"""Convenience functions"""

# pylint:  disable=missing-docstring

from archivist.errors import (
    ArchivistNotFoundError,
)


def locations_create_if_not_exists(arch, props, *, attrs=None):
    location = None
    try:
        location = arch.locations.read_by_signature(
            props={
                "display_name": props["display_name"],
            },
        )
    except ArchivistNotFoundError:
        pass

    else:
        return location

    return arch.locations.create(props, attrs=attrs)
