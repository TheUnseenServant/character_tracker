#!/usr/bin/env python

# name    :  test/test_parse_args.py
# version :  0.0.1
# date    :  20241123
# author  :  Leam Hall
# desc    :  Test the argument parser in allocate_shares.py


import unittest

import allocate_shares as a_s


class TestParseArgs(unittest.TestCase):
    """Test the argument parser in allocate shares."""

    def test_parse_args_coin(self):
        """Test having coin, and not having coin."""
        parser = a_s.parse_args(["-c 100"])
        self.assertEqual(type(parser.coin), int)
        self.assertEqual(100, parser.coin)

        parser = a_s.parse_args(["--coin", "100"])
        self.assertEqual(100, parser.coin)

        parser = a_s.parse_args([])
        self.assertEqual(0, parser.coin)

    def test_parse_args_mis(self):
        """Test having magic item sales, and not."""
        parser = a_s.parse_args(["-m 100"])
        self.assertEqual(type(parser.mis), int)
        self.assertEqual(100, parser.mis)

        parser = a_s.parse_args(["--mis", "100"])
        self.assertEqual(100, parser.mis)

        parser = a_s.parse_args([])
        self.assertEqual(0, parser.mis)

    def test_parse_args_xp(self):
        """Test having xp, and not."""
        parser = a_s.parse_args(["-x 100"])
        self.assertEqual(type(parser.xp), int)
        self.assertEqual(100, parser.xp)

        parser = a_s.parse_args(["--xp", "100"])
        self.assertEqual(100, parser.xp)

        parser = a_s.parse_args([])
        self.assertEqual(0, parser.xp)

    def test_parse_args_monster_groups(self):
        """Test having a monster_groups file, and not."""
        expected = "data/mymonstergroups.csv"
        default = "data/monster_groups.csv"

        parser = a_s.parse_args(
            ["--monster_groups", "data/mymonstergroups.csv"]
        )
        self.assertEqual(expected, parser.monster_groups)

        parser = a_s.parse_args([])
        self.assertEqual(default, parser.monster_groups)

    def test_parse_args_monster_manual(self):
        """Test having a monster_manual file, and not."""
        expected = "data/mymonstermanual.csv"
        default = "data/monster_manual.csv"

        parser = a_s.parse_args(
            ["--monster_manual", "data/mymonstermanual.csv"]
        )
        self.assertEqual(expected, parser.monster_manual)

        parser = a_s.parse_args([])
        self.assertEqual(default, parser.monster_manual)

    def test_parse_args_monsters(self):
        """Test having monsters, and not."""

        parser = a_s.parse_args(["-M"])
        self.assertTrue(parser.monsters)

        parser = a_s.parse_args([])
        self.assertFalse(parser.monsters)

    def test_parse_args_file(self):
        """Test having a adventure group file, and not."""
        expected = "data/my_advg.csv"
        default = "data/adventure_party.csv"

        parser = a_s.parse_args(["-f", "data/my_advg.csv"])
        self.assertEqual(expected, parser.file)

        parser = a_s.parse_args(["--file", "data/my_advg.csv"])
        self.assertEqual(expected, parser.file)

        parser = a_s.parse_args([])
        self.assertEqual(default, parser.file)

    def test_parse_args_tax_rate(self):
        """Test having a tax_rate, and not."""

        parser = a_s.parse_args(["-t", "0.5"])
        self.assertEqual(parser.tax_rate, 0.5)

        parser = a_s.parse_args(["--tax_rate", "0.5"])
        self.assertEqual(parser.tax_rate, 0.5)

        parser = a_s.parse_args([])
        self.assertFalse(parser.tax_rate)
