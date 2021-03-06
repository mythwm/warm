##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from __future__ import print_function
from __future__ import absolute_import

import logging

from yardstick.benchmark.scenarios import base
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class DelNetwork(base.Scenario):
    """Delete an OpenStack network"""

    __scenario_type__ = "DelNetwork"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.network_id = self.options.get("network_id", None)

        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        status = op_utils.delete_neutron_net(self.neutron_client,
                                             network_id=self.network_id)
        if status:
            result.update({"del_network": 1})
            del_status = 1
            LOG.info("Delete network successful!")
        else:
            result.update({"del_network": 0})
            del_status = 0
            LOG.error("Delete network failed!")
        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [del_status]
            return self._push_to_outputs(keys, values)
