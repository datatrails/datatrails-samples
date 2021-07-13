#   Copyright 2021 Jitsuin, inc
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

#   This is API SAMPLE CODE, not for production use.

# pylint:  disable=missing-docstring

from archivist import archivist
from software_package import SoftwarePackage


def main():
    # Refer to RKVST documentation for how to get an authtoken
    try:
        with open(".auth_token", mode="r") as tokenfile:
            authtoken = tokenfile.read().strip()
    except FileNotFoundError:
        exit(
            "ERROR: Auth token not found. Please store your bearer token in a file called '.auth_token' and try again."
        )

    # Initialize connection to Archivist
    arch = archivist.Archivist(
        "https://rkvst.poc.jitsuin.io",
        auth=authtoken,
    )

    # SoftwarePackage class encapsulates SBOM object in RKVST
    print("Creating Software Package Asset...", end="")
    package = SoftwarePackage(arch)

    package.create(
        "ACME Roadrunner Detector 2013 Coyote Edition SP1",
        "Different box, same great taste!",
        attachments=["attachments/Comp_2.jpeg"],
        custom_attrs={
            "sbom_license": "www.gnu.org/licenses/gpl.txt",
            "proprietary_secret": "For your eyes only",
        },
    )
    print(f"Software Package Created (Identity={package.asset['identity']})")

    # Make a release
    print("Making a release...", end="")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.5 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.5",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0",
        },
        attachments=["attachments/v4_1_5_sbom.xml"],
    )
    print("Release registered.")

    # Make a release
    print("Making a release...", end="")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.6 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.6",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-0",
        },
        attachments=["attachments/v4_1_6_sbom.xml"],
    )
    print("Release registered.")

    # Private patch
    print("Making a private patch...", end="")
    package.private_patch(
        {
            "private_id": "special_customer",
            "target_component": "rrdetector",
            "target_version": "v1.4.6",
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "Private patch to v4.1.6 for limited customer set",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-6-1",
            "reference": "CVE-20210613-1",
        },
        attachments=["attachments/v4_1_6_1_sbom.xml"],
    )
    print("Private patch registered.")

    # Make a release
    print("Making a release...", end="")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v4.1.7 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v4.1.7",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-7-0",
        },
        attachments=["attachments/v4_1_7_sbom.xml"],
    )
    print("Release registered.")

    # Plan major upgrade
    package.release_plan(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
        },
        attachments=["attachments/v5_0_0_sbom.xml"],
    )

    # Approve major upgrade
    package.release_accepted(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "date": "2021-07-13",
            "reference": "BIG_V_5",
            "captain": "Deputy Dawg",
            "approver": "Yosemite Sam",
        },
        attachments=["attachments/v5_0_0_sbom.xml"],
    )

    # Release major upgrade
    print("Making a release...", end="")
    package.release(
        {
            "name": "ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "description": "v5.0.0 Release - ACME Roadrunner Detector 2013 Coyote Edition SP1",
            "hash": "a314fc2dc663ae7a6b6bc6787594057396e6b3f569cd50fd5ddb4d1bbafd2b6a",
            "version": "v5.0.0",
            "author": "The ACME Corporation",
            "supplier": "Coyote Services, Inc.",
            "uuid": "com.acme.rrd2013-ce-sp1-v5-0-0-0",
        },
        attachments=["attachments/v5_0_0_sbom.xml"],
    )
    print("Release registered.")


if __name__ == "__main__":
    main()
