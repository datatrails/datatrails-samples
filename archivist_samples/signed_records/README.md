# Signed Records sample

A key aspect of Zero Trust architectures is the removal of inherent trust in any individual part of your network. The best way to assure trustworthy operations is to combine several best-of-breed security technologies and then adopt a trust-but-verify (or rather, verify-then-trust) approach to all of them.

One such strong technology is to use device certificates or cryptographic keys on your IoT devices and use them to authenticate messages, proving that the message came from a particular piece of hardware. This of course is not foolproof: a compromised device with a strong key can send some very secure bad messages! But it is a strong defence against simple network-borne attacks like spoofing and man-in-the-middle forgeries.

RKVST already supports high integrity authentication from secure devices through its flexible command authorization scheme (leading to the 'who' in 'who did what when') but this can be added to by also signing the message contents (the 'what') with a device key. This signature is then verifiable independent of RKVST and provides additional proof of authenticity when it's needed.

The `signed-records` sample demonstrates how to integrate message-level signatures from a secure-by-default device into RKVST records, providing an independent measure of integrity and provenance on messages.

## Pre-requisites

* Python 3.7 and later versions are supported.

* Install the RKVST samples package. If you are just trying out the pre-made samples you should get the official [RKVST samples Python package](https://pypi.org/project/jitsuin-archivist-samples/ "PyPi package page") from PyPi. If you are modifying this sample and want to try out your changes then you'll need to rebuild the wheel: please refer to the developer instructions in the top level of this repository to see how to do that.

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [RKVST documentation](https://docs.jitsuin.com/docs/setup-and-administration/getting-access-tokens-using-client-secret/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

The Taskfile in the top level of this repository includes a pre-packaged run of this sample that creates a simulated secure-by-default IoT device, creates an Event with a good signature and another with a hacked signature, and then shows how to verify them.

Please refer to the instructions in the [top level README](https://github.com/jitsuin-inc/archivist-samples#signed-records "signed records sample")

