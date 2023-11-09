# Door entry sample

Access control is not just an issue for files and computer systems: when it comes to connected door locks it's a real world issue. Various stakeholders (landlords, building services, police, delivery companies) have legitimate reasons to enter the communal areas of shared buildings but the residents and owners of that building also need to be sure of their safety and privacy. How do you makes sure that privileged access to buildings is enabled whilst also holding the authorities to account and preventing abuses?

DataTrails Data Assurance Hub offers a solution to this problem: by ensuring that all stakeholders have a transparent view of privileged access events, abuses are discouraged and quickly discovered. By combining virtual world evidence (cryptographic identities, timestamps) with real world evidence (photographs from the built-in camera from the door access system) a very strong record of when who accessed a building is maintained and made available for audit and dispute resolution.

This sample simulates a set of smart connected door locks processing and reporting their privileged accesses through DataTrails. Through simulating door access cards it also demonstrates DataTrails's principle of building up asset provenance based on trusted Witness Statements rather than direct connection to assets, which provides much greater system visibility than traditional agent-based platforms.


## Pre-requisites

* Python 3.8 and later versions are supported.

* Install the DataTrails samples package. If you are just trying out the pre-made samples you should get the official [DataTrails samples Python package](https://pypi.org/project/datatrails-samples/ "PyPi package page") from PyPi. If you are modifying this sample and want to try out your changes then you'll need to rebuild the wheel: please refer to the developer instructions in the top level of this repository to see how to do that.

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [DataTrails documentation](https://docs.datatrails.ai/docs/datatrails-basics/getting-access-tokens-using-app-registrations/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The Taskfile in the top level of this repository includes a pre-packaged run of this sample that creates a number of door access terminals and access cards and simulates privileged access events which can then be viewed and analysed in your DataTrails tenancy. 

Please refer to the instructions in the [top level README](https://github.com/datatrails/datatrails-samples#door-entry-control "door entry sample")

