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

"""Convenience layer that ensures that assets and locations are created, read or
   counted for a particular namespace
"""

# pylint:  disable=missing-docstring

from copy import deepcopy
from yaml import full_load

from archivist.errors import (
    ArchivistNotFoundError,
)


NAMESPACE_KEY = "functests_namespace"


# NB: this is not namespaced and cannot be namespaced until we get GRP2.0
#     and a proto definition with suitable attributes
def attachments_upload_from_file(arch, name, mtype):
    with open(name, "rb") as fd:
        attachment = arch.attachments.upload(fd, mtype=mtype)

    return attachment


def locations_create_from_yaml_file(arch, name):
    """Load location from yaml file

    assumes there is only one document in the file.
    """
    with open(name, "r") as fd:
        data = full_load(fd)
        attrs = data["attributes"]
        del data["attributes"]
        return locations_create_if_not_exists(arch, data, attrs=attrs)


def __newattrs(arch, attrs):
    newattrs = deepcopy(attrs or {})
    if arch.namespace is not None:
        newattrs[NAMESPACE_KEY] = arch.namespace
    return newattrs


def locations_read_by_signature(arch, props, *, attrs=None):
    return arch.locations.read_by_signature(props=props, attrs=__newattrs(arch, attrs))


def locations_list(arch, *, props=None, attrs=None):
    return arch.locations.list(props=props, attrs=__newattrs(arch, attrs))


def locations_create(arch, props, attrs):
    return arch.locations.create(props, attrs=__newattrs(arch, attrs))


def locations_create_if_not_exists(arch, props, *, attrs=None):
    location = None
    try:
        location = locations_read_by_signature(
            arch,
            {
                "display_name": props["display_name"],
            },
        )
    except ArchivistNotFoundError:
        location = locations_create(arch, props, attrs=attrs)

    return location


def assets_count(arch, attrs):
    return arch.assets.count(attrs=__newattrs(arch, attrs))


def assets_list(arch, *, attrs=None):
    return arch.assets.list(attrs=__newattrs(arch, attrs))


def assets_read_by_signature(arch, attrs):
    return arch.assets.read_by_signature(attrs=__newattrs(arch, attrs))


def assets_create(arch, behaviours, attrs, *, confirm=None):
    return arch.assets.create(behaviours, __newattrs(arch, attrs), confirm=confirm)


def assets_wait_for_confirmed(arch, attrs):
    arch.assets.wait_for_confirmed(attrs=__newattrs(arch, attrs))


def events_create(arch, asset_id, props, attrs, *, asset_attrs=None, confirm=None):
    return arch.events.create(
        asset_id,
        props,
        __newattrs(arch, attrs),
        asset_attrs=asset_attrs,
        confirm=confirm,
    )


def events_list(arch, asset_id, attrs=None):
    return arch.events.list(asset_id=asset_id, attrs=__newattrs(arch, attrs))


def events_count(arch, asset_id, attrs=None):
    return arch.events.count(asset_id=asset_id, attrs=__newattrs(arch, attrs))
