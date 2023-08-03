#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring
# pylint:  disable=too-many-statements

import logging

from sys import exit as sys_exit
from archivist import about

from .wipp import Wipp, upload_attachment
from ..testing.assets import AttachmentDescription

LOGGER = logging.getLogger(__name__)


def run_cask(arch, args):
    """
    Run the sample, only creating the cask asset
    """
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # Cask Asset
    LOGGER.info("Creating Cask Asset...")
    caskname = "Cask"

    cask = Wipp(arch, "TRU RH 72B Cask")
    cask.create(
        caskname,
        "NRC certified type-B road shipping container, capacity 3 x 55-gallon drum",
        args.namespace,
        attachments=[AttachmentDescription("rh72b.png", "arc_primary_image")],
        custom_attrs={"wipp_capacity": "3", "OnboardingSampleID": "NuclearWIPP"},
    )
    if cask.existed:
        LOGGER.info("Cask Asset %s already exists", caskname)
        sys_exit(1)

    LOGGER.info("Cask Asset Created (Identity=%s)", cask.asset["identity"])

    LOGGER.info("Loading cask...")
    cask.loading(
        {
            "description": "Filled with " + "Drum",
            "container": cask.asset["identity"],
        },
        custom_asset_attrs={
            "wipp_inventory": "assets/b7d07310-398a-48d8-990e-49ec94e5de26",
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("trupact_loading.jpg", "arc_primary_image")
            )
        ],
    )
    LOGGER.info("Loading registered...")

    LOGGER.info("Pre-shipping inspection...")
    cask.preshipping(
        {
            "description": "Inspected " + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription(
                    "preshipment_inspection.jpg", "arc_primary_image"
                ),
            )
        ],
    )
    LOGGER.info("Pre-shipping inspection registered...")

    LOGGER.info("Loading departure...")
    cask.departure(
        {
            "description": cask.asset["attributes"]["arc_display_name"]
            + " departing for WIPP."
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_departure.jpg", "arc_primary_image")
            ),
            upload_attachment(
                arch,
                AttachmentDescription(
                    "SRS_to_WPP_route_instructions.pdf", "approved_route"
                ),
            ),
        ],
    )
    LOGGER.info("Departure registered...")

    # Waypoint
    waypoints = [
        ["Atlanta", "33.592177", "-84.406064"],
        ["Talladega", "33.592177", "-86.248379"],
        ["Birmingham", "33.494993", "-86.895403"],
        ["Tuscaloosa", "33.184220", "-87.610330"],
        ["Meridian", "32.391672", "-88.532850"],
        ["Jackson", "32.285409", "-90.074633"],
        ["Monroe", "32.463868", "-91.893769"],
        ["Shreveport", "32.537993", "-93.651582"],
        ["Tyler", "32.334001", "-95.321504"],
        ["South Dallas", "32.639816", "-96.826631"],
        ["Gordon", "32.499115", "-98.521317"],
        ["Abilene", "32.457004", "-99.816598"],
        ["Big Spring", "32.244259", "-101.458984"],
        ["Andrews", "32.312469", "-102.548197"],
        ["Seminole", "32.457004", "-99.816598"],
        ["Hobbs", "32.244259", "-101.458984"],
    ]
    for point in waypoints:
        LOGGER.info("Loading waypoints from %s...", point[0])
        cask.waypoint(
            {
                "description": "TRAGIS smart sensors ping: Checking in near "
                + point[0]
                + " All sensors GREEN",
                "latitude": point[1],
                "longitude": point[2],
            },
            custom_attrs={
                "wipp_sensors_shock": "0",
                "wipp_sensors_rad": "45",
            },
            attachments=[
                upload_attachment(
                    arch,
                    AttachmentDescription("truck_departure.jpg", "arc_primary_image"),
                )
            ],
        )
    LOGGER.info("Waypoints registered...")

    # Arrival
    LOGGER.info("Loading arrival...")
    cask.arrival(
        {
            "description": cask.asset["attributes"]["arc_display_name"]
            + " arriving at WIPP",
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_arrival.jpg", "arc_primary_image")
            )
        ],
    )
    LOGGER.info("Arrival registered...")

    # Unload
    LOGGER.info("Unloading...")
    cask.unloading(
        {
            "description": "Unloaded Drum",
        },
        custom_asset_attrs={
            "wipp_inventory": "",
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription("trupact_unloading.jpg", "arc_primary_image"),
            )
        ],
        custom_attrs={
            "OnboardingFinalEventMarker": "true",
        },
    )
    LOGGER.info("Unloading registered...")
    sys_exit(0)


def run(arch, args):
    LOGGER.info("Using version %s of rkvst-archivist", about.__version__)
    LOGGER.info("Fetching use case test assets namespace %s", args.namespace)

    # Wipp class encapsulates wipp object in RKVST
    LOGGER.info("Creating Drum Asset...")
    drum = Wipp(arch, "55 gallon drum")
    drumname = "Drum"

    drum.create(
        drumname,
        "Standard non-POC 55 gallon drum",
        args.namespace,
        attachments=[AttachmentDescription("55gallon.jpg", "arc_primary_image")],
        custom_attrs={
            "wipp_capacity": "55",
            "wipp_package_id": args.namespace,
        },
    )
    if drum.existed:
        LOGGER.info("Drum Asset %s already exists", drumname)
        sys_exit(0)

    LOGGER.info("Drum Asset Created (Identity=%s)", drum.asset["identity"])

    # Cask Asset
    LOGGER.info("Creating Cask Asset...")
    caskname = "Cask"

    cask = Wipp(arch, "TRU RH 72B Cask")
    cask.create(
        caskname,
        "NRC certified type-B road shipping container, capacity 3 x 55-gallon drum",
        args.namespace,
        attachments=[AttachmentDescription("rh72b.png", "arc_primary_image")],
        custom_attrs={
            "wipp_capacity": "3",
        },
    )
    if cask.existed:
        LOGGER.info("Cask Asset %s already exists", caskname)
        sys_exit(1)

    LOGGER.info("Cask Asset Created (Identity=%s)", cask.asset["identity"])

    # Drum Characterization
    LOGGER.info("Adding characterization...")
    drum.characterize(
        {
            "description": "Waste coding characterization: A2 Fraction 2.10E+05",
            "weight": "790300",
            "a2fraction_characterized": "2.10E+05",
            "activity_characterized": "1.69E+02",
            "total_characterized": "2.12E+02",
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription(
                    "DOE-WIPP-02-3122_Rev_9_FINAL.pdf", "Reference WAC"
                ),
            ),
            upload_attachment(
                arch,
                AttachmentDescription(
                    "characterization.pdf", "Characterization report"
                ),
            ),
        ],
    )
    LOGGER.info("Characterization registered...")

    # Drum Tomography
    LOGGER.info("Adding tomography...")
    drum.tomography(
        {
            "description": "Confirming waste coding characterizations",
            "weight": "790300",
            "a2fraction_confirmed": "2.10E+05",
            "activity_confirmed": "1.69E+02",
            "total_confirmed": "2.12E+02",
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("wipp_radiography.jpg", "arc_primary_image")
            ),
            upload_attachment(
                arch,
                AttachmentDescription(
                    "DOE-WIPP-02-3122_Rev_9_FINAL.pdf", "Reference WAC"
                ),
            ),
        ],
    )
    LOGGER.info("Tomography registered...")

    # Loading
    LOGGER.info("Loading drum and cask...")
    drum.loading(
        {
            "description": "Loaded drum into "
            + cask.asset["attributes"]["arc_display_name"],
            "container": cask.asset["identity"],
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("trupact_loading.jpg", "arc_primary_image")
            )
        ],
    )
    cask.loading(
        {
            "description": "Filled with "
            + drum.asset["attributes"]["arc_display_name"],
            "container": cask.asset["identity"],
        },
        custom_asset_attrs={
            "wipp_inventory": drum.asset["identity"],
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("trupact_loading.jpg", "arc_primary_image")
            )
        ],
    )
    LOGGER.info("Loading registered...")

    # Pre-shipping
    LOGGER.info("Pre-shipping inspection...")
    drum.preshipping(
        {
            "description": "Inspection inventory "
            + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription(
                    "preshipment_inspection.jpg", "arc_primary_image"
                ),
            )
        ],
    )
    cask.preshipping(
        {
            "description": "Inspected " + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription(
                    "preshipment_inspection.jpg", "arc_primary_image"
                ),
            )
        ],
    )
    LOGGER.info("Pre-shipping inspection registered...")

    # Departure
    LOGGER.info("Loading departure...")
    drum.departure(
        {
            "description": "Departed SRS inventory "
            + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_departure.jpg", "arc_primary_image")
            ),
            upload_attachment(
                arch,
                AttachmentDescription(
                    "SRS_to_WPP_route_instructions.pdf", "approved_route"
                ),
            ),
        ],
    )
    cask.departure(
        {
            "description": cask.asset["attributes"]["arc_display_name"]
            + "departing for WIPP."
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_departure.jpg", "arc_primary_image")
            ),
            upload_attachment(
                arch,
                AttachmentDescription(
                    "SRS_to_WPP_route_instructions.pdf", "approved_route"
                ),
            ),
        ],
    )
    LOGGER.info("Departure registered...")

    # Waypoint
    waypoints = [
        ["Atlanta", "33.592177", "-84.406064"],
        ["Talladega", "33.592177", "-86.248379"],
        ["Birmingham", "33.494993", "-86.895403"],
        ["Tuscaloosa", "33.184220", "-87.610330"],
        ["Meridian", "32.391672", "-88.532850"],
        ["Jackson", "32.285409", "-90.074633"],
        ["Monroe", "32.463868", "-91.893769"],
        ["Shreveport", "32.537993", "-93.651582"],
        ["Tyler", "32.334001", "-95.321504"],
        ["South Dallas", "32.639816", "-96.826631"],
        ["Gordon", "32.499115", "-98.521317"],
        ["Abilene", "32.457004", "-99.816598"],
        ["Big Spring", "32.244259", "-101.458984"],
        ["Andrews", "32.312469", "-102.548197"],
        ["Seminole", "32.457004", "-99.816598"],
        ["Hobbs", "32.244259", "-101.458984"],
    ]
    for point in waypoints:
        LOGGER.info("Loading waypoints from %s...", point[0])
        cask.waypoint(
            {
                "description": "TRAGIS smart sensors ping: Checking in near "
                + point[0]
                + " All sensors GREEN",
                "latitude": point[1],
                "longitude": point[2],
            },
            custom_attrs={
                "wipp_sensors_shock": "0",
                "wipp_sensors_rad": "45",
            },
            attachments=[
                upload_attachment(
                    arch,
                    AttachmentDescription("truck_departure.jpg", "arc_primary_image"),
                )
            ],
        )
    LOGGER.info("Waypoints registered...")

    # Arrival
    LOGGER.info("Loading arrival...")
    drum.arrival(
        {
            "description": "At WIPP, inventory"
            + cask.asset["attributes"]["arc_display_name"],
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_arrival.jpg", "arc_primary_image")
            )
        ],
    )
    cask.arrival(
        {
            "description": cask.asset["attributes"]["arc_display_name"]
            + "arriving at WIPP",
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("truck_arrival.jpg", "arc_primary_image")
            )
        ],
    )
    LOGGER.info("Arrival registered...")

    # Unload
    LOGGER.info("Unloading...")
    drum.unloading(
        {
            "description": "Unloaded drum from cask"
            + cask.asset["attributes"]["arc_display_name"],
        },
        custom_asset_attrs={
            "wipp_container": "",
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription("trupact_unloading.jpg", "arc_primary_image"),
            )
        ],
    )
    cask.unloading(
        {
            "description": "Unloaded " + drum.asset["attributes"]["arc_display_name"],
        },
        custom_asset_attrs={
            "wipp_inventory": "",
        },
        attachments=[
            upload_attachment(
                arch,
                AttachmentDescription("trupact_unloading.jpg", "arc_primary_image"),
            )
        ],
    )
    LOGGER.info("Unloading registered...")

    # Emplacement
    LOGGER.info("Loading emplacement...")
    drum.emplacement(
        {
            "description": "Emplacement in location D-32",
            "location": "D-32",
        },
        attachments=[
            upload_attachment(
                arch, AttachmentDescription("waste_placement.jpg", "arc_primary_image")
            )
        ],
    )
    LOGGER.info("Emplacement registered...")
    sys_exit(0)
