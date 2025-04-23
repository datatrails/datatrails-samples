#!/usr/bin/env python3

# List of imports used for this script
# In addition this script uses DataTrails Python3 SDK
import os
import os.path
from os import getenv

import subprocess
import sys
import hashlib

import datetime
from datetime import timedelta

from archivist.logger import set_logger
from archivist.archivist import Archivist
from archivist.utils import get_auth

import time
import string
import random

import sample

import importlib.resources as res


# DataTrails Connection Parameters -- Honest Abe
#
# The below are environment variables that are parameters used to connect
# to the production instance of DataTrails.
#
# HONEST_CLIENT_ID = represents the client ID from an App Registration
# HONEST_CLIENT_SECRET_FILENAME = represents location of client secret from an App Registration
def honest_arch():
    client_id = getenv("HONEST_CLIENT_ID")
    client_secret_file = getenv("HONEST_CLIENT_SECRET_FILENAME")
    with open(client_secret_file, mode="r", encoding="utf-8") as tokenfile:
        client_secret = tokenfile.read().strip()

    arch = Archivist(
        "https://app.datatrails.ai", (client_id, client_secret), max_time=300
    )

    return arch


# DataTrails Connection Parameters -- Evil Eddie
#
# The below are environment variables that are parameters used to connect
# to the production instance of DataTrails.
#
# EVIL_CLIENT_ID = represents the client ID from an App Registration
# EVIL_CLIENT_SECRET_FILENAME = represents location client secret from an App Registration
def evil_arch():
    client_id = getenv("EVIL_CLIENT_ID")
    client_secret_file = getenv("EVIL_CLIENT_SECRET_FILENAME")
    with open(client_secret_file, mode="r", encoding="utf-8") as tokenfile:
        client_secret = tokenfile.read().strip()

    arch = Archivist(
        "https://app.datatrails.ai", (client_id, client_secret), max_time=300
    )

    return arch


# Uploads attachments to DataTrails
def upload_attachment(arch, path, name):
    with res.files(sample).joinpath(path).open("rb") as fd:
        blob = arch.attachments.upload(fd)
        attachment = {
            "arc_display_name": name,
            "arc_attribute_type": "arc_attachment",
            "arc_file_name": path,
            "arc_blob_identity": blob["identity"],
            "arc_blob_hash_value": blob["hash"]["value"],
            "arc_blob_hash_alg": blob["hash"]["alg"],
        }
        return attachment


# Creates a SHA256 hash value for documents that are uploaded to DataTrails
def create_hash(path):
    with open(path, "rb") as f:
        data = f.read()
        digest = hashlib.sha256(data).hexdigest()

    return digest


# Creates a public Document Asset with a primary image and related attachments within DataTrails
#
# arc_primary_image = represents the primary image to be displayed within the DataTrails user interface
# document_document = represents the attachments/document to be uploaed to DataTrails
#
# For additional information regarding DataTrails Document Profile see below:
# https://docs.datatrails.ai/developers/developer-patterns/document-profile/
def create_asset(
    arch,
    displayname,
    description,
    displaytype,
    version,
    id,
    hash,
    attachments,
    doc_attachments,
):
    attrs = {
        "arc_primary_image": attachments,
        "document_document": doc_attachments,
        "arc_display_name": displayname,
        "arc_description": description,
        "arc_display_type": displaytype,
        "arc_profile": "Document",
        "document_hash_alg": "SHA256",
        "document_hash_value": hash,
        "document_version": version,
        "id": id,
    }
    props = {"public": True}

    return arch.assets.create(props=props, attrs=attrs)


# Uploads primary image and related attachments to DataTrails
# Creates hash value for related attachments
# Passes expected values to create_asset method
#
# image = represents the digital content to be recorded within DataTrails
# serial_num = represents unique Asset attribute (id) that can be referenced
def create_c2docasset(arch, image):
    attachments = upload_attachment(arch, image, "arc_primary_image")
    doc_attachments = upload_attachment(arch, image, "initial_image")

    # Creates hash value for Document Asset
    doc_hash = create_hash("./sample/" + image)

    serial_num = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )

    return create_asset(
        arch,
        "C2PA Image - Vinyl",
        "C2PA Image - Vinyl",
        "C2PA",
        "1.0.0",
        serial_num,
        doc_hash,
        attachments,
        doc_attachments,
    )


# Retrieving Asset based on unique id Asset attribute
def get_asset(arch, id):
    attrs = {"id": id}

    return arch.assets.read_by_signature(attrs=attrs)


# Creates an Asset-Embedded Manifest Event for an Asset identified by id
#
# Uses c2pa command line utility to create the Asset-Embedded Manifest
# Documentation referencing below command line utility:
# https://github.com/contentauth/c2patool
#
# See "Adding a manifest to an asset file"
#
# c2patool sample/pexels-miguel-á-padriñán-5764283.jpg -m sample/definition.json -f -o sample/signed_pexels-miguel-á-padriñán-5764283.jpg
#
# image = represents the file a manifest will be created against
# definition = represents the json file used to create the manifest
# signed_image = represents the output file that contains the manifest
def create_manifest(arch, id, image, definition):
    print("Generating Manifest")

    asset = get_asset(arch, id)
    if not asset:
        print("No asset found")

    props = {"operation": "Record", "behaviour": "RecordEvidence"}

    cmd = [
        "c2patool",
        "sample/" + image,
        "-m",
        "sample/" + definition,
        "-f",
        "-o",
        "sample/signed_" + image,
    ]
    subprocess.run(cmd, shell=False)

    sattachments = upload_attachment(arch, "signed_" + image, "signed_image")

    attrs = {
        "signed_image": sattachments,
        "arc_display_type": "Embedded Manifest Creation",
        "arc_description": "Generated Embedded Manifest",
    }

    return arch.events.create(asset["identity"], props=props, attrs=attrs)


# Creates a Publish Event for an Asset identified by id
#
# Records the hash value of the document to be published in addition
# to author, version and description.
#
# manifest = represents the file to be published.
def create_publish(arch, id, version, manifest, description, author):
    asset = get_asset(arch, id)
    if not asset:
        print("No asset found")

    doc_hash = create_hash("./sample/" + manifest)

    attachments = upload_attachment(arch, manifest, "published_document")

    props = {"operation": "Record", "behaviour": "RecordEvidence"}
    attrs = {
        "arc_display_type": "Publish",
        "arc_description": description,
        "document_version_authors": [
            {"display_name": author, "email": "demo@demo.com"}
        ],
    }
    asset_attrs = {
        "document_document": attachments,
        "document_hash_alg": "SHA256",
        "document_hash_value": doc_hash,
        "document_version": version,
        "document_status": "Published",
        "arc_display_name": "C2PA Image - Vinyl",
        "arc_display_type": "C2PA",
    }

    return arch.events.create(
        asset["identity"], props=props, attrs=attrs, asset_attrs=asset_attrs
    )


# Creates an Ingredient Event for an Asset identified by id
#
# Ingredient file relays information about the image (format, title, id, etc...)
#
# Uses c2pa command line utility to create ingredient json file
# Documentation referencing below command line utility:
# https://github.com/contentauth/c2patool
#
# See "Creating an ingredient from a file"
#
# c2patool sample/pexels-miguel-á-padriñán-5764283.jpg --ingredient --force --output ./ingredient
#
# image = represents asset-embedded file used to create ingredient info
# Output file is located in directory called "ingredient" and copied to
# sample directory.
def create_ingredient(arch, id, image):
    print("Generating Ingredient List")

    asset = get_asset(arch, id)
    if not asset:
        print("No asset found")

    cmd = [
        "c2patool",
        "sample/" + image,
        "--ingredient",
        "--force",
        "--output",
        "./ingredient",
    ]
    cp_cmd = ["cp", "-f", "ingredient/ingredient.json", "sample/"]

    subprocess.run(cmd, shell=False)
    subprocess.run(cp_cmd, shell=False)

    attachments = upload_attachment(arch, "ingredient.json", "ingredient_list")

    props = {"operation": "Record", "behaviour": "RecordEvidence"}
    attrs = {
        "ingredient_list": attachments,
        "arc_display_type": "Ingredients",
        "arc_description": "Ingredient List",
    }

    return arch.events.create(asset["identity"], props=props, attrs=attrs)


# Creates a Parent Manifest Event for an Asset identified by id
#
# Uses c2pa command line utility to create parent manifest
# Documentation referencing below command line utility:
# https://github.com/contentauth/c2patool
#
# See "Adding a manifest to an asset file/Specifying a parent file"
#
# Passing the ingredient file of the "parent" image to be added to the manifest
# for the "child" image.
#
# c2patool sample/pexels-miguel-á-padriñán-5764284.jpg -m sample/4defintion.json -p ./ingredient -f -o sample/signed_pexels-miguel-á-padriñán-5764284.jpg
#
# image = represents "child" image that DOES NOT have a manifest
# defintion = represents the json file used to create the manifest
# signed_image = represents the output file that contains the manifest
def create_parent(arch, id, image, definition):
    print("Creating Manifest with Parent Image")

    asset = get_asset(arch, id)
    if not asset:
        print("No asset found")

    cmd = [
        "c2patool",
        "sample/" + image,
        "-m",
        "sample/" + definition,
        "-p",
        "./ingredient",
        "-f",
        "-o",
        "sample/signed_" + image,
    ]
    subprocess.run(cmd, shell=False)

    attachments = upload_attachment(arch, "signed_" + image, "parent_manifest")

    attrs = {
        "parent_manifest": attachments,
        "arc_display_type": "Parent Manifest",
        "arc_description": "Generating Parent Manifest",
    }
    props = {"operation": "Record", "behaviour": "RecordEvidence"}

    return arch.events.create(asset["identity"], props=props, attrs=attrs)


# Creates a Details Event for an Asset identified by id
#
# Uses c2pa command line utility to create manifest detail info
# Documentation referencing below command line utility:
# https://github.com/contentauth/c2patool
#
# See "Detailed manifest report"
#
# c2patool sample/signed_pexels-miguel-á-padriñán-5764284.jpg -d --force --output ./details
#
# detailed.json = represents info about the format of c2pa file
# manifest_store.json = represents  the manifest(s) info related to the signed image file
#
# Output files are located in "details" directory and copied to samples directory
def create_details(arch, id, image):
    print("Generating Details Report")

    asset = get_asset(arch, id)
    if not asset:
        print("No asset found")

    cmd = ["c2patool", "sample/" + image, "-d", "--force", "--output", "./details"]
    cp_cmd = ["cp", "-f", "details/detailed.json", "sample/"]
    cp1_cmd = ["cp", "-f", "details/manifest_store.json", "sample/"]

    subprocess.run(cmd, shell=False)
    subprocess.run(cp_cmd, shell=False)
    subprocess.run(cp1_cmd, shell=False)

    dattachments = upload_attachment(arch, "detailed.json", "details")
    mattachments = upload_attachment(arch, "manifest_store.json", "manifest_store")

    props = {"operation": "Record", "behaviour": "RecordEvidence"}
    attrs = {
        "detail_report": dattachments,
        "manifest_report": mattachments,
        "arc_display_type": "Details Report",
        "arc_description": "Generated Details Report",
    }

    return arch.events.create(asset["identity"], props=props, attrs=attrs)


# Main Function:
#
# Records two public Document Assets by two individuals: Honest Abe and Evil Eddie
#
# Honest Abe and Evil Eddie reside in two separate DataTrails tenancies with App Registrations that
# represent each tenancy.
#
# arch = Honest Abe
# bad_arch = Evil Eddie
#
# Honest Abe records initial image, asset-embedded manifests along with related information about the
# the image that has been recorded.  Thus providing a historical journey of Honest Abe's image.
#
# Evil Eddie records Honest Abe's image but has changed manifest information by changing the related
# definition file.  Evil Eddie continues to record historical journey of Honest Abe's image with the
# "changed" manifest.  Thus provifing a historical journey of Honest Abe's image with redacted/changed
# manifest data.
#
# definition.json = represents the true/real manifest definition file for "pexels-miguel-á-padriñán-5764283.jpg"
# 4defintion.json = represents the true/real manifest defintion file for "pexels-miguel-á-padriñán-5764284.jpg"
#
# bad_definition = represents the redacted/changed manifest defition file for "pexels-miguel-á-padriñán-5764283.jpg"
# 4bad_defintion = represents the redacted/changed manifest defition file for "pexels-miguel-á-padriñán-5764284.jpg"
def main():
    set_logger("DEBUG")
    arch = honest_arch()
    bad_arch = evil_arch()

    asset = create_c2docasset(arch, "pexels-miguel-á-padriñán-5764283.jpg")
    create_manifest(
        arch,
        asset["attributes"]["id"],
        "pexels-miguel-á-padriñán-5764283.jpg",
        "definition.json",
    )
    create_publish(
        arch,
        asset["attributes"]["id"],
        "1.1.M",
        "signed_pexels-miguel-á-padriñán-5764283.jpg",
        "Published Asset-Embedded Manifest",
        "Honest Abe",
    )
    create_ingredient(
        arch, asset["attributes"]["id"], "signed_pexels-miguel-á-padriñán-5764283.jpg"
    )
    create_publish(
        arch,
        asset["attributes"]["id"],
        "2.0.0",
        "pexels-miguel-á-padriñán-5764284.jpg",
        "Published Related Image",
        "Honest Abe",
    )
    create_parent(
        arch,
        asset["attributes"]["id"],
        "pexels-miguel-á-padriñán-5764284.jpg",
        "4definition.json",
    )
    create_publish(
        arch,
        asset["attributes"]["id"],
        "2.1.PM",
        "signed_pexels-miguel-á-padriñán-5764284.jpg",
        "Published Parent Manifest",
        "Honest Abe",
    )
    create_details(
        arch, asset["attributes"]["id"], "signed_pexels-miguel-á-padriñán-5764284.jpg"
    )

    time.sleep(2)

    evil_asset = create_c2docasset(bad_arch, "pexels-miguel-á-padriñán-5764283.jpg")
    create_manifest(
        bad_arch,
        evil_asset["attributes"]["id"],
        "pexels-miguel-á-padriñán-5764283.jpg",
        "bad_definition.json",
    )
    create_publish(
        bad_arch,
        evil_asset["attributes"]["id"],
        "1.1.M",
        "signed_pexels-miguel-á-padriñán-5764283.jpg",
        "Published Asset-Embedded Manifest",
        "Evil Eddie",
    )
    create_ingredient(
        bad_arch,
        evil_asset["attributes"]["id"],
        "signed_pexels-miguel-á-padriñán-5764283.jpg",
    )
    create_publish(
        bad_arch,
        evil_asset["attributes"]["id"],
        "2.0.0",
        "pexels-miguel-á-padriñán-5764284.jpg",
        "Published Related Image",
        "Evil Eddie",
    )
    create_parent(
        bad_arch,
        evil_asset["attributes"]["id"],
        "pexels-miguel-á-padriñán-5764284.jpg",
        "4bad_definition.json",
    )
    create_publish(
        bad_arch,
        evil_asset["attributes"]["id"],
        "2.1.PM",
        "signed_pexels-miguel-á-padriñán-5764284.jpg",
        "Published Parent Manifest",
        "Evil Eddie",
    )
    create_details(
        bad_arch,
        evil_asset["attributes"]["id"],
        "signed_pexels-miguel-á-padriñán-5764284.jpg",
    )


if __name__ == "__main__":
    main()
