# Copyright (c) 2018 Tencent Ltd.
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


class HttpProfile(object):
    scheme = "https"

    def __init__(self, protocol=None, endpoint=None, reqMethod="POST", reqTimeout=60,
                 keepAlive=False, proxy=None, rootDomain=None, certification=None):
        """HTTP profile.
        :param protocol: http or https, default is https.
        :type protocol: str
        :param endpoint: The domain to access, like: cvm.tencentcloudapi.com
        :type endpoint: str
        :param reqMethod: the http method, valid choice: GET, POST
        :type reqMethod: str
        :param reqTimeout: The http timeout in second.
        :type reqTimeout: int
        :param rootDomain: The root domain to access, like: tencentcloudapi.com.
        :type rootDomain: str
        """
        self.endpoint = endpoint
        self.reqTimeout = 60 if reqTimeout is None else reqTimeout
        self.reqMethod = "POST" if reqMethod is None else reqMethod
        self.protocol = protocol or "https"
        # protocol is not precise word according to rfc
        self.scheme = self.protocol
        self.keepAlive = keepAlive
        self.proxy = proxy
        self.rootDomain = "tencentcloudapi.com" if rootDomain is None else rootDomain
        self.certification = certification