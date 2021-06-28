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

from archivist.errors import ArchivistNotFoundError

from ..testing.namespace import (
    assets_create,
    assets_read_by_signature,
    attachments_upload_from_file,
)


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


def attachments_read_from_file(arch, name, mtype):
    return attachments_upload_from_file(
        arch, f"archivist_samples/synsation/images/{name}", mtype
    )


def assets_create_if_not_exists(arch, behaviours, attrs, *, confirm=None):
    asset = None
    try:
        asset = assets_read_by_signature(
            arch,
            {
                "arc_display_name": attrs["arc_display_name"],
            },
        )
    except ArchivistNotFoundError:
        asset = assets_create(arch, behaviours, attrs, confirm=confirm)

    return asset
