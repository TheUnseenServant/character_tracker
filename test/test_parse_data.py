#!/usr/bin/env python

# name    :  test/test_parse_data.py
# version :  0.0.1
# date    :  20240619
# author  :  Leam Hall
# desc    :  Tests for parse_data.py


import unittest
import tempfile
import os.path

import parse_data as pd


class TestScrub(unittest.TestCase):

    def test_scrub_line(self):
        line_in_1 = "[b]Drotik[/b] (1s,6p/mo) (Currently Questing)"
        expected_line_1 = "Drotik (1s,6p/mo) (Currently Questing)"
        self.assertEqual(expected_line_1, pd.scrub_line(line_in_1))

        line_in_2 = "[spoiler] [i]Fighter[/i] 3 (HD 4, hp 5, SD 0, sp 0)."
        expected_line_2 = "Fighter 3 (HD 4, hp 5, SD 0, sp 0)"
        self.assertEqual(expected_line_2, pd.scrub_line(line_in_2))


class TestListFromFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.test_dir.name, "raw_data.txt")
        with open(self.data_file, "w") as f:
            f.write("[b]Drotik[/b] (1s,6p/mo) (Currently Questing)\n")
            f.write("\n")
            f.write("[i]Combat[/i]\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_has_right_len(self):
        expected = 2
        result = len(pd.list_from_file(self.data_file))
        self.assertEqual(expected, result)

    def test_has_content(self):
        result = pd.list_from_file(self.data_file)
        self.assertIn("Drotik", result[0])
        self.assertIn("Combat", result[1]) 
