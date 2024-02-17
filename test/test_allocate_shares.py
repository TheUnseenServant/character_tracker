#!/usr/bin/env python

# name    :  test_allocate_shares.py
# version :  0.0.1
# date    :  20231010
# author  :
# desc    :

import os.path
import tempfile
import unittest

import allocate_shares as a_s


class TestShares(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.test_dir.name, "data.csv")
        with open(self.data_file, "w") as f:
            f.write("name;coin;xp\n")
            f.write("pc1;1;1\n")
            f.write("pc2;1;1\n")
            f.write("npc1;0.5;0.5\n")
            f.write("npc2;0;0.5\n")

        self.data = {
            "pc1": [1, 1],
            "pc2": [1, 1],
            "npc1": [0.5, 0.5],
            "npc2": [0, 0.5],
        }

    def tearDown(self):
        self.test_dir.cleanup()

    def test_members_from_csv(self):
        members = a_s.members_from_csv(self.data_file)
        self.assertEqual(len(members), 4)
        self.assertEqual(members[0].name, "pc1")

    def test_share_results(self):
        t = a_s.Treasure({"coin": 100, "xp": 100, "mis": 100})
        s = a_s.Shares({"coin": 3, "xp": 2.5})
        s.one_share(t)
        self.assertEqual(s.coin, 31)
        self.assertEqual(s.mis, 33)
        self.assertEqual(s.xp, 80)

    def test_member_basic(self):
        t = a_s.Treasure({"coin": 100, "xp": 50, "mis": 100})
        s = a_s.Shares({"coin": 3, "xp": 2.5})
        s.one_share(t)
        member = {"name": "fred", "coin": 0.5, "xp": 0.5}
        m = a_s.Member(member)
        m.give_shares(s)
        self.assertEqual(m.name, "fred")
        self.assertEqual(m.share_coin, 0.5)
        self.assertEqual(m.share_xp, 0.5)
        self.assertEqual(m.share_mis, 0.5)
        self.assertEqual(m.coins, 15)
        self.assertEqual(m.mis, 16)
        self.assertEqual(m.xps, 30)

    def test_treasure(self):
        data = {"coin": 100, "xp": 100, "mis": 100}
        t = a_s.Treasure(data)
        self.assertEqual(t.tax, 5)
        self.assertEqual(t.xp, 200)
        self.assertEqual(t.coin, 95)
        self.assertEqual(t.mis, 100)

    def test_shares(self):
        t = a_s.Treasure({"coin": 100, "xp": 100, "mis": 100})
        s = a_s.Shares({"coin": 3, "xp": 2.5})
        s.one_share(t)
        self.assertEqual(s.coin, 31)
        self.assertEqual(s.mis, 33)
        self.assertEqual(s.xp, 80)
