# -*- coding: utf-8 -*-
#
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
import os
import json

from mathtranslate.tencentcloud.common.abstract_client import AbstractClient
from mathtranslate.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


class CommonClient(AbstractClient):
    """
    使用CommonClient，可以只安装tencentcloud-sdk-python-common包，即可调用各个产品的接口
    使用详情见github示例

    """

    def __init__(self, service, version, credential, region, profile=None):
        """
        :param credential: 接口调用凭证
        :type credential: tencentcloud.common.credential.Credential or tencentcloud.common.credential.STSAssumeRoleCredential or None
        :param region: 接口调用地域
        :type region: str
        :param version: 接口版本
        :type version: str
        :param service: 接口产品
        :type service: str
        :param profile: 请求网络信息
        :type profile: tencentcloud.common.profile.client_profile.ClientProfile
        """
        if region is None or version is None or service is None:
            raise TencentCloudSDKException("CommonClient Parameter Error, "
                                           "credential region version service all required.")
        self._apiVersion = version
        self._service = service
        super(CommonClient, self).__init__(credential, region, profile)