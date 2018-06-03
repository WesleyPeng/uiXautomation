# Copyright (c) 2017-2018 {Flair Inc.} WESLEY PENG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib3
from requests.auth import HTTPBasicAuth
from requests.sessions import Session

from taf.foundation.api.svc.REST import Client


class RESTClient(Session, Client):
    def __init__(
            self,
            base_url,
            port=None,
            username=None,
            password=None,
            **kwargs
    ):
        Session.__init__(self)

        Client.__init__(
            self, base_url, port,
            username, password, **kwargs
        )

        self.verify = False

        self._set_auth(
            password, username
        )

        urllib3.disable_warnings()

    def get(self, url, **kwargs):
        return Session.get(
            self,
            self._get_resource_uri(url),
            **self._set_default_timeout(
                **kwargs
            )
        )

    def post(
            self,
            url,
            data=None,
            json=None,
            **kwargs
    ):
        return Session.post(
            self,
            self._get_resource_uri(url),
            data, json,
            **self._set_default_timeout(
                **kwargs
            )
        )

    def put(self, url, data=None, **kwargs):
        return Session.put(
            self,
            self._get_resource_uri(url),
            data,
            **self._set_default_timeout(
                **kwargs
            )
        )

    def delete(self, url, **kwargs):
        return Session.delete(
            self,
            self._get_resource_uri(url),
            **self._set_default_timeout(
                **kwargs
            )
        )

    def patch(self, url, data=None, **kwargs):
        return Session.patch(
            self,
            self._get_resource_uri(url),
            data,
            **self._set_default_timeout(
                **kwargs
            )
        )

    def _set_auth(
            self,
            username,
            password
    ):
        self.auth = HTTPBasicAuth(
            username,
            password
        )

    def _get_resource_uri(self, resource):
        import sys

        if sys.version_info.major < 3:
            from urlparse import urljoin
        else:
            from urllib.parse import urljoin

        return urljoin(
            self.params.get('url'),
            resource
        )

    def _set_default_timeout(self, **kwargs):
        kwargs.setdefault(
            'timeout',
            self.params.get('timeout', 60)
        )

        return kwargs
