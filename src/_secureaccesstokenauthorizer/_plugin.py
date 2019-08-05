# Copyright 2019 PrivateStorage.io, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The Twisted plugin that glues the Zero-Knowledge Access Pass system into
Tahoe-LAFS.
"""

import attr

from zope.interface import (
    implementer,
)

from twisted.internet.defer import (
    succeed,
)

from allmydata.interfaces import (
    IFoolscapStoragePlugin,
    IAnnounceableStorageServer,
)

from .api import (
    ZKAPAuthorizerStorageServer,
    ZKAPAuthorizerStorageClient,
)

from ._storage_server import (
    TOKEN_LENGTH,
)

from .resource import (
    from_configuration as resource_from_configuration,
)

@implementer(IAnnounceableStorageServer)
@attr.s
class AnnounceableStorageServer(object):
    announcement = attr.ib()
    storage_server = attr.ib()



@implementer(IFoolscapStoragePlugin)
class ZKAPAuthorizer(object):
    """
    A storage plugin which provides a token-based access control mechanism on
    top of the Tahoe-LAFS built-in storage server interface.
    """
    name = u"privatestorageio-satauthz-v1"

    def get_storage_server(self, configuration, get_anonymous_storage_server):
        announcement = {}
        storage_server = ZKAPAuthorizerStorageServer(
            get_anonymous_storage_server(),
            **configuration
        )
        return succeed(
            AnnounceableStorageServer(
                announcement,
                storage_server,
            ),
        )


    def get_storage_client(self, configuration, announcement, get_rref):
        return succeed(
            ZKAPAuthorizerStorageClient(
                get_rref,
                lambda: [b"x" * TOKEN_LENGTH],
            )
        )


    def get_client_resource(self, node_config):
        return resource_from_configuration(node_config)
