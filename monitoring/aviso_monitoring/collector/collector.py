# (C) Copyright 1996- ECMWF.
# 
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from abc import ABC
from threading import Thread

from .. import logger
from .transmitter import Transmitter
from .config import Config

class Collector(ABC):
    """
    This class is responsible for collecting a telemetry and to transmit it. It's an abstract class as it is assumed 
    that the details on how and what to collect are in its specialisation.
    """
    def __init__(self, config: Config) -> None:
        self.enabled = config.enabled
        self.telemetry_type = config.telemetry_type
        # create a buffer for the measurements collected
        self.tlm_buffer = []
        self.transmitter = Transmitter(
            config.transmitter, 
            self.tlm_buffer, 
            self.aggregate_tlms, 
            self.telemetry_type)
        # start the transmitter
        if self.enabled:
            self.transmitter.start()
            
    def aggregate_tlms(self, tlms):
        """
        This method aggregates the measurements collected in the buffer and create a tlm out of them

        Args:
            tlms (List): List of measurements to aggregates
        """
        pass