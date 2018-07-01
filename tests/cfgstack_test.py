#! /usr/bin/env python

import cfgstack, contextlib, datetime, logging, logtool, os, unittest
from functools import partial
from path import Path

# logging.basicConfig (level = logging.DEBUG)

@logtool.log_call
@contextlib.contextmanager
def chdir_ctx (target):
  cwd = os.getcwd ()
  try:
    os.chdir (target)
    yield
  finally:
    os.chdir (cwd)

@logtool.log_call
def dict_compare (d1, d2):
  d1_keys = set (d1.keys ())
  d2_keys = set (d2.keys ())
  intersect_keys = d1_keys.intersection (d2_keys)
  added = d1_keys - d2_keys
  removed = d2_keys - d1_keys
  modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
  same = set (o for o in intersect_keys if d1[o] == d2[o])
  return added, removed, modified, same

class CfgStack_Tests (unittest.TestCase):
  results = [
    {"bill-to": {
      "address": {"city": "Royal Oak",
                  "lines": "458 Walkman Dr.\nSuite #292\n",
                  "postal": 48046,
                  "state": "MI"},
      "family": "Dumars",
      "given": "Chris"},
     "comments": "Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.\n",
     "date": datetime.date(2001, 1, 23),
     "invoice": 34843,
     "product": [{"description": "Basketball",
                  "price": 450.0,
                  "quantity": 4,
                  "sku": "BL394D"},
                 {"description": "Super Hoop",
                  "price": 2392.0,
                  "quantity": 1,
                  "sku": "BL4438H"}],
     "ship-to": {"address": {"city": "Royal Oak",
                             "lines": "458 Walkman Dr.\nSuite #292\n",
                             "postal": 48046,
                             "state": "MI"},
                 "family": "Dumars",
                 "given": "Chris"},
     "tax": 251.42,
     "total": 4443.52},
    {"empty": {"foo": "bar", "password": "sekrit"},
     "mixed": {"foo": "bar", "other": "thing", "password": "ohdear"},
     "partial": {"foo": "baz", "password": "sekrit"},
     "unaffected": [
       {"name": "#mychannel", "password": ""},
       {"name": "#myprivatechannel", "password": "mypassword"}]},
    {"here": "there",
     "problem": {"foo": "baz", "overlay": "power"},
     "this": {
       "foo": "bar",
       "other": "thing",
       "overlay": "power",
       "start": "end"}},
    {"root": {"bottom": "bottom", "override": "test4b", "top": "top"}},
    {"root": {"collector": {"def": "test5",
                            "side": "side",
                            "test5b": "test5b",
                            "this": "that"},
              "nest": {"bird": {"here": "test5", "sparrow": "tweet"},
                       "def": "test5",
                       "side": "side",
                       "test5b": "test5b"},
              "top": "test5b"}},
    {"root": {"second": {
      "block1": {"def": "test6a"},
      "block2": {"def": "test6a", "foo": "bar"},
      "block3": {"def": "local_value"},
      "block_6b": {"def": "test6a", "something": "else"},
      "block_b61": {"def": "test6a"},
      "block_bb2": {"def": "test6b"}}}},
    {"root": {"empty": {"def": "test7a"},
              "other": {"def": "test7a", "thing": "this"},
              "value": {"def": "test7"}}},
    {"root": {"empty": {"def": "simple"},
              "mixed": {"def": "simple", "this": "that"}}},
  ]

#  @logtool.log_call
#  def __init__ (self):
#    for i in xrange (len (results)):
#      setattr (self, "test_test" + i, _partial (self.meta, i))

  @logtool.log_call
  def _meta (self, ndx):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test%d" % ndx)
      d = c.data.to_dict ()
      expected = self.results[ndx - 1]
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test1 (self):
    self._meta (1)

  @logtool.log_call
  def test_test2 (self):
    self._meta (2)

  @logtool.log_call
  def test_test3 (self):
    self._meta (3)

  @logtool.log_call
  def test_test4 (self):
    self._meta (4)

  @logtool.log_call
  def test_test5 (self):
    self._meta (5)

  @logtool.log_call
  def test_test6 (self):
    self._meta (6)

  @logtool.log_call
  def test_test7 (self):
    self._meta (7)

  @logtool.log_call
  def test_test8 (self):
    self._meta (8)

if __name__ == "__main__":
  unittest.main()
