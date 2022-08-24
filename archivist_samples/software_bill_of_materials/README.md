# Software Bill of Materials sample

Maintaining and publishing an accurate Software Bill of Materials (SBOM) is an essential cybersecurity activity for all vendors of critical software and cyber physical systems. However, publishing is not enough: users of the software also need to be able to find the information and be able to understand it in order to make strong and rational decisions about their own system security.

In its [recommendations for the minimum required elements of an SBOM](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom "NTIA recommendations"). the NTIA identifies the need to balance transparency with access controls (_"SBOMs should be available in a timely fashion to those who need them and must have appropriate access permissions and roles in place"_), and illustrates in its [NTIA SBOM Proof of Concept](https://www.ntia.doc.gov/files/ntia/publications/ntia_sbom_energy_pocplanning.pdf "NTIA Energy PoC Presentation") the need for strong stakeholder community management and a trusted SBOM data sharing mechanism which protects the interests of all parties.

RKVST Data Assurance Hub offers a solution to this sharing and distribution problem: vendors retain control of their proprietary information and release processes while customers have assured and reliable visibility into their digital supply chain risks with reliable access to current and historical SBOM data for the components they rely on.

This sample shows how to quickly get started with integrating your build and SBOM generation process with RKVST Data Assurance Hub.


## Pre-requisites

* Python 3.7 and later versions are supported.

* Install the [RKVST samples Python package](https://pypi.org/project/jitsuin-archivist-samples/ "PyPi package page")

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [RKVST documentation](https://docs.jitsuin.com/docs/setup-and-administration/getting-access-tokens-using-client-secret/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The sample creates a SoftwarePackage object and uploads a Software Bill of Materials based on the [standard SWID example](https://www.ntia.gov/files/ntia/publications/ntia_sbom_formats_and_standards_whitepaper_-_version_20191025.pdf "ACME Roadrunner Detector") "ACME Roadrunner Detector". It takes the concept of assured data one step further and extends to assured processes by simulating a series of product lifecycle events that result in a variety of updates to the SBOM, including private patches for specific customers and internal planning and approval for major updates.

To run it: 

```bash
archivist_samples_sbom [-v]
```

## Using the SoftwarePackage class

A SoftwarePackage represents the published version history of the evolving Software Bill of Materials for a product line.

This Python class makes it easy to manage SBOM distribution in RKVST and publish the [NTIA minimum required SBOM information](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom "NTIA recommendations") for your own SBOMs, regardless of how you generated them.


### Creating a new SoftwarePackage

To create a brand new SBOM Asset and begin tracking and sharing the release history of a product line, use `SoftwarePackage.create()`:

```python
    # Binaries such as images and SBOM XML need to be uploaded to RKVST first
    def upload_attachment(arch, path, name):
        with pkg_resources.open_binary(sbom_files, path) as fd:
            blob = arch.attachments.upload(fd)
            attachment = {
                "arc_display_name": name,
                "arc_attachment_identity": blob["identity"],
                "arc_hash_value": blob["hash"]["value"],
                "arc_hash_alg": blob["hash"]["alg"],
            }
            return attachment

    # Instantiate SoftwarePackage object and create an RKVST record to begin
    # tracing and publishing its version history
    package = SoftwarePackage(arch)
    package.create(
        "ACME Roadrunner Detector 2013 Coyote Edition SP1",
        "Different box, same great taste!",
        attachments=[upload_attachment(arch , "Comp_2.jpeg", "arc_primary_image")],
    )
```


### Loading an existing SoftwarePackage

If you know the RKVST Asset Identity you can load the SBOM directly as a SoftwarePackage using `SoftwarePackage.read()`:

```python
# Assume Archivist connection already initialized in `arch`
package = SoftwarePackage(arch)
package.read("assets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
```

If you do not know the RKVST Asset Identity then you can load the SBOM based on any unique set of attributes using `SoftwarePackage.read_by_signature()`:

```python
# Assume Archivist connection already initialized in `arch`
package = SoftwarePackage(arch)
package.read_by_signature({"sbom_uuid": "com.acme.rrd2013-ce-sp1-v4-1-5-0"})
```


### Making a release

When a new official release is issued, update the version history in RKVST with `SoftwarePackage.release()`:

```python
# Assume Archivist connection already initialized in `arch`
package = SoftwarePackage(arch)
package.read("assets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

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
    attachments=[upload_attachment(arch , "v4_1_5_sbom.xml", "SWID SBOM XML")],
    custom_attrs={"sbom_license": "www.gnu.org/licenses/gpl.txt"},
)
```


### Other functions

* `release_plan()`: A new release is planned but not yet made. Use this to signal upcoming changes to stakeholders who need advanced notice to review or plan software changes

* `release_accepted()`: A planned released has been approved. Use this to signal approval/sign-off of upcoming changes to stakeholders who need evidence of process approval prior to taking new releases

* `patch()`: An existing version of a release requires a patch update

* `private_patch()`: An existing version of a release requires a patch update but should only be disclosed to a subset of stakeholders

* `vuln_disclosure()`: An existing version of a release has an identified vulnerability

* `vuln_update()`: An existing version of a release with an identified vulnerability has been updated to address the vulnerability

* `deprecation()`: An existing version of a release has gone EOL or otherwise deprecated

## Access policies

In order to control data sharing to restrict general customers to see only the recommended minimal SBOM elements and not private patches or planning/approval steps, create an Access Policy like this (substituting for real Subject IDs of your value chain partners):

```json
    {
      "identity": "access_policies/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "display_name": "SBOM soft publish",
      "filters": [
        {
          "or": [ "attributes.arc_display_type=Software Package" ]
        }
      ],
      "access_permissions": [
        {
          "subjects": [ "subjects/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" ],
          "behaviours": [ "Attachments", "RecordEvidence" ],
          "include_attributes": [],
          "user_attributes": [],
          "asset_attributes_read": [
            "arc_display_type",
            "arc_display_name",
            "arc_description",
            "arc_attachments",
            "sbom_component",
            "sbom_supplier",
            "sbom_uuid",
            "sbom_author",
            "sbom_version",
            "sbom_hash"
          ],
          "asset_attributes_write": [],
          "event_arc_display_type_read": [
            "Release",
            "Patch",
            "Vulnerability Disclosure",
            "Vulnerability Update"
          ],
          "event_arc_display_type_write": []
        }
      ],
      "tenant": "tenant/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "description": "Publish minimum required SBOM params to partners"
    }

```
