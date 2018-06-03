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

import json

from taf.foundation.utils import YAMLData


class Client(object):
    def __init__(
            self,
            base_url,
            port=None,
            username=None,
            password=None,
            **kwargs
    ):
        import sys

        if sys.version_info.major < 3:
            from urlparse import urlparse
        else:
            from urllib.parse import urlparse

        _url = urlparse(base_url)

        if port and str(port).strip():
            assert str(port).strip().isdigit(), \
                'Invalid port number'

            _url._replace(
                netloc='{}:{}'.format(
                    _url.hostname,
                    str(port).strip()
                )
            )

        kwargs.update(
            url=_url.geturl(),
            username=username,
            password=password
        )

        self.params = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *args):
        raise NotImplementedError(
            'Close connection'
        )

    def get(
            self,
            resource,
            **kwargs
    ):
        raise NotImplementedError(
            'GET - To retrieve a resource'
        )

    def post(
            self,
            resource,
            data=None,
            **kwargs
    ):
        raise NotImplementedError(
            'POST - To create a resource,'
            'or to execute a complex operation on a resource'
        )

    def put(
            self,
            resource,
            data=None,
            **kwargs
    ):
        raise NotImplementedError(
            'PUT - To update a resource'
        )

    def delete(
            self,
            resource,
            **kwargs
    ):
        raise NotImplementedError(
            'DELETE - To delete a resource'
        )

    def patch(
            self,
            resource,
            data=None,
            **kwargs
    ):
        raise NotImplementedError(
            'PATCH - To perform a partial update to a resource'
        )

    @classmethod
    def decode(cls, json_string):
        try:
            json_string = json.loads(json_string)

            if isinstance(json_string, dict):
                _model = YAMLData(
                    **json_string
                )
            else:
                _model = json_string
        except (TypeError, ValueError):
            _model = {}

        return _model

    @classmethod
    def encode(cls, model):
        def _iter_encode(data):
            _json = {}

            if isinstance(data, YAMLData):
                data = vars(data)

            if isinstance(data, dict):
                for key, value in data.items():
                    _json[key] = _iter_encode(value)
            elif isinstance(data, (list, tuple)):
                _json = [
                    _iter_encode(item) for item in data
                ]
            else:
                # Arbitrarily raise potential exception
                # for unknown model
                _json = data

            return _json

        return json.dumps(
            _iter_encode(model),
            indent=2,
            sort_keys=True
        )
