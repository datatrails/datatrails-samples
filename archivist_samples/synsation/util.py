# WARNING: Proof of concept code: Not for release


# pylint:  disable=missing-docstring

import importlib.resources as res

from . import images
from .images import assets as images_assets


def asset_attachment_upload_from_file(arch, name, mtype):
    with res.files(images_assets).joinpath(name).open("rb") as fd:
        attachment = arch.attachments.upload(fd, mtype=mtype)

    return attachment


def attachment_upload_from_file(arch, name, mtype):
    with res.files(images).joinpath(name).open("rb") as fd:
        attachment = arch.attachments.upload(fd, mtype=mtype)

    return attachment
