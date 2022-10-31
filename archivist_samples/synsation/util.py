# WARNING: Proof of concept code: Not for release


# pylint:  disable=missing-docstring

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from yaml import full_load

from . import images, locations
from .images import assets as images_assets

from ..testing.locations import (
    locations_create_if_not_exists,
)


def asset_attachment_upload_from_file(arch, name, mtype):
    with pkg_resources.open_binary(images_assets, name) as fd:
        attachment = arch.attachments.upload(fd, mtype=mtype)

    return attachment


def attachment_upload_from_file(arch, name, mtype):
    with pkg_resources.open_binary(images, name) as fd:
        attachment = arch.attachments.upload(fd, mtype=mtype)

    return attachment


def locations_create_from_yaml_file(arch, name):
    """Load location from yaml file

    assumes there is only one document in the file.
    """
    with pkg_resources.open_binary(locations, name) as fd:
        data = full_load(fd)
        attrs = data["attributes"]
        del data["attributes"]
        return locations_create_if_not_exists(arch, data, attrs=attrs)


def locations_from_yaml_file(name):
    """Load location from yaml file

    assumes there is only one document in the file.
    """
    with pkg_resources.open_binary(locations, name) as fd:
        data = full_load(fd)
        attrs = data["attributes"]
        del data["attributes"]
        return {
            "props": data,
            "attrs": attrs,
        }
