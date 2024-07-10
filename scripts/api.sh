#!/bin/sh
#
# Executes a command inside the api container
#
# Usage Examples
#
#     ./scripts/api.sh /bin/bash   # for shell
#     ./scripts/api.sh             # enters python REPL
#     ./scripts/api.sh ....

docker run \
    --rm -it \
    -v $(pwd):/home/api \
    -u $(id -u):$(id -g) \
    -e TEST_ARCHIVIST \
    -e TEST_AUTHTOKEN_FILENAME \
    -e TEST_NAMESPACE \
    -e TEST_PARTNER_ID \
    -e TEST_SELECTOR \
    -e TEST_VERBOSE \
    -e GITHUB_REF \
    -e TWINE_USERNAME \
    -e TWINE_PASSWORD \
    datatrails-samples-api \
    "$@"
