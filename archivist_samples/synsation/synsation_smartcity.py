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

# Definitions and data for Synsation Smart City demo data

# pylint: disable=missing-docstring

import logging

from ..testing.assets import assets_create_if_not_exists

from .util import asset_attachment_upload_from_file

LOGGER = logging.getLogger(__name__)


def initialise_asset_types(ac):
    type_map = {}

    newattachment = asset_attachment_upload_from_file(
        ac, "outdoor_cctv.jpg", "image/jpg"
    )
    type_map["Outdoor security camera"] = newattachment

    newattachment = asset_attachment_upload_from_file(
        ac, "traffic_light_with_violation_camera.jpg", "image/jpg"
    )
    type_map["Traffic light with violation camera"] = newattachment

    newattachment = asset_attachment_upload_from_file(
        ac, "traffic_light.jpg", "image/jpg"
    )
    type_map["Traffic light"] = newattachment

    newattachment = asset_attachment_upload_from_file(
        ac, "street_light_controller.jpg", "image/jpg"
    )
    type_map["Street light controller"] = newattachment

    newattachment = asset_attachment_upload_from_file(
        ac, "outdoor_air_quality_meter.jpg", "image/jpg"
    )
    type_map["Outdoor air quality meter"] = newattachment

    LOGGER.debug(type_map)

    return type_map


def create_smartcity_device(
    ac, locationid, displayname, displaytype, serial, description, image
):
    attrs = {
        "arc_firmware_version": "1.0",
        "arc_serial_number": serial,
        "arc_display_name": displayname,
        "arc_description": description,
        "arc_home_location_identity": locationid,
        "arc_display_type": displaytype,
        "arc_attachments": [
            {
                "arc_display_name": "arc_primary_image",
                "arc_attachment_identity": image["identity"],
                "arc_hash_value": image["hash"]["value"],
                "arc_hash_alg": image["hash"]["alg"],
            }
        ],
    }
    newasset = assets_create_if_not_exists(ac, attrs)
    LOGGER.debug(newasset)
    return newasset


def create_newmarketroad_roundabout(ac, asset_types):
    # Parkside junction has:
    #  - 4-way traffic lights with red light violation cameras
    #  - 2 general CCTV stand
    #  - 2 streetlight controller
    props = {
        "display_name": "Newmarket Road Roundabout",
        "description": (
            "Circulatory intersection between Newmarket " "Road and East Road"
        ),
        "latitude": 52.208479,
        "longitude": 0.137648,
    }
    attrs = {
        "intersection_type": "roundabout",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    LOGGER.debug(newlocation)
    location_identity = newlocation["identity"]

    create_smartcity_device(
        ac,
        location_identity,
        "tcl.nmr.n01",
        "Traffic light with violation camera",
        "vtl-x4-01",
        "Traffic flow control light at Newmarket Road East entrance",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.nmr.002",
        "Traffic light with violation camera",
        "vtl-x4-02",
        "Traffic flow control light at A1134 West entrance",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.nmr.003",
        "Traffic light with violation camera",
        "vtl-x4-03",
        "Traffic flow control light at A603 South entrance",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.nmr.004",
        "Traffic light with violation camera",
        "vtl-x4-04",
        "Traffic flow control light at A1134 North entrance",
        asset_types["Traffic light with violation camera"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "cctv-01-01",
        "Outdoor security camera",
        "gmr-123-01",
        "East-facing camera surveying Newmarket Road",
        asset_types["Outdoor security camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "cctv-01-02",
        "Outdoor security camera",
        "gmr-123-02",
        "West-facing camera surveying East Road",
        asset_types["Outdoor security camera"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c022",
        "Street light controller",
        "ssl-a4l-01",
        "Street light controller for column ID 22c022",
        asset_types["Street light controller"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c023",
        "Street light controller",
        "ssl-a4l-02",
        "Street light controller for column ID 22c023",
        asset_types["Street light controller"],
    )


def create_parkside_junction(ac, asset_types):
    # Parkside junction has:
    #  - 4-way traffic lights with red light violation cameras
    #  - 1 general CCTV stand
    #  - 1 streetlight controller
    props = {
        "display_name": "Parkside Junction",
        "description": "Box intersection between Mill Road and East Road",
        "latitude": 52.202502,
        "longitude": 0.131148,
    }
    attrs = {
        "intersection_type": "box",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    location_identity = newlocation["identity"]

    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ppj.n01",
        "Traffic light with violation camera",
        "vtl-x4-05",
        "Traffic flow control light at Mill Road South East",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ppj.002",
        "Traffic light with violation camera",
        "vtl-x4-06",
        "Traffic flow control light at Parkside North West",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ppj.003",
        "Traffic light with violation camera",
        "vtl-x4-07",
        "Traffic flow control light at A603 North East",
        asset_types["Traffic light with violation camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ppj.004",
        "Traffic light with violation camera",
        "vtl-x4-08",
        "Traffic flow control light at A603 South West",
        asset_types["Traffic light with violation camera"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "cctv-02-01",
        "Outdoor security camera",
        "gmr-123-03",
        "Camera surveying the skate park",
        asset_types["Outdoor security camera"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c010",
        "Street light controller",
        "ssl-a4l-03",
        "Street light controller for column ID 22c010",
        asset_types["Street light controller"],
    )


def create_drummerstreet_terminal(ac, asset_types):
    # Drummer Street Bus Terminal has:
    #  - 1 traffic light
    #  - 4 general CCTV stand
    #  - 4 streetlight controller
    #  - 1 air quality meter
    props = {
        "display_name": "Drummer Street Terminal",
        "description": "Drummer Street Bus Terminal",
        "latitude": 52.205345,
        "longitude": 0.123922,
    }
    attrs = {
        "intersection_type": "terminal",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    location_identity = newlocation["identity"]

    create_smartcity_device(
        ac,
        location_identity,
        "tcl.dst.n01",
        "Traffic light",
        "tl-x1-01",
        "Traffic flow control light at terminal entrance",
        asset_types["Traffic light"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "cctv-03-01",
        "Outdoor security camera",
        "gmr-123-04",
        "South-facing shelter camera",
        asset_types["Outdoor security camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "cctv-03-02",
        "Outdoor security camera",
        "gmr-123-05",
        "North-facing shelter camera",
        asset_types["Outdoor security camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "cctv-03-03",
        "Outdoor security camera",
        "gmr-123-06",
        "Safety camera surveying turning area",
        asset_types["Outdoor security camera"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "cctv-04-04",
        "Outdoor security camera",
        "gmr-123-07",
        "Safety camera surveying public lavatories",
        asset_types["Outdoor security camera"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c106",
        "Street light controller",
        "ssl-a4l-04",
        "Street light controller for column ID 22c106",
        asset_types["Street light controller"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c108",
        "Street light controller",
        "ssl-a4l-05",
        "Street light controller for column ID 22c108",
        asset_types["Street light controller"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c110",
        "Street light controller",
        "ssl-a4l-06",
        "Street light controller for column ID 22c110",
        asset_types["Street light controller"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c112",
        "Street light controller",
        "ssl-a4l-07",
        "Street light controller for column ID 22c112",
        asset_types["Street light controller"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "airqualmet00",
        "Outdoor air quality meter",
        "tm-1417-a61",
        "Pedstrian safety air quality meter at Drummer Street bus shelter",
        asset_types["Outdoor air quality meter"],
    )


def create_catholicchurch_junction(ac, asset_types):
    # Catholic Church Junction has:
    #  - 4-way traffic light
    #  - 1 streetlight controller
    #  - 1 air quality monitor
    props = {
        "display_name": "Catholic Church Junction",
        "description": (
            "Junction of Lensfield Road and Hills Road at the "
            "Church of Our Lady and the English Martyrs"
        ),
        "latitude": 52.199308,
        "longitude": 0.127378,
    }
    attrs = {
        "intersection_type": "cross",
    }
    newlocation = ac.locations.create(props, attrs=attrs)
    location_identity = newlocation["identity"]

    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ccj.001",
        "Traffic light",
        "vtl-x4-05",
        "Traffic flow control light at Hills Road South East",
        asset_types["Traffic light"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ccj.002",
        "Traffic light",
        "vtl-x4-06",
        "Traffic flow control light at Regent Street North West",
        asset_types["Traffic light"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ccj.003",
        "Traffic light",
        "vtl-x4-07",
        "Traffic flow control light at A603 North East",
        asset_types["Traffic light"],
    )
    create_smartcity_device(
        ac,
        location_identity,
        "tcl.ccj.004",
        "Traffic light",
        "vtl-x4-08",
        "Traffic flow control light at A603 South West",
        asset_types["Traffic light"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "lighting.street.22c045",
        "Street light controller",
        "ssl-a4l-08",
        "Street light controller for column ID 22c045",
        asset_types["Street light controller"],
    )

    create_smartcity_device(
        ac,
        location_identity,
        "airqualmet01",
        "Outdoor air quality meter",
        "tm-1416-a61",
        (
            "Pedstrian safety air quality meter at the Church of "
            "Our Lady and the English Martyrs"
        ),
        asset_types["Outdoor air quality meter"],
    )


def initialise_all(ac):
    LOGGER.info("Creating data for Synsation Services Smart City...")
    # Unlike the others, the smartcity scenario is not randomly created
    # and distributed, and does not allow changing the number of locations
    # and so on.  Everything is planned and fixed in place
    asset_types = initialise_asset_types(ac)

    create_newmarketroad_roundabout(ac, asset_types)
    create_parkside_junction(ac, asset_types)
    create_drummerstreet_terminal(ac, asset_types)
    create_catholicchurch_junction(ac, asset_types)

    LOGGER.info("Smart City data initialized")
