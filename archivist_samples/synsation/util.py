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
# Copies the flow of the Jitsuinator demo script


# pylint:  disable=missing-docstring

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from yaml import full_load

from . import images, locations
from .images import assets as images_assets

from ..testing.namespace import (
    locations_create_if_not_exists,
)


# NB: this is not namespaced and cannot be namespaced until we get GRP2.0
#     and a proto definition with suitable attributes
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


def make_event_json(
    event_behaviour, event_op, when_str, who_str, what_str, msg_str, corval
):
    """Create a simple Archivist event payload"""
    props = {
        "operation": event_op,
        "behaviour": event_behaviour,
        "principal_declared": {
            "issuer": "job.idp.server/1234",
            "subject": who_str,
            "display_name": who_str,
        },
        "timestamp_declared": when_str,
    }
    attrs = {
        "arc_display_type": what_str,
        "arc_description": msg_str,
        "arc_correlation_value": corval,
    }
    return props, attrs
