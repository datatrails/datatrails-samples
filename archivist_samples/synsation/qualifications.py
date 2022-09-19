#   Copyright 2022 RKVST, inc
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# WARNING: Proof of concept code: Not for release
# Copies the flow of the Jitsuinator demo script


# pylint:  disable=missing-docstring

import datetime
from time import strptime
from archivist.errors import ArchivistNotFoundError


def get_employee_record(arch, emp_id):
    try:
        employee_asset = arch.assets.read_by_signature(
            attrs={
                "arc_display_type": "Employee Verification",
                "emp_id": emp_id,
            },
        )

    except ArchivistNotFoundError:
        return None

    if not employee_asset:
        return None

    # Assume emp_id is unique - no safety net here
    return employee_asset["attributes"]


def check_qualification(arch, emp_id, qualification, target_asset):
    # See if we have an employee with this ID and qualification at all
    # Note that this just checks general qualifications, and is not
    # specific to the target device, but it could be restricted further
    # if deemed useful
    record = get_employee_record(arch, emp_id)

    qualification_entries = {"firmware": "f_exp_date", "maintenance": "m_exp_date"}

    if not record:
        res = False
        result = "FAIL"
        message = f"No employee record found for ID {emp_id} with qualification type '{qualification}'"
    else:
        # If we do, check that they are qualified...
        try:
            exp_string = record[qualification_entries[qualification]]

            # ...and the qualification is in date
            expiry_date = datetime.datetime.strptime(exp_string, "%Y-%m-%d")
            if expiry_date < datetime.datetime.now():
                res = False
                result = "FAIL"
                message = f"Employee ID {emp_id} qualification for '{qualification}' has expired"
            else:
                res = True
                result = "PASS"
                message = "Credentials verified and current"

        except KeyError:
            res = False
            result = "FAIL"
            message = f"Employee ID {emp_id} is not qualified for '{qualification}'"

    # Record the facts and return to caller
    props = {
        "operation": "Record",
        "behaviour": "RecordEvidence",
    }
    attrs = {
        "arc_description": f"Verified Employee Qualifications: {result}. {message}.",
        "arc_evidence": message,
        "arc_display_type": "Qualification Check",
        "qualification_result": f"{result}",
    }

    arch.events.create(target_asset, props=props, attrs=attrs, confirm=True)

    return res
