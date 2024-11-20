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


class TestMonster(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.mm_file = os.path.join(self.test_dir.name, "monster_manual.csv")
        with open(self.mm_file, "w") as f:
            f.write("key;name;base_xp;hp_xp\n")
            f.write("wight;Wight;540;10\n")
            f.write("wight8;8HD Wight;1180;20\n")
            f.write("skeleton;Skeleton;14;5\n")

        self.group_file = os.path.join(
            self.test_dir.name, "monster_groups.csv"
        )
        with open(self.group_file, "w") as g:
            g.write("key;hp;count\n")
            g.write("wight;7;8\n")
            g.write("wight8;11;3\n")
            g.write("wight8;8;1\n")
            g.write("skeleton;2;75\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_base_monster(self):
        data = {
            "key": "skeleton",
            "name": "Skeleton",
            "base_xp": 14,
            "hp_xp": 5,
        }
        result = a_s.Monster(data)
        expected_string = "Skeleton (skeleton) Base 14 + 5 per HP"
        self.assertEqual(result.key, "skeleton")
        self.assertEqual(result.name, "Skeleton")
        self.assertEqual(result.base_xp, 14)
        self.assertEqual(result.hp_xp, 5)
        self.assertEqual(str(result), expected_string)

    def test_something_from_csv(self):
        monsters = a_s.something_from_csv(self.mm_file, a_s.Monster, dict())
        self.assertEqual(type(monsters), dict)
        self.assertEqual(monsters["wight8"].name, "8HD Wight")

    def test_xp_for_monsters(self):
        monsters = a_s.something_from_csv(self.mm_file, a_s.Monster, dict())
        data = a_s.Group({"key": "wight", "hp": 4, "count": 8})
        expected = 4640
        result = a_s.xp_for_monsters(data, monsters)
        self.assertEqual(expected, result)

    def test_xp_for_monsters_keyerror(self):
        monsters = a_s.something_from_csv(self.mm_file, a_s.Monster, dict())
        data = a_s.Group({"key": "zight", "hp": 4, "count": 8})
        expected = 0
        result = a_s.xp_for_monsters(data, monsters)
        self.assertEqual(expected, result)

    def test_monster_group(self):
        monster_groups = a_s.something_from_csv(
            self.group_file, a_s.Group, list()
        )
        self.assertEqual(type(monster_groups), list)
        self.assertIn(monster_groups[0].key, ["wight", "wight8", "skeleton"])

    def test_get_total_xp(self):
        monsters = a_s.something_from_csv(self.mm_file, a_s.Monster, dict())
        monster_groups = a_s.something_from_csv(
            self.group_file, a_s.Group, list()
        )
        expected = 12220
        result = a_s.get_total_xp(monster_groups, monsters)
        self.assertEqual(expected, result)
