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


class CheckAttribute(base.Scenario):
    """Check instance's attribute values with a given value

    options:
        operator: equal(eq) and not equal(ne)
        target:
        attribute:
        value:
    output: check_attribute_result
    """

    __scenario_type__ = "CheckAttribute"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.instance = self.options.get("target", None)
        self.attribute = self.options.get("attribute", None)
        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        op = self.options.get("operator")
        LOG.debug("options=%s", self.options)
        value1 = self.instance[self.attribute]
        value2 = self.options.get("value", None)
        check_result = "PASS"
        if op == "eq" and value1 != value2:
            LOG.info("value1=%s, value2=%s, error: should equal!!!", value1,
                     value2)
            check_result = "FAIL"
            assert value1 == value2, "Error %s!=%s" % (value1, value2)
        elif op == "ne" and value1 == value2:
            LOG.info("value1=%s, value2=%s, error: should not equal!!!", value1,
                     value2)
            check_result = "FAIL"
            assert value1 != value2, "Error %s==%s" % (value1, value2)
        LOG.info("Check result is %s", check_result)
        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [check_result]
            return self._push_to_outputs(keys, values)
