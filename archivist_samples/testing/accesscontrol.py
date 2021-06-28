#   Copyright 2019-2020 Jitsuin, inc
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

"""Access control utilities for interacting with Jitsuin Archivist"""

# may become a separate jitsuin wheel package?

import datetime
import json
import requests

from archivist.archivist import Archivist
from archivist.logger import LOGGER

# Types
#######


class ArchivistUserException(Exception):
    """Exceptions in ArchivistUser defintions and behaviours"""


class ArchivistOrganizationException(Exception):
    """Exceptions in ArchivistOrganization defintions and behaviours"""


class ArchivistAccessException(Exception):
    """Exceptions for access control errors and violations"""


class ArchivistUser:
    """Encapsulates an Archivist user principal
    @userparams@ is a dictionary filled with necessary user config"""

    def __init__(self, userparams, uri):
        self._name = userparams["name"]
        self._email = userparams["email"]
        self._authparams = userparams["authentication"]
        self._arcnode = uri
        self._jwt = ""
        self._jwtexpiry = None
        self._archivist = None
        self._endpoint = None

    def __eq__(self, other):
        """ArchivistUsers are considered equal if they have the same name
        and email address and are affiliated to the same archivist node"""
        if isinstance(other, ArchivistUser):
            if (
                (self.email == other.email)
                and (self.name == other.name)
                and (self.arcnode == other.arcnode)
            ):
                return True

        return False

    def __hash__(self):
        """ArchivistUsers are considered equal if they have the same name
        and email address and are affiliated to the same archivist node"""
        unique = self.email + self.name + self.arcnode
        return hash(unique)

    def _refreshAAD(self, force=False):
        """Fetch an authtoken from the AAD OAUTH v2.0 endpoint"""
        if self._authparams["type"] != "AzureAD":
            raise ArchivistUserException(
                f"IDP {self._authparams['type']} doesn't match 'AzureAD'"
            )

        # Don't do it if you don't need to...
        if self._jwtexpiry and not force:
            tolerance = self._jwtexpiry - datetime.timedelta(minutes=5)
            if tolerance > datetime.datetime.now():
                dbgstr = f"Token not yet expired. Not refreshing until {tolerance}"
                LOGGER.debug(dbgstr)
                return

        self._endpoint = self._arcnode  # pylint: disable=attribute-defined-outside-init
        scope = f"{self._arcnode}/.default"
        post_data = {
            "grant_type": "client_credentials",
            "client_id": self._authparams["appid"],
            "client_secret": self._authparams["secret"],
            "scope": scope,
        }

        response = requests.post(self._authparams["oauth_url"], data=post_data)
        LOGGER.debug(response)

        values = parse_json_response(response)
        if not values or not "access_token" in values:
            raise ArchivistAccessException("No JWT returned in token refresh attempt")

        self._jwt = values["access_token"]
        LOGGER.debug(self._jwt)

        if "expires_in" in values:
            expseconds = int(values["expires_in"])
            self._jwtexpiry = datetime.datetime.now() + datetime.timedelta(expseconds)
            dbgstr = f"Token will expire at {self._jwtexpiry}"
            LOGGER.debug(dbgstr)
        else:
            self._jwtexpiry = None

    def _refreshFAM(self, params):  # pylint: disable=no-self-use
        raise ArchivistAccessException("Forgerock token refresh NYI")

    def _refreshPO(self, params):  # pylint: disable=no-self-use
        raise ArchivistAccessException("Ping One token refresh NYI")

    def _refreshMTLS(self):
        """Pick up key and cert for mutual TLS"""
        # MTLS doesn't need to refresh tokens but it does have a special
        # endpoint to connect to, so over-ride the path
        self._endpoint = self._arcnode.replace(
            "https://", "https://auth."
        )  # pylint: disable=attribute-defined-outside-init

    def connect(self):
        """Get a credential and create an Archivist connection"""
        authmethods = {
            "AzureAD": self._refreshAAD,
            "ForgerockAM": self._refreshFAM,
            "PingOne": self._refreshPO,
            "TLSClientAuth": self._refreshMTLS,
        }
        if self._authparams["type"] not in authmethods:
            raise ArchivistAccessException(
                f"Unsupported authentication method '{self._authparams['type']}'"
            )

        authmethods[self._authparams["type"]]()

        self._archivist = Archivist(
            self._endpoint,
            auth=self._jwt,
            cert=self._authparams["certfile"]
            if "certfile" in self._authparams
            else None,
        )

        if not self._archivist:
            raise ArchivistUserException("Connection to Archivist failed")

    @property
    def name(self):
        """return the name of the user

        Returns:
            [type]: name of the user
        """
        return self._name

    @property
    def email(self):
        """return the email of the user

        Returns:
            [type]: email of the user
        """
        return self._email

    @property
    def arcnode(self):
        """return the arcnode of the user

        Returns:
            [type]: arcnode of the user
        """
        return self._arcnode

    @property
    def endpoint(self):
        """return the endpoint that the user need to connect to

        Returns:
            [type]: [description]
        """
        return self._endpoint

    @property
    def archivist(self):
        """return the archivist connection

        Returns:
            [type]: archivist connection
        """
        return self._archivist


class ArchivistOrganization:
    """Encapsulates an Archivist organization principal
    @userparams@ is a dictionary filled with necessary organization config"""

    def __init__(self, orgparams):
        self._arcnode = orgparams["arcnode"]
        self._name = orgparams["name"]
        self._subject = orgparams["subject"]
        self._users = set()

    @property
    def name(self):
        """return the name of the archivist organization

        Returns:
            [type]: name of the archivist organization
        """
        return self._name

    @property
    def idp(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._idp  # pylint: disable=no-member

    @property
    def archivist(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._archivist  # pylint: disable=no-member

    def add_user(self, userparams):
        """Creates a new ArchivistUser and adds it to this Organization's
        user list."""
        self._users.add(ArchivistUser(userparams, self._arcnode))

    def find_user(self, name=None, email=None):
        """Find a user from this organization's user list by name or
        email. If both name and email are specified then BOTH must
        match"""
        if not name and not email:
            return None

        for u in self._users:
            found = True
            if name and u.name != name:
                found = False
                continue
            if email and u.email != email:
                found = False
                continue

            if found:
                return u

        return None


# Utilities
###########


def parse_users(usersfile):
    """Reads a JSON file and returns a list of ArchivistOrganization
    objects,populated with their ArchivistUsers"""
    orgs = {}

    with open(usersfile, mode="r") as fd:
        rawusers = json.load(fd)

    # Now initialize all the orgs/users
    for org in rawusers["organizations"]:
        neworg = ArchivistOrganization(org)
        orgs[neworg.name] = neworg
        for user in org["users"]:
            neworg.add_user(user)

    return orgs


def parse_json_response(response):
    """[summary]

    Args:
        response ([type]): [description]

    Returns:
        [type]: [description]
    """
    if response.status_code != 200:
        LOGGER.debug(
            "Call failed: status %d - '%s", response.status_code, response.text
        )

        return None

    try:
        json_result = response.json()
        LOGGER.debug(json.dumps(json_result, indent=2, sort_keys=False))
        return json_result
    except ValueError:
        LOGGER.debug("No JSON content - cannot decode response")

    return None
