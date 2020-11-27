# (C) Copyright 1996- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from .. import logger
from .etcd_monitor import EtcdMonitor
from .aviso_rest_monitor import AvisoRestMonitor
from .aviso_auth_monitor import AvisoAuthMonitor


class MonitorFactory:
    def __init__(self, config):

        # instantiate the various monitors
        self.monitors = [
            EtcdMonitor(config),
            AvisoRestMonitor(config),
            AvisoAuthMonitor(config),
            ]