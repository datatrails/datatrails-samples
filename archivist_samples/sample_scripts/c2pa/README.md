# Purpose

The purpose of this sample is to demonstrate how one can record and trace the lifecycle of an embedded file manifest within DataTrails thus providing a historical chain of events of wanted or unwanted changes and/or updates.

It creates 2 separate assets, controlled by different credentials, to show how potentially malicious redaction or stripping of provenance information can be detected and proven.

# Installation

## Prerequisite:

This script uses the C2PA command line utility to create asset-embedded manifests and other output files. Please install this utility before executing this script. 

[Install C2PA Command Line Utility](https://github.com/contentauth/c2patool)

C2PA Readme sections relevant to this script: 
- Adding a manifest to an asset file 
- Specifying a parent file 
- Creating an ingredient from a file 
- Detail manifest report 

## Environment Variables

There are two app registrations that represent each actor within the script.  The information obtained by the app registration (client id and client secret) are referenced by using environment variables. 

To create an DataTrails App Registrtaion feel free to reference our [documentation](https://docs.datatrails.ai/developers/developer-patterns/getting-access-tokens-using-app-registrations/). 

### Note: One does not have to create a JWT token for the REST API, just the app registrations in the DataTrails tenant settings.

Please set the below environment variables, they represent the client id and location of client secret for DataTrails app registrations:

```bash
export HONEST_CLIENT_ID=”client id for Honest Abe” 
export HONEST_CLIENT_SECRET_FILENAME=”credentials/.honest_secret” 
export EVIL_CLIENT_ID=”client id for Evil Eddie” 
export EVIL_C2_CLIENT_SECRET_FILENAME=”credentials/.evil_secret” 
```

In addition, this script utilizes the DataTrails Python3 SDK, located [here](https://github.com/datatrails/datatrails-python).  This is not a requirement as DataTrails APIs are code agnostic. 

# Scenario

The scenario executed within this script involves two actors, one is good (Honest Abe) and one is nefarious (Evil Eddie).  Honest Abe is a music journalist that is creating and recording asset-embedded manifest for digital content to be used for ACL (Austin City Limits) articles.  Evil Eddie is a fellow colleague that likes to make changes to digital content that will be used for articles not written by him.  Eddie believes his changes will make his co-workers articles better, however they often do not. 

When changes are made, they are hard to track and cause timeline delays, as Eddie’s colleagues try to find the original digital content that an individual usually removes.  Now that DataTrails is being used, all asset-embedded manifests for digital content are recorded including: the original content, any changes/updates and related detail files.  

There are two digital content assets recorded within DataTrails one by Honest Abe and the other by Evil Eddie.  Eddie and Abe have both recorded and published the same asset however Eddie has made changes to the manifest and began recording changes in DataTrails alongside Abe.  Now we have two assets that are the same, with the same journey and the same versions. Which one is the correct one?   

This can be identified by using the Instaproof feature within DataTrails and downloading the json files within the details event and locating the redacting information or downloading the images and using the [Verify](https://verify.contentauthenticity.org/inspect) tool, one will see “open” information has been removed from the content credentials.  
