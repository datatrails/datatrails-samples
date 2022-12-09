# Estate Info sample

One of the greatest benefits of RKVST is having a system-wide view of your entire asset estate in one place, enabling better informed, more confident decisions.

The `estate-info` sample very simply demonstrates how to read and enumerate Assets and Events from your RKVST tenancy. It also demonstrates various techniques for quickly counting assets and events without fetching the whole data set.


## Pre-requisites

* Python 3.7 and later versions are supported.

* Install the RKVST samples package. If you are just trying out the pre-made samples you should get the official [RKVST samples Python package](https://pypi.org/project/rkvst-samples/ "PyPi package page") from PyPi. If you are modifying this sample and want to try out your changes then you'll need to rebuild the wheel: please refer to the developer instructions in the top level of this repository to see how to do that.

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [RKVST documentation](https://docs.rkvst.com/docs/rkvst-basics/getting-access-tokens-using-app-registrations/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The Taskfile in the top level of this repository includes a pre-packaged run of this sample that performs both a quick and deep count of the Assets and Events in your RKVST tenancy. 

Please refer to the instructions in the [top level README](https://github.com/rkvst/rkvst-samples#manage-assets-and-events-and-check-for-any-inconsistencies "estate info sample")

