# Synsation suite

Synsation Corporation is a fictional company used to build storylines and illustrate use cases around industrial and smart cities applications of the DataTrails platform.

The suite includes a number of entry points / samples that illustrate different capabilities:

* `archivist_samples_synsation initialise` Creates a range of Assets representing different types of equipment
* `archivist_samples_synsation charger` Simulates cyber maintenance lifecycles of electric vehicle chargers
* `archivist_samples_synsation simulator` Simulates a software update cycle from finding a vulnerability through approvals, patch, and deployment
* `archivist_samples_synsation wanderer` Simulates a simple physical shipping use case with GIS tracking
* `archivist_samples_synsation analyze` assesses SLAs and vulnerability windows in the Synsation asset set

## Pre-requisites

* Python 3.9 and later versions are supported.

* Install the DataTrails samples package. If you are just trying out the pre-made samples you should get the official [DataTrails samples Python package](https://pypi.org/project/datatrails-samples/ "PyPi package page") from PyPi. If you are modifying this sample and want to try out your changes then you'll need to rebuild the wheel: please refer to the developer instructions in the top level of this repository to see how to do that.

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [DataTrails documentation](https://docs.datatrails.ai/docs/datatrails-basics/getting-access-tokens-using-app-registrations/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The Taskfile in the top level of this repository includes a pre-packaged run of this sample that performs both a quick and deep count of the Assets and Events in your DataTrails tenancy. 

Please refer to the instructions in the [top level README](https://github.com/datatrails/datatrails-samples#synsation "synsation suite")

