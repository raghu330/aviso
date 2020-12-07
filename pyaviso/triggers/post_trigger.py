# (C) Copyright 1996- ECMWF.
# 
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import requests
import json
from typing import Dict
import uuid
import datetime
import importlib
from enum import Enum

from . import trigger
from .trigger import TriggerType
from .. import logger
from ..custom_exceptions import TriggerException


class ProtocolType(Enum):
    """
    Enum for the various protocols accepted by the post triggers
    """
    cloudevent = ("post_trigger", "PostCloudEvent")

    def get_class(self):
        module = importlib.import_module("pyaviso.triggers."+self.value[0])
        return getattr(module, self.value[1])

class PostTrigger(trigger.Trigger):
    """
    This class implements a trigger in charge of posting the notification accordingly to the protocol selected.
    This class expects the param protocol and protocol type. The remaining fields are optional.
    """

    def __init__(self, notification: Dict, params: Dict):
        trigger.Trigger.__init__(self, notification, params)
        assert params.get("protocol") is not None, "protocol is a mandatory field" 
        protocol_params = params.get("protocol")
        assert protocol_params.get("type") is not None, "protocol type is a mandatory field" 
        self.protocol = ProtocolType[protocol_params.get("type").lower()].get_class()(notification, protocol_params)

    def execute(self):
        logger.info(f"Starting Post Trigger for (params.get('protocol'))...'")
        
        # execute the specific protocol
        self.protocol.execute()

        logger.debug(f"Post Trigger completed")


class PostCloudEvent():
    """
    This class implements a trigger in charge of translating the notification in a CloudEvent message and 
    POST it to the URL specified by the user.
    This class expects the params to contain the URL where to send the message to. The remaining fields are optional.
    """
    TIMEOUT_DEFAULT = 60
    TYPE_DEFAULT = "aviso"
    SOURCE_DEFAULT = "https://aviso.ecmwf.int"

    def __init__(self, notification: Dict, params: Dict):
        self.notification = notification
        assert params.get("url") is not None, "url is a mandatory field"
        self.url = params.get("url")
        self.timeout = params.get("timeout", self.TIMEOUT_DEFAULT)
        self.headers = params.get("headers", {})

        # cloudEvent specific fields
        if  params.get("cloudevent"):
            self.type = params.get("cloudevent").get("type", self.TYPE_DEFAULT)
            self.source = params.get("cloudevent").get("source", self.SOURCE_DEFAULT)
        else:
            self.type = self.TYPE_DEFAULT
            self.source = self.SOURCE_DEFAULT


    def execute(self):
        
        # prepare the CloudEvent message
        data = {
            "type": self.type,
            "data": self.notification,
            "datacontenttype": "application/json",
            "id": str(uuid.uuid4()),
            "source": self.source,                    
            "specversion": "1.0",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        logger.debug(f"Sending CloudEvent notification {data}")

        # send the message
        try:
            resp = requests.post(self.url, json=data, headers=self.headers, verify=False, timeout=self.timeout)
        except Exception as e:
            logger.error("Not able to POST CloudEvent notification")
            raise TriggerException(e) 
        if resp.status_code != 200:
            raise TriggerException(f"Not able to POST CloudEvent notification to {self.url}, "
                         f"status {resp.status_code}, {resp.reason}, {resp.content.decode()}")
             
        logger.debug(f"CloudEvent notification sent successfully")