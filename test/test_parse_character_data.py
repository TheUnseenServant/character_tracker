#!/usr/bin/env python

# name    :  test/test_parse_character_data.py
# version :  0.0.1
# date    :  20250603
# author  :  
# desc    :  


import unittest

import parse_character_data as pcd


class TestParseCharacterData(unittest.TestCase):
    

    def test_remove_cost_with_data(self):
        data = "Winifred (12p/mo)"
        expected = "Winifred"
        result = pcd.remove_cost(data)
        self.assertEqual(expected, result)

    def test_remove_cost_no_data(self):
        data = "Winifred"
        expected = "Winifred"
        result = pcd.remove_cost(data)
        self.assertEqual(expected, result)

    def test_remove_cost_different_data(self):
        data = "Winifred ( hd 5, hp 5, sd 3, sp 3)  "
        expected = "Winifred ( hd 5, hp 5, sd 3, sp 3)"
        result = pcd.remove_cost(data)
        self.assertEqual(expected, result)


