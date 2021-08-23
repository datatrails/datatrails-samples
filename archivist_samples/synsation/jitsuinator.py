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


import datetime
from sys import exit as sys_exit
from sys import stdout as sys_stdout
import time
import uuid

from archivist import about
from archivist.errors import ArchivistNotFoundError

from ..testing.asset import MyAsset
from ..testing.logger import set_logger, LOGGER
from ..testing.parser import common_parser, common_endpoint
from ..testing.time_warp import TimeWarp

from .util import attachment_upload_from_file


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

    cve_id = "CVE2020-deadbeef"
    MyAsset(ac, asset_id, tw, "Brian@WhiteHatHackers.io",).report_vulnerability(
        (
            f"Synsation Industries {asset_type}s are vulnerable "
            f"to {cve_id}. Upgrade as soon as possible."
        ),
        cve_id,
        cve_corval,
    )

    # -> OEM fixes it and issues the patch
    if wait:
        time.sleep(wait)
        LOGGER.info("OEM patch...")
    else:
        input("Press to enact OEM issue patch")

    MyAsset(ac, asset_id, tw, "Releases@SynsationIndustries.com",).patch_vulnerability(
        f"Patch for critical vulnerability '{cve_id}' released in version 1.6",
        (
            "SHA256-sum for official 1.6 release: "
            "68ada47318341d060c387a765dd854b57334ab1f7322d22c155428414feb7518"
        ),
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

    MyAsset(ac, asset_id, tw, "Releases@SynsationIndustries.com",).certify_patch(
        "Safety conformance approved for version 1.6. See attached conformance report",
        "DVA Conformance Report attached",
        {
            "arc_primary_image_identity": iattachment["identity"],
            "arc_attachments": [
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
            ],
        },
        extra_attrs={"synsation_conformance_report": rattachment["identity"]},
    )

    # -> Owner accepts new version and issues maintenance request to have it installed
    if wait:
        time.sleep(wait)
        LOGGER.info("Owner approval...")
    else:
        input("Press to enact Owner approves")

    MyAsset(ac, asset_id, tw, "Legal@SmartCity.fr",).service_required(
        "Version 1.6 accepted. Please install ASAP",
        job_corval,
    )

    # -> Operator schedules downtime and patches it
    if wait:
        time.sleep(wait)
        LOGGER.info("Maintenance and patch...")
    else:
        input("Press to enact Maintenance")

    MyAsset(ac, asset_id, tw, "Phil@SynsationServicing.com",).service(
        f"Upgraded and restarted {asset_type} during safe downtime window",
        job_corval,
    )

    MyAsset(ac, asset_id, tw, "otaService@SynsationServicing.com",).update_firmware(
        "Responding to vulnerability 'CVE2020-deadbeef' with patch 'v1.6'",
        "1.6",
        cve_corval,
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
        asset = ac.assets.read_by_signature(
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
    parser, _ = common_parser("Runs the Jitsuinator demo script manually")
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

    args = parser.parse_args()

    if args.verbose:
        set_logger("DEBUG")
    else:
        set_logger("INFO")

    poc = common_endpoint("synsation", args)
    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
