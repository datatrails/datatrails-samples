"""Convenience functions
"""

# pylint:  disable=missing-docstring

from dataclasses import dataclass
import logging
from typing import Callable, Dict, List, Optional
from archivist import archivist as type_helper

from archivist.errors import ArchivistNotFoundError
from .locations import locations_create_if_not_exists

LOGGER = logging.getLogger(__name__)


@dataclass
class AttachmentDescription:
    filename: str
    attribute_name: str


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


def make_assets_create(
    attachment_creator: Optional[
        Callable[[type_helper.Archivist, AttachmentDescription], Dict]
    ] = None,
    confirm=False,
):
    """
    Creates a general function that creates an asset with a location
    and a list of attachments but only if the asset does not already exist.

    the argument is the method that creates an attachment of the form
         attachment_create(arch, ("filename", "display_name"))
    """

    def assets_create(
        arch,
        displayname,
        asset_attrs,
        *,
        location=None,
        attachments: Optional[List[AttachmentDescription]] = None,
    ):
        asset = None
        existed = False
        try:
            asset = arch.assets.read_by_signature(
                attrs={
                    "arc_display_name": displayname,
                },
            )

        except ArchivistNotFoundError:
            LOGGER.info("%s does not exist", displayname)
            asset_attrs["arc_display_name"] = displayname
            if location is not None:
                location = locations_create_if_not_exists(
                    arch,
                    location["props"],
                    attrs=location["attrs"],
                )
                asset_attrs["arc_home_location_identity"] = location["identity"]

            if attachments is not None and attachment_creator is not None:
                for attachment in attachments:
                    attachment_attr = attachment_creator(arch, attachment)
                    asset_attrs[attachment.attribute_name] = attachment_attr

            LOGGER.debug("asset_attrs %s", asset_attrs)
            asset = arch.assets.create(
                attrs=asset_attrs,
                confirm=confirm,
            )

        else:
            LOGGER.info("%s already existed", displayname)
            existed = True

        return asset, existed

    return assets_create
