"""Convenience functions"""

# pylint:  disable=missing-docstring

from dataclasses import dataclass
import logging
from typing import Callable, Dict, List, Optional
from archivist import archivist as type_helper

from archivist.errors import ArchivistNotFoundError

LOGGER = logging.getLogger(__name__)


@dataclass
class AttachmentDescription:
    filename: str
    attribute_name: str


def assets_create_if_not_exists(arch, attrs):
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

    return arch.assets.create(attrs=attrs)


def make_assets_create(
    attachment_creator: Optional[
        Callable[[type_helper.Archivist, AttachmentDescription], Dict]
    ] = None,
    public=False,
):
    """
    Creates a general function that creates an asset
    and a list of attachments but only if the asset does not already exist.

    By default the selector for, if the asset already exists, is the `arc_display_name`.
    But passing in `selector_key` and `selector_value` to the returned
    function allows for a custom selector.

    the argument is the method that creates an attachment of the form
         attachment_create(arch, ("filename", "display_name"))
    """

    def assets_create(
        arch,
        display_name,
        asset_attrs,
        *,
        attachments: Optional[List[AttachmentDescription]] = None,
        selector_key="arc_display_name",
        selector_value=None
    ):
        asset = None
        existed = False

        # by default use the display name as the selector value
        if selector_value is None:
            selector_value = display_name

        try:
            asset = arch.assets.read_by_signature(
                attrs={
                    selector_key: selector_value,
                },
            )

        except ArchivistNotFoundError:
            asset_attrs["arc_display_name"] = display_name
            if attachments is not None and attachment_creator is not None:
                for attachment in attachments:
                    attachment_attr = attachment_creator(arch, attachment)
                    asset_attrs[attachment.attribute_name] = attachment_attr

            # add the selector for the next run
            if selector_key != "arc_display_name" and selector_value is not None:
                asset_attrs[selector_key] = selector_value

            LOGGER.debug("asset_attrs %s", asset_attrs)
            asset = arch.assets.create(attrs=asset_attrs, props={"public": public})

        else:
            LOGGER.info("%s already existed", display_name)
            existed = True

        return asset, existed

    return assets_create
