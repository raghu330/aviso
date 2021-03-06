# (C) Copyright 1996- ECMWF.
# 
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import collections.abc
import sys
from typing import Dict

from . import logger


class Config:
    """
    This class is in charge of holding the configuration for the monitoring system, including UDP server and reporters,
    which can be defined by arguments, environment variables or defaults.
    """

    def __init__(self,
                 udp_server=None,
                 monitor_server=None,
                 aviso_rest_reporter=None,
                 aviso_auth_reporter=None,
                 etcd_reporter=None):

        try:
            # we build the configuration in priority order from the lower to the higher
            # start from the defaults
            self._config = self._create_default_config()
            # add environment variables
            Config.deep_update(self._config, self._read_env_variables())
            # add constructor parameters
            self.udp_server = udp_server
            self.monitor_server = monitor_server
            self.aviso_rest_reporter = aviso_rest_reporter
            self.aviso_auth_reporter = aviso_auth_reporter
            self.etcd_reporter = etcd_reporter

            logger.debug(f"Loading configuration completed")

        except Exception as e:
            logger.error(f"Error occurred while setting the configuration, exception: {type(e)} {e}")
            logger.debug("", exc_info=True)
            sys.exit(-1)

    @staticmethod
    def _create_default_config() -> Dict:

        udp_server = {
            "host": "127.0.0.1",
            "port": 1111,
            "buffer_size": 64 * 1024
        }
        # this are the setting for sending the telemetry to a monitoring server like Opsview
        monitor_server = {
            "url": "https://localhost",
            "username": "TBD",
            "password": "TBD",
            "service_host": "aviso",
            "req_timeout": 60,  # seconds

        }
        aviso_rest_reporter = {
            "tlm_type": "rest_resp_time",
            "enabled": False,
            "frequency": 1,  # in minutes
            "warning_t": 10,  # s
            "critical_t": 20,  # s
        }

        aviso_auth_reporter = {
            "tlm_type": "auth_resp_time",
            "enabled": False,
            "frequency": 1,  # in minutes
            "warning_t": 10,  # s
            "critical_t": 20,  # s
            "sub_tlms": []
        }

        etcd_reporter = {
            "enabled": False,
            "frequency": 5,  # in minutes
            "member_urls": ["http://localhost:2379"],
            "tlm_type": ["etcd_store_size", "etcd_cluster_status", "etcd_total_keys"],
            "req_timeout": 60,  # seconds
        }

        # main config
        config = {}
        config["udp_server"] = udp_server
        config["monitor_server"] = monitor_server
        config["aviso_rest_reporter"] = aviso_rest_reporter
        config["aviso_auth_reporter"] = aviso_auth_reporter
        config["etcd_reporter"] = etcd_reporter
        return config

    def _read_env_variables(self) -> Dict:
        config = {}
        # TBD
        return config

    @property
    def udp_server(self):
        return self._udp_server

    @udp_server.setter
    def udp_server(self, udp_server):
        u = self._config.get("udp_server")
        if udp_server is not None and u is not None:
            Config.deep_update(u, udp_server)
        elif udp_server is not None:
            u = udp_server
        # verify is valid
        assert u is not None, "udp_server has not been configured"
        assert u.get("host") is not None, "udp_server host has not been configured"
        assert u.get("port") is not None, "udp_server port has not been configured"
        assert u.get("buffer_size") is not None, "udp_server buffer_size has not been configured"
        self._udp_server = u

    @property
    def monitor_server(self):
        return self._monitor_server

    @monitor_server.setter
    def monitor_server(self, monitor_server):
        m = self._config.get("monitor_server")
        if monitor_server is not None and m is not None:
            Config.deep_update(m, monitor_server)
        elif monitor_server is not None:
            m = monitor_server
        # verify is valid
        assert m is not None, "monitor_server has not been configured"
        assert m.get("url") is not None, "monitor_server url has not been configured"
        assert m.get("username") is not None, "monitor_server username has not been configured"
        assert m.get("password") is not None, "monitor_server password has not been configured"
        assert m.get("service_host") is not None, "monitor_server service_host has not been configured"
        assert m.get("req_timeout") is not None, "monitor_server req_timeout has not been configured"
        self._monitor_server = m

    @property
    def aviso_rest_reporter(self):
        return self._aviso_rest_reporter

    @aviso_rest_reporter.setter
    def aviso_rest_reporter(self, aviso_rest_reporter):
        ar = self._config.get("aviso_rest_reporter")
        if aviso_rest_reporter is not None and ar is not None:
            Config.deep_update(ar, aviso_rest_reporter)
        elif aviso_rest_reporter is not None:
            ar = aviso_rest_reporter
        # verify is valid
        assert ar is not None, "aviso_rest_reporter has not been configured"
        assert ar.get("tlm_type") is not None, "aviso_rest_reporter tlm_type has not been configured"
        assert ar.get("enabled") is not None, "aviso_rest_reporter enabled has not been configured"
        assert ar.get("frequency") is not None, "aviso_rest_reporter frequency has not been configured"
        assert ar.get("warning_t") is not None, "aviso_rest_reporter warning_t has not been configured"
        assert ar.get("critical_t") is not None, "aviso_rest_reporter critical_t has not been configured"
        self._aviso_rest_reporter = ar

    @property
    def aviso_auth_reporter(self):
        return self._aviso_auth_reporter

    @aviso_auth_reporter.setter
    def aviso_auth_reporter(self, aviso_auth_reporter):
        aa = self._config.get("aviso_auth_reporter")
        if aviso_auth_reporter is not None and aa is not None:
            Config.deep_update(aa, aviso_auth_reporter)
        elif aviso_auth_reporter is not None:
            aa = aviso_auth_reporter
        # verify is valid
        assert aa is not None, "aviso_auth_reporter has not been configured"
        assert aa.get("tlm_type") is not None, "aviso_auth_reporter tlm_type has not been configured"
        assert aa.get("enabled") is not None, "aviso_auth_reporter enabled has not been configured"
        assert aa.get("frequency") is not None, "aviso_auth_reporter frequency has not been configured"
        assert aa.get("warning_t") is not None, "aviso_auth_reporter warning_t has not been configured"
        assert aa.get("critical_t") is not None, "aviso_auth_reporter critical_t has not been configured"
        self._aviso_auth_reporter = aa

    @property
    def etcd_reporter(self):
        return self._etcd_reporter

    @etcd_reporter.setter
    def etcd_reporter(self, etcd_reporter):
        e = self._config.get("etcd_reporter")
        if etcd_reporter is not None and e is not None:
            Config.deep_update(e, etcd_reporter)
        elif etcd_reporter is not None:
            e = etcd_reporter
        # verify is valid
        assert e is not None, "etcd_reporter has not been configured"
        assert e.get("tlm_type") is not None, "etcd_reporter tlm_type has not been configured"
        assert e.get("enabled") is not None, "etcd_reporter enabled has not been configured"
        assert e.get("frequency") is not None, "etcd_reporter frequency has not been configured"
        assert e.get("member_urls") is not None, "etcd_reporter member_urls has not been configured"
        assert e.get("req_timeout") is not None, "etcd_reporter req_timeout has not been configured"
        self._etcd_reporter = e

    def __str__(self):
        config_string = (
                f"udp_server: {self.udp_server}" +
                f", monitor_server: {self.monitor_server}" +
                f", aviso_rest_reporter: {self.aviso_rest_reporter}" +
                f", aviso_auth_reporter: {self.aviso_auth_reporter}" +
                f", etcd_reporter: {self.etcd_reporter}"
        )
        return config_string

    def _configure_property(self, param, name):
        value = None
        if param is not None:
            value = param
        elif self._config.get(name) is not None:
            # Setting var from user configuration file
            value = self._config.get(name)
        else:
            logger.error(f"{name} has not been configured")
            sys.exit(-1)
        return value

    @staticmethod
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = Config.deep_update(d.get(k, type(v)()), v)
            else:
                d[k] = v
        return d
