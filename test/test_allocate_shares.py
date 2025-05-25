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
            f.write("key;name;shares\n")
            f.write("pc1;PC 1;1\n")
            f.write("pc2;PC 2;1\n")
            f.write("npc1;NPC 1;0.5\n")
            f.write("npc2;NPC 2;0\n")

        self.data = {
            "pc1": [1],
            "pc2": [1],
            "npc1": [0.5],
            "npc2": [0],
        }
        self.party = a_s.something_from_csv(self.data_file, a_s.Member, dict())

    def tearDown(self):
        self.test_dir.cleanup()

    def test_bad_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            a_s.something_from_csv("fred.txt", a_s.Member, dict())
        self.assertRaises(
            FileNotFoundError, a_s.something_from_csv, "fred.txt", a_s.Member
        )

    def test_something_from_csv(self):
        members = a_s.something_from_csv(self.data_file, a_s.Member, dict())
        self.assertEqual(len(members), 4)
        self.assertEqual(members["pc1"].name, "PC 1")

    def test_share_results(self):
        t = a_s.Treasure({"coin": 100, "xp": 100, "mis": 100})
        s = a_s.Shares({"shares": 3})
        s.one_share(t)
        self.assertEqual(s.coin, 33)
        self.assertEqual(s.mis, 33)
        self.assertEqual(s.xp, 66)

    def test_member_basic(self):
        t = a_s.Treasure({"coin": 100, "xp": 50, "mis": 100})
        s = a_s.Shares({"shares": 3})
        s.one_share(t)
        member = {"name": "fred", "shares": 0.5}
        m = a_s.Member(member)
        m.give_shares(s)
        self.assertEqual(m.name, "fred")
        self.assertEqual(m.shares, 0.5)
        self.assertEqual(m.coins, 16)
        self.assertEqual(m.mis, 16)
        self.assertEqual(str(m), "fred gets 25 XP and 32 coin.")

    def test_treasure(self):
        data = {"coin": 100, "xp": 100, "mis": 100, "tax_rate": 5}
        t = a_s.Treasure(data)
        self.assertEqual(t.tax, 5)
        self.assertEqual(t.xp, 200)
        self.assertEqual(t.base_xp, 100)
        self.assertEqual(t.coin, 95)
        self.assertEqual(t.mis, 100)

    def test_treasure_high_tax(self):
        data = {"coin": 100, "xp": 100, "mis": 100, "tax_rate": 50}
        t = a_s.Treasure(data)
        self.assertEqual(t.tax, 50)
        self.assertEqual(t.xp, 200)
        self.assertEqual(t.base_xp, 100)
        self.assertEqual(t.coin, 50)
        self.assertEqual(t.mis, 100)

    def test_treasure_no_tax(self):
        data = {"coin": 100, "xp": 100, "mis": 100}
        t = a_s.Treasure(data)
        self.assertEqual(t.tax, 0)
        self.assertEqual(t.xp, 200)
        self.assertEqual(t.coin, 100)
        self.assertEqual(t.mis, 100)

    def test_shares(self):
        t = a_s.Treasure({"coin": 100, "xp": 100, "mis": 100})
        s = a_s.Shares({"shares": 3})
        s.one_share(t)
        self.assertEqual(s.coin, 33)
        self.assertEqual(s.mis, 33)
        self.assertEqual(s.xp, 66)

    def test_share_header_with_tax(self):
        treasure = a_s.Treasure(
            {"coin": 100, "xp": 100, "mis": 100, "tax_rate": 0.5}
        )
        shares = a_s.Shares({"shares": 3})
        result = a_s.share_header(shares, treasure)
        self.assertIn("Tax", result)
        self.assertIn("tax", result)

    def test_share_header_without_tax(self):
        treasure = a_s.Treasure({"coin": 100, "xp": 100, "mis": 100})
        shares = a_s.Shares({"shares": 3})
        result = a_s.share_header(shares, treasure)
        self.assertNotIn("Tax", result)
        self.assertNotIn("tax", result)
        self.assertIn("base XP", result)
        self.assertIn("base XP +", result)
        self.assertIn("total coin", result)

    def test_keys(self):
        result = a_s.keys(self.party)
        self.assertIn("pc1", result)
        self.assertEqual("PC 1", result["pc1"])
