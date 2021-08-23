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

"""Key management
"""

# pylint:  disable=missing-docstring


import base64
import os

from sys import exit as sys_exit
from sys import stdout as sys_stdout

# From the documentation:
# This is a “Hazardous Materials” module. You should ONLY use it if you’re 100%
# absolutely sure that you know what you’re doing because this module is full of
# land mines, dragons, and dinosaurs with laser guns.
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# from cryptography.hazmat.primitives import hashes, padding  # see call to public_key.verify below
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat import backends

from archivist import about
from archivist.errors import ArchivistNotFoundError

from ..testing.logger import set_logger, LOGGER
from ..testing.parser import common_parser, common_endpoint

# Key management functions
#
# In a real device these keys would be stored in a
# local SE/HSM or provisioned into a TEE or such, but for this
# sample we generate fresh keys and store them as PEM files
# in the local directory.
# For key use in a real device we would expect the keys to be
# fetched from (and ideally used in) secure storage or local HSM
# but in this example we simply load the PEM files and use a
# local in-memory crypto lib
#########################


def generate_fresh_keys():
    # Generate keys.
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key


def load_keys(asset_name):
    # Read out the PEM files from disk and load them.
    # A real device would most likely just initialise
    # key IDs in a TEE or SE or something
    fname = f'{asset_name.replace(" ", "_")}-priv.pem'
    LOGGER.debug("Loading private key file...")
    with open(fname, mode="rb") as privkeyfile:
        privkey_pem = privkeyfile.read().strip()

    backend = backends.default_backend()
    private_key = backend.load_pem_private_key(privkey_pem, password=None)
    public_key = private_key.public_key()

    return private_key, public_key


# General utility functions
###########################


def asset_exists(archivist, asset_name):
    # This is a simple safety feature for the sample program to
    # avoid over-writing or duplicating assets. It's not necessary
    # for real hardware endpoints which are properly enrolled.

    # Check 1: see if this asset is registered in Archivist
    # NOTE: Doing this opens a connection to archivist, and fetches
    # a copy of the Archivist record for this asset which includes
    # information such as the asset identity and its public key.
    # However in order to keep the sample clean in terms of a real
    # device with local storage and local enclaves we don't take
    # advantage of this information here and load it locally when
    # needed instead.
    try:
        archivist.assets.read_by_signature(
            attrs={"arc_display_name": asset_name},
        )
    except ArchivistNotFoundError:
        LOGGER.info("Asset '%s' not found in Archivist", asset_name)
        return False

    # Check 2: see if its asset config file is present
    fname = f'{asset_name.replace(" ", "_")}-priv.pem'
    if not os.path.exists(fname):
        LOGGER.info("Asset '%s' key files not found", asset_name)
        return False

    # Check 3: see if its local emulated key files are present
    fname = f'{asset_name.replace(" ", "_")}-priv.pem'
    if not os.path.exists(fname):
        LOGGER.info("Asset '%s' config not found in Archivist", asset_name)
        return False

    return True


def load_asset(asset_name):
    priv, pub = load_keys(asset_name)

    if not priv or not pub:
        return None

    fname = f'{asset_name.replace(" ", "_")}.aid'
    with open(fname, mode="r") as aidfile:
        a_id = aidfile.read().strip()

    return priv, pub, a_id


# Use case functions
####################


def generate_crypto_asset(archivist, asset_name):
    # Generate the keys. In a real device these would be stored in a
    # local SE/HSM or provisioned into a TEE or such, and fetched
    # from (or used in) secure storage, but for this example we
    # generate fresh and put them in local storage
    private_key, public_key = generate_fresh_keys()
    if not private_key or not public_key:
        LOGGER.error("Failed to generate keys for new asset")
        return None

    # Get the public key in a portable format to store in the
    # asset's 'birth certificate'
    pubkey_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Note this asset is as lean as possible in order to cleanly demonstrate
    # how to associate a private key for message signing. Please see other
    # samples for broader and richer use of asset attributes
    attrs = {
        "arc_display_name": asset_name,
        "arc_description": "Sample cryptographic asset for Jitsuin Archivist",
        "arc_display_type": "Crypto endpoint",
        "arc_evidence_signing_pubkey": pubkey_pem.decode("utf-8"),
    }
    newasset = archivist.assets.create(attrs=attrs, confirm=True)
    LOGGER.debug(newasset)
    if not newasset:
        LOGGER.error("Failed to register new asset with Archivist")
        return None

    # Now that the asset is safely registered, write keys to disk
    # as PEM files.
    # Note we don't technically need the public key to be saved -
    # we can always work it out given the private key - but we write
    # it out for the benefit of the sample so that (for example) it
    # can be used in OpenSSL to test the signatures that are produced
    # and stored by Archivist

    fname = f'{asset_name.replace(" ", "_")}-pub.pem'
    LOGGER.debug("Writing public key file...")
    with open(fname, mode="wb+") as pubkeyfile:
        pubkeyfile.write(pubkey_pem)

    privkey_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    fname = f'{asset_name.replace(" ", "_")}-priv.pem'
    LOGGER.debug("Writing private key file...")
    with open(fname, mode="wb+") as privkeyfile:
        privkeyfile.write(privkey_pem)

    # Stash the asset's tokenized ID so that we can talk to the
    # Archivist later. We don't need to do this - the asset could
    # always search for its record iun all kinds of ways - but
    # much more efficient to retain this in local storage on a
    # real device
    fname = f'{asset_name.replace(" ", "_")}.aid'
    LOGGER.debug("Writing asset config file...")
    with open(fname, mode="w+") as assetconfigfile:
        assetconfigfile.write(newasset["identity"])

    return newasset


def submit_signed_evidence(archivist, asset_name, message, corrupt_sig):
    # Load the device state
    priv, pub, a_id = load_asset(asset_name)

    if not priv or not pub or not a_id:
        LOGGER.error("Failed to load asset state")
        return

    # Sign the message, convert to base64 for safe transmission
    sig = priv.sign(message.encode("utf-8"))
    signature = base64.urlsafe_b64encode(sig).decode("utf-8")

    if corrupt_sig:
        # Special testing mode to show what happens if false evidence
        # or a corrupted device gets inserted into Archivist
        signature = signature[2:]

    # Issue RecordEvidence log. Note you can add a signature to
    # any type of Archivist event in this way. This is just a simple
    # example to demonstrate the technique
    props = {
        # Simple evidence event - not interpreted by the
        # Archivist system but can be analysed externally
        "operation": "Record",
        "behaviour": "RecordEvidence",
        # Masquerade as an independent device. This allows this test
        # script to superficially appear like multiple actors, and this
        # functionality is genuinely useful in the case of mobile apps
        # or shared terminals where the actual app credential is less
        # interesting than the logged in user, but note that the system
        # WILL record the actual user from the JWT as well.
        "principal_declared": {
            "subject": f"{asset_name}",
            "email": f"{asset_name}@iot.wavestone.com",
            "display_name": f"{asset_name} machine credential",
        },
    }
    attrs = {
        # Required properties for the Archivist system
        "arc_display_type": "Status",
        "arc_description": f"Status update from '{asset_name}'",
        "arc_evidence": message,
        # Optional property allows us to attach a signature from the
        # device's private key. The key should match the one stored
        # in the asset's 'arc_evidence_signing_pubkey'. The signature
        # should cover the complete 'arc_evidence' field (and no more)
        "arc_evidence_signature": signature,
    }
    archivist.events.create(a_id, props, attrs, confirm=True)


def print_history(archivist, asset_name):
    # This function shows how to verify the records from the
    # asset history. This would not run on the device - its an
    # audit function - so we don't rely on any of the locally
    # stored state here.
    # This is essentially what Archivist does internally, but it's
    # also useful to see how it can be done externally

    # Get the trusted public key from the asset record
    asset = archivist.assets.read_by_signature(
        attrs={"arc_display_name": asset_name},
    )
    if not asset:
        LOGGER.error("Asset not found in Archivist")
        return

    if not "arc_evidence_signing_pubkey" in asset["attributes"]:
        LOGGER.error("Asset not signing-enabled")
        return

    backend = backends.default_backend()
    public_key = backend.load_pem_public_key(
        bytes(asset["attributes"]["arc_evidence_signing_pubkey"], encoding="utf8")
    )

    if not public_key:
        LOGGER.error("Asset public key corrupted")
        return

    # Fetch all the events for this asset
    events = archivist.events.list(asset_id=asset["identity"])

    # Now check each one in turn
    for event in events:
        attrs = event["event_attributes"]
        if not "arc_evidence_signature" in attrs:
            LOGGER.debug("Skipping event with no signature field")
            continue

        message = attrs["arc_evidence"].encode("utf-8")
        signature = base64.urlsafe_b64decode(attrs["arc_evidence_signature"])

        LOGGER.info("Checking message '%s'...", attrs["arc_evidence"])
        try:
            # NOTE: pylint complains about 2 missing args 'padding' and 'hashes'.
            # Googling shows that this call should be:
            #     public_key.verify(signature, message, padding.PKCS7(128), hashes.SHA512())
            # However this generates a runtime error about expecting only 3 args and
            # not 5. Some funky python fiddling is going on here. Note the warning from
            # the hazmat documentation reproduced at the top of this file next to the import
            # statement.
            public_key.verify(  # pylint: disable=no-value-for-parameter
                signature, message
            )
            LOGGER.info("√ GOOD")
        except InvalidSignature:
            LOGGER.error("X BAD")


# Main app loop
###############
def run(archivist, args):

    LOGGER.info("Using version %s of jitsuin-archivist", about.__version__)
    asset_name = " ".join([args.asset_name, args.namespace])
    # Check which operation we're doing, and ensure we have the info
    # we need to do it

    if args.create_asset:
        # Don't create if there's already an asset record with this name.
        # This is not strictly necessary - the Jitsuin Archivist system
        # does not require arc_display_name to be unique - but to keep
        # things simple we'll avoid duplicates here.
        if asset_exists(archivist, asset_name):
            LOGGER.error(
                "Asset '%s' already exists."
                " Please choose a different name to create.",
                asset_name,
            )
            sys_exit(1)

        LOGGER.info("Generate crypto asset '%s'", asset_name)
        generate_crypto_asset(archivist, asset_name)
        sys_exit(0)

    if args.sign_message:
        if not asset_exists(archivist, asset_name):
            LOGGER.error(
                "Asset '%s' does not exist."
                " Please choose a different name to create.",
                asset_name,
            )
            sys_exit(1)

        LOGGER.info("Submit signed evidence '%s'", asset_name)
        submit_signed_evidence(archivist, asset_name, args.sign_message, False)
        sys_exit(0)

    if args.bad_sign_message:
        if not asset_exists(archivist, asset_name):
            LOGGER.error(
                "Asset '%s' does not exist."
                "Please choose the correct name or create it first.",
                asset_name,
            )
            sys_exit(1)

        LOGGER.info("Submit badly signed evidence %s", asset_name)
        submit_signed_evidence(archivist, asset_name, args.bad_sign_message, True)
        sys_exit(0)

    if args.check_sigs:
        if not asset_exists(archivist, asset_name):
            LOGGER.error(
                "Asset '%s' does not exist."
                "Please choose the correct name or create it first.",
                asset_name,
            )
            sys_exit(1)

        LOGGER.info("Check %s", asset_name)
        print_history(archivist, asset_name)
        sys_exit(0)


def main():
    parser, _ = common_parser(
        "Shows simple integration of a device private signing key with Archivist records"
    )
    parser.add_argument(
        "--namespace",
        type=str,
        dest="namespace",
        action="store",
        default=None,
        help="namespace of item population (to enable parallel demos",
    )

    # Operations
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument(
        "--create",
        dest="create_asset",
        action="store_true",
        default=False,
        help="create a new asset record",
    )
    operations.add_argument(
        "--sign-message",
        type=str,
        dest="sign_message",
        action="store",
        default=None,
        help=("Sign this string and add record to Archivist"),
    )
    operations.add_argument(
        "--bad-sign-message",
        type=str,
        dest="bad_sign_message",
        action="store",
        default=None,
        help="Add an evidence record to Archivist with a bad signature (for testing)",
    )
    operations.add_argument(
        "--check",
        dest="check_sigs",
        action="store_true",
        default=False,
        help="Check the signatures on all evidence records of ASSET_NAME",
    )

    # Required args
    parser.add_argument("asset_name")

    args = parser.parse_args()

    if args.verbose:
        set_logger("DEBUG")
    else:
        set_logger("INFO")

    poc = common_endpoint("signed_records", args)

    run(poc, args)

    parser.print_help(sys_stdout)
    sys_exit(1)
