# archivist-samples - developers

Sample python code that uses the archivist python SDK to manage particular types of assets
such as 'doors', 'cards', 'containers' etc.

This document describes how to test any modifications made to the codebase.

# Developer Pre-requisites

Required tools for modifying this repo are task-runner and docker-ce.

  - Install task runner: https://github.com/go-task/task
  - Install docker-ce: https://docs.docker.com/get-docker/

A running archivist instance which allows creation of arbitrary assets etc. This is usually
a test or demo system and **not** a production system.

# Running the samples code

Clone this repo and cd into the root directory of the repo.

## Pre-requisites

Python 3.6 and later versions are supported.

Build the docker image:

```bash
task api
```

## Authorization 

Add a token to the file credentials/.auth_token and set some environment vars to
specify the archivist endpoint:

```bash
export TEST_ARCHIVIST="https://rkvst.poc.jitsuin.io"
export TEST_AUTHTOKEN_FILENAME=credentials/.auth_token
export TEST_NAMESPACE="unique label"
export TEST_VERBOSE=-v
export TEST_PROOF_MECHANISM="-i SIMPLE_HASH"
```

If TEST_VERBOSE is "-v" debugging output will appear when running the tests.

TEST_PROOF_MECHANISM must be either "KHIPU" or "SIMPLE_HASH"

## TEST_NAMESPACE

If TEST_NAMESPACE is blank or unspecified then each execution of './scripts/samples.sh' will not be
independent. Any assets events, locations will be visible to other users running the same tests
on the same URL.

Each example test creates assets,events,locations that are not visible to other example tests.
For example the door_entry assets,events etc are not visible to the synsation example tests.

Assets and locations are only created if they do not already exist according to namespace.

Due to restrictions attachments are always uploaded during every test execution.

Events are created every execution of a test - currently no check is done if the event already exists.

A special value of TEST_NAMESPACE:

```bash
export TEST_NAMESPACE=date
```

will set the namespace to the result of `date +%s` i.e. no. of seconds since epoch. This effectively makes
each test run independently of every other test run.

## TESTS

To see what tests are available specify the help option:

```bash
TEST_SELECTOR=help task samples

Available functional tests are:

    TEST_SELECTOR=door_entry task samples
    TEST_SELECTOR=estate_info task samples
    TEST_SELECTOR=signed_records task samples
    TEST_SELECTOR=synsation_initialise task samples
    TEST_SELECTOR=synsation_analyze task samples
    TEST_SELECTOR=synsation_charger task samples
    TEST_SELECTOR=synsation_jitsuinator task samples
    TEST_SELECTOR=synsation_wanderer task samples

To run more than one test use a comma-separated list:

    TEST_SELECTOR=door_entry,estate_info task samples

To run all tests:

    TEST_SELECTOR=all task samples
```

and follow the instructions.

For example:

```bash
TEST_SELECTOR=door_entry,estate_info task samples
TEST_SELECTOR=all task samples
```

Note that the synsation example tests all share the same NAMESPACE.

