# Document Lineage Sample

RKVST offers complete document lineage.

This sample focuses on an invoice document for a fabricated Asteroid Mining Company.

It shows the evolution of an invoice document over time, where each version adds or ammends information to the invoice:

* Version 1 - Standard invoice
* Version 2 - Updates the invoice with an order number
* Version 3 - Updates the invoice with a discount
 
This sample shows that although there are multiple versions of the invoice, with varying
amounts of money, it is clear to both the selling and buying party, which version is correct. In this case the latest version is correct.

If the document contains sensitive information, it is also possible to just provide the document hash without uploading the sensitive document.

## Pre-requisites

* Python 3.7 and later versions are supported.

* Install the [RKVST samples Python package](https://pypi.org/project/rkvst-samples/ "PyPi package page")

* Get an authorization bearer token and store it in the file `credentials/.auth_token`. If you don't know how to do this, please refer to the [RKVST documentation](https://docs.rkvst.com/docs/rkvst-basics/getting-access-tokens-using-app-registrations/ "Getting an auth token"). Make sure that the `credentials` folder is suitably restricted by disallowing root and group access.


## Running the sample

First acquire an auth token and put it in the following file:

```
credentials/.authtoken
```

To run the sample: 

```bash
archivist_samples_document [-v] -t credentials/.authtoken
```

## Using the Document class

The Document class can create a Document Asset and currently has the ability to add
`publish` events to that Document Asset.

### Creating a Document

To create a brand new Document Asset, use `document.create()`.

see `run.py` for example.

### Publishing a new Document Version


To publish a new version of a document, use `document.publish()`.

see `run.py` for example.

## Public Access

By default the document created is private, and cannot be viewed publically.