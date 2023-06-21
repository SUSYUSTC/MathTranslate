# Copyright 1999-2017 Tencent Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys


class AbstractModel(object):
    """Base class for all models."""
    _headers = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    def _serialize(self, allow_none=False):
        d = vars(self)
        ret = {}
        for k in d:
            if k.startswith("_"):
                continue
            if isinstance(d[k], AbstractModel):
                r = d[k]._serialize(allow_none)
            elif isinstance(d[k], list):
                r = list()
                for tem in d[k]:
                    if isinstance(tem, AbstractModel):
                        r.append(tem._serialize(allow_none))
                    else:
                        r.append(
                            tem.encode("UTF-8") if isinstance(tem, type(u"")) and sys.version_info[0] == 2 else tem)
            else:
                r = d[k].encode("UTF-8") if isinstance(d[k], type(u"")) and sys.version_info[0] == 2 else d[k]
            if allow_none or r is not None:
                ret[k[0].upper() + k[1:]] = r
        return ret


    def _deserialize(self, params):
        return None

    def to_json_string(self, *args, **kwargs):
        """Serialize obj to a JSON formatted str, ensure_ascii is False by default"""
        if "ensure_ascii" not in kwargs:
            kwargs["ensure_ascii"] = False
        return json.dumps(self._serialize(allow_none=True), *args, **kwargs)

    def from_json_string(self, jsonStr):
        """Deserialize a JSON formatted str to a Python object"""
        params = json.loads(jsonStr)
        self._deserialize(params)

    def __repr__(self):
        return "%s" % self.to_json_string()