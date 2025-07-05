#!/usr/bin/env python

# name    :  test/test_d6_roller.py
# version :  0.0.1
# date    :  20250705
# author  :  Leam Hall
# desc    :  Tests for the d6_roller.py


import unittest

import d6_roller as d6


class TestParseArgsCLINoDefaults(unittest.TestCase):
    """Test the argument parser with no defaults"""

    def setUp(self):
        self.parser = d6.parse_args(
            [
                "-n 3",
                "-d 2",
                "-t 4",
            ]
        )

    def tearDown(self):
        pass

    def test_num(self):
        self.assertEqual(self.parser.num, 3)

    def test_dice(self):
        self.assertEqual(self.parser.dice, 2)

    def test_target(self):
        self.assertEqual(self.parser.target, 4)


class TestParseArgsCLIDefaults(unittest.TestCase):
    """Test the argument parser with defaults"""

    def setUp(self):
        self.parser = d6.parse_args([])

    def tearDown(self):
        pass

    def test_num(self):
        self.assertEqual(self.parser.num, 1)

    def test_dice(self):
        self.assertEqual(self.parser.dice, 1)

    def test_target(self):
        self.assertEqual(self.parser.target, 5)


class TestParseArgsFile(unittest.TestCase):
    """Test the argument parser's file attribute"""

    def test_file(self):
        parser = d6.parse_args(["-f myfile.csv"])
        self.assertEqual(parser.file, "myfile.csv")


class TestRollDice(unittest.TestCase):
    """Test the roll_dice function"""

    def test_roll_dice_no_defaults(self):
        for _ in range(100):
            successes, rolls = d6.roll_dice(6, 5, 1)
            self.assertIn(successes, range(0, 7))

    def test_roll_dice_dice_default(self):
        for _ in range(100):
            successes, rolls = d6.roll_dice(6, 5)
            self.assertIn(successes, range(0, 7))

    def test_roll_dice_lots_with_dice_default(self):
        for _ in range(100):
            successes, rolls = d6.roll_dice(60, 5)
            self.assertIn(successes, range(0, 61))
