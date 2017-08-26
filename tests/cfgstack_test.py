#! /usr/bin/env python

import cfgstack, contextlib, datetime, logging, logtool, os, unittest
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

  @logtool.log_call
  def test_test1 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test1")
      d = c.data.to_dict ()
      expected = {
        "bill-to": {
          "address": {
            "city": "Royal Oak",
            "lines": "458 Walkman Dr.\nSuite #292\n",
            "postal": 48046,
            "state": "MI",
          },
          "family": "Dumars",
          "given": "Chris",
        },
        "comments": "Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.\n",
        "date": datetime.date (2001, 1, 23),
        "invoice": 34843,
        "product": [
          {
            "description": "Basketball",
            "price": 450.0,
            "quantity": 4,
            "sku": "BL394D",
          },
          {
            "description": "Super Hoop",
            "price": 2392.0,
            "quantity": 1,
            "sku": "BL4438H",
          },
        ],
        "ship-to": {
          "address": {
            "city": "Royal Oak",
            "lines": "458 Walkman Dr.\nSuite #292\n",
            "postal": 48046,
            "state": "MI"},
          "family": "Dumars",
          "given": "Chris",
        },
        "tax": 251.42,
        "total": 4443.52,
      }
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test2 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test2")
      d = c.data.to_dict ()
      expected = {
        'empty': {'foo': 'bar', 'password': 'sekrit'},
        'mixed': {'foo': 'bar', 'other': 'thing', 'password': 'ohdear'},
        'partial': {'foo': 'baz', 'password': 'sekrit'},
        'unaffected': [{'name': '#mychannel', 'password': ''},
                       {'name': '#myprivatechannel',
                        'password': 'mypassword'}]}
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test3 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test3")
      d = c.data.to_dict ()
      expected = {
        "this": {
          "start": "end",
          "foo": "bar",
          "other": "thing",
          "overlay": "power",
        },
        "problem": {
          "foo": "baz",
          "overlay": "power",
        },
        "here": "there",
      }
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test4 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test4")
      d = c.data.to_dict ()
      expected = {
        "root": {
          "bottom": "bottom",
          "override": "test4b",
          "top": "top",
        },
      }
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test5 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test5")
      d = c.data.to_dict ()
      expected = {
        "root": {
          "collector": {
            "def": "test5a",
            "side": "side",
            "test5b": "test5b",
            "this": "test5b",
          },
          "nest": {
            "bird": {
              "here": "test5",
              "sparrow": "tweet",
            },
            "def": "test5a",
            "side": "side",
            "test5b": "test5b"
          },
          "top": "test5b",
        },
      }
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

  @logtool.log_call
  def test_test6 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test5")
      d = c.data.to_dict ()
      expected = {'root': {'second': {'block1': {'def': 'test6a'},
                     'block2': {'def': 'test6a', 'foo': 'bar'},
                     'block3': {'def': 'local_value'},
                     'block_6b': {'def': 'test6a', 'something': 'else'},
                     'block_b61': {'def': 'test6a'},
                     'block_bb2': {'def': 'test6b'}}}}
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})


  @logtool.log_call
  def test_test6 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test5")
      d = c.data.to_dict ()
      expected = {'root': {'second': {'block1': {'def': 'test6a'},
                     'block2': {'def': 'test6a', 'foo': 'bar'},
                     'block3': {'def': 'local_value'},
                     'block_6b': {'def': 'test6a', 'something': 'else'},
                     'block_b61': {'def': 'test6a'},
                     'block_bb2': {'def': 'test6b'}}}}
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})


  @logtool.log_call
  def test_test8 (self):
    with Path ("tests"):
      c = cfgstack.CfgStack ("test8")
      d = c.data.to_dict ()
      expected = {'root': {'empty': {'def': 'simple'},
          'mixed': {'def': 'simple', 'this': 'that'}}}
      added, removed, modified, same = dict_compare (expected, d)
      self.assertEqual (added, set ([]))
      self.assertEqual (removed, set ([]))
      self.assertEqual (modified, {})

if __name__ == "__main__":
  unittest.main()
