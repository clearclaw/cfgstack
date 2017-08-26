#! /usr/bin/env python

import logging, pprint, sys
from cfgstack import CfgStack

# logging.basicConfig (level = logging.DEBUG)

c = CfgStack (sys.argv[1])
print pprint.pformat (c.data.to_dict ())