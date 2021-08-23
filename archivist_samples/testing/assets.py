"""Convenience functions
"""

# pylint:  disable=missing-docstring

from archivist.errors import (
    ArchivistNotFoundError,
)


def assets_create_if_not_exists(arch, attrs, *, confirm=False):
    asset = None
    try:
        asset = arch.assets.read_by_signature(
            attrs={
                "arc_display_name": attrs["arc_display_name"],
            },
        )
    except ArchivistNotFoundError:
        # The backoff module we use seems to inherit the exception
        # raised here so we execute the assets_create outside of this
        # exception handler
        pass

    else:
        return asset

    return arch.assets.create(attrs=attrs, confirm=confirm)
