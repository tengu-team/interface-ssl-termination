#!/usr/bin/env python3
# Copyright (C) 2017  Qrama, developed by Tengu-team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406

from charms.reactive import (
    when_any,
    when_not,
    set_flag,
    clear_flag,
    Endpoint,
)


class SSLTerminationProvides(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def client_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def client_broken(self):
        clear_flag(self.expand_name('available'))

    @when_any('endpoint.{endpoint_name}.departed',
              'endpoint.{endpoint_name}.changed.cert-request')
    def client_changed(self):
        set_flag(self.expand_name('update'))
        clear_flag(self.expand_name('departed'))
        clear_flag(self.expand_name('changed.cert-request'))

    def get_cert_requests(self):
        cert_requests = []
        for relation in self.relations:
            for unit in relation.units:
                request = unit.received['cert-request']
                if request:
                    request['juju_unit'] = unit.unit_name
                    cert_requests.append(request)
        return cert_requests

    def send_status(self, status):
        for relation in self.relations:
            relation.to_publish['status'] = status
