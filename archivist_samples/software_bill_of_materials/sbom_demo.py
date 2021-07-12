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
#from software_deployment import SoftwareDeployment


def main():
    # Refer to RKVST documentation for how to get an authtoken
    try:
        with open(".auth_token", mode="r") as tokenfile:
            authtoken = tokenfile.read().strip()
    except FileNotFoundError:
        exit("ERROR: Auth token not found. Please store your bearer token in a file called '.auth_token' and try again.")

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
        attachments=["attachments/Comp_2.jpeg"]
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
            "uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0"
        },
        attachments=["attachments/v4_1_5_sbom.xml"],
        custom_attrs={"sbom_license": "www.gnu.org/licenses/gpl.txt"}
    )
    print("Release registered.")


if __name__ == "__main__":
    main()
