#!/usr/bin/env bash
#
# Manual testing of the wheel package.
#
# 'task wheel' to generate installable wheel package generated locally.
#
# Populate the credentials directory with auth token.
# The auth token must be for a particular tenant identity.
#
rm -rf samples-venv
python3 -m venv samples-venv
source samples-venv/bin/activate
function finalise {
    deactivate
    rm -rf samples-venv
}
trap finalise EXIT

# do everything in sub directory to ensure that wheel is used and not local code.
(export TEST_AUTHTOKEN_FILENAME=../${TEST_AUTHTOKEN_FILENAME} \
    && cd samples-venv \
    && python3 -m pip install -q ../dist/datatrails_samples-*.whl \
    && ../scripts/samples.sh functests)



