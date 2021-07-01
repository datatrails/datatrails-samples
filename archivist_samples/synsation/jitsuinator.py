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

"""Jitsuinator"""

# pylint:  disable=missing-docstring
# pylint:  disable=too-many-statements


import argparse
import datetime
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import time
import uuid

from archivist import about
from archivist.archivist import Archivist
from archivist.errors import ArchivistNotFoundError
from archivist.timestamp import make_timestamp

from ..testing.logger import set_logger, LOGGER
from ..testing.namespace import (
    assets_read_by_signature,
    events_create,
)
from ..testing.time_warp import TimeWarp

from .util import make_event_json, attachment_upload_from_file


def demo_flow(ac, asset_id, asset_type, tw, wait):
    # Demo flow:
    # -> Asset is created, nothing to see here
    # -> White hat hacker reports vulnerability
    # -> OEM fixes it and issues the patch
    # -> Integrator approves the patch and issues new safety certificate
    # -> Owner accepts new version and issues maintenance request to have
    #    it installed by the operator
    # -> Operator schedules downtime and patches it
    # -> All is well

    job_corval = str(uuid.uuid4())
    cve_corval = str(uuid.uuid4())

    # -> Asset is created, nothing to see here
    # -> White hat hacker reports vulnerability
    if wait:
        time.sleep(wait)
        LOGGER.info("White Hat Hacker...")
    else:
        input("Press to enact White Hat Hacker")

    recall_msg = (
        f"Synsation Industries {asset_type}s are vulnerable "
        f"to CVE2020-deadbeef. Upgrade as soon as possible."
    )
    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "Firmware",
        "Vulnerability",
        dtstring,
        "Brian@WhiteHatHackers.io",
        "FW Vulnerability",
        recall_msg,
        cve_corval,
    )
    attrs["arc_cve_id"] = "CVE2020-deadbeef"

    events_create(
        ac,
        asset_id,
        props,
        attrs,
        confirm=True,
    )

    # -> OEM fixes it and issues the patch
    if wait:
        time.sleep(wait)
        LOGGER.info("OEM patch...")
    else:
        input("Press to enact OEM issue patch")

    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "RecordEvidence",
        "Record",
        dtstring,
        "Releases@SynsationIndustries.com",
        "Config Management",
        "Patch for critical vulnerability 'CVE2020-deadbeef' released in version 1.6",
        "",
    )
    attrs["arc_evidence"] = (
        "SHA256-sum for official 1.6 release: "
        "68ada47318341d060c387a765dd854b57334ab1f7322d22c155428414feb7518"
    )
    events_create(
        ac,
        asset_id,
        props,
        attrs,
        confirm=True,
    )

    # -> Integrator approves the patch and issues new safety certificate
    if wait:
        time.sleep(wait)
        LOGGER.info("Integrator approval...")
    else:
        input("Press to enact Integrator approves")

    iattachment = attachment_upload_from_file(
        ac, "trafficlightconformance.png", "image/png"
    )
    rattachment = attachment_upload_from_file(
        ac, "trafficlightconformance.pdf", "application/pdf"
    )

    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "RecordEvidence",
        "Record",
        dtstring,
        "DesignAuthority@Integrator.com",
        "Config Management",
        "Safety conformance approved for version 1.6. See attached conformance report",
        "",
    )
    attrs["arc_evidence"] = "DVA Conformance Report attached"
    attrs["synsation_conformance_report"] = rattachment["identity"]
    attrs["arc_primary_image_identity"] = iattachment["identity"]
    attrs["arc_attachments"] = [
        {
            "arc_display_name": "arc_primary_image",
            "arc_attachment_identity": iattachment["identity"],
            "arc_hash_value": iattachment["hash"]["value"],
            "arc_hash_alg": iattachment["hash"]["alg"],
        },
        {
            "arc_display_name": "Conformance Report",
            "arc_attachment_identity": rattachment["identity"],
            "arc_hash_value": rattachment["hash"]["value"],
            "arc_hash_alg": rattachment["hash"]["alg"],
        },
    ]
    events_create(
        ac,
        asset_id,
        props,
        attrs,
        confirm=True,
    )

    # -> Owner accepts new version and issues maintenance request to have it installed
    if wait:
        time.sleep(wait)
        LOGGER.info("Owner approval...")
    else:
        input("Press to enact Owner approves")

    maint_msg = "Version 1.6 accepted. Please install ASAP"
    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "Maintenance",
        "MaintenanceRequired",
        dtstring,
        "Legal@SmartCity.fr",
        "Service RQ",
        maint_msg,
        job_corval,
    )
    events_create(
        ac,
        asset_id,
        props,
        attrs,
        confirm=True,
    )

    # -> Operator schedules downtime and patches it
    if wait:
        time.sleep(wait)
        LOGGER.info("Maintenance and patch...")
    else:
        input("Press to enact Maintenance")

    maint_msg = f"Upgraded and restarted {asset_type} during safe downtime window"
    notnow = tw.now()
    dtstring = make_timestamp(notnow)
    props, attrs = make_event_json(
        "Maintenance",
        "Maintenance",
        dtstring,
        "Phil@SynsationServicing.com",
        "Service RP",
        maint_msg,
        job_corval,
    )
    events_create(
        ac,
        asset_id,
        props,
        attrs,
        confirm=True,
    )

    patch_msg = "Responding to vulnerability 'CVE2020-deadbeef' with patch 'v1.6'"
    props, attrs = make_event_json(
        "Firmware",
        "Update",
        dtstring,
        "otaService@SynsationServicing.com",
        "FW Update",
        patch_msg,
        cve_corval,
    )
    attrs["arc_firmware_version"] = "1.6"
    asset_attrs = {}
    asset_attrs["arc_firmware_version"] = "1.6"
    events_create(
        ac,
        asset_id,
        props,
        attrs,
        asset_attrs=asset_attrs,
        confirm=True,
    )

    # -> All is well
    LOGGER.info("Done")


# Main app
##########


def run(ac, args):
    """logic goes here"""
    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    LOGGER.info("Looking for asset...")
    try:
        asset = assets_read_by_signature(
            ac,
            attrs={"arc_display_name": args.asset_name},
        )
    except ArchivistNotFoundError:
        LOGGER.info("Asset not found.  Aborting.")
        sys_exit(1)

    asset_id = asset["identity"]
    attrs = asset["attributes"]
    asset_type = attrs["arc_display_type"] if "arc_display_type" in attrs else "Device"

    LOGGER.info("Creating time warp...")
    tw = TimeWarp(args.start_date, args.fast_forward)

    LOGGER.info("Beginning simulation...")
    demo_flow(ac, asset_id, asset_type, tw, args.wait)

    LOGGER.info("Done.")
    sys_exit(0)


def entry():
    parser = argparse.ArgumentParser(
        description="Runs the Jitsuinator demo script manually"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="print verbose debugging",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        dest="url",
        action="store",
        default="https://rkvst.poc.jitsuin.io",
        help="location of Archivist service",
    )
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default=None,
        help="namespace of item population (to enable parallel demos",
    )

    parser.add_argument(
        "-n",
        "--asset_name",
        type=str,
        dest="asset_name",
        action="store",
        default="tcl.ccj.01",
        help="Name of the asset to ship",
    )
    parser.add_argument(
        "-s",
        "--start-date",
        type=lambda d: datetime.datetime.strptime(d, "%Y%m%d"),
        dest="start_date",
        action="store",
        default=datetime.date.today() - datetime.timedelta(days=1),
        help="Start date for event series (format: yyyymmdd)",
    )
    parser.add_argument(
        "-f",
        "--fast-forward",
        type=float,
        dest="fast_forward",
        action="store",
        default=3600,
        help="Fast forward time in event series (default: 1 second = 1 hour)",
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        dest="wait",
        action="store",
        default=0.0,
        help="auto-advance after WAIT seconds",
    )

    security = parser.add_mutually_exclusive_group(required=True)
    security.add_argument(
        "-t",
        "--auth-token",
        type=str,
        dest="auth_token_file",
        action="store",
        default=".auth_token",
        help="FILE containing API authentication token",
    )
    security.add_argument(
        "-c",
        "--clientcert",
        type=str,
        dest="client_cert_name",
        action="store",
        help=(
            "name of TLS client cert (.key and .pem with matching name"
            "must be in current directory)"
        ),
    )

    args = parser.parse_args()

    if args.verbose:
        set_logger("DEBUG")
    else:
        set_logger("INFO")

    # Initialise connection to Archivist
    LOGGER.info("Initialising connection to Jitsuin Archivist...")
    if args.auth_token_file:
        with open(args.auth_token_file, mode="r") as tokenfile:
            authtoken = tokenfile.read().strip()

        poc = Archivist(args.url, auth=authtoken, verify=False)

    elif args.client_cert_name:
        poc = Archivist(args.url, cert=args.client_cert_name, verify=False)

    if poc is None:
        LOGGER.error("Critical error.  Aborting.")
        sys_exit(1)

    poc.namespace = (
        "_".join(["synsation", args.namespace]) if args.namespace is not None else None
    )

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
