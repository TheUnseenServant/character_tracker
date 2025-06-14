#!/usr/bin/env python

# name    :  test/test_parse_character_data.py
# version :  0.0.1
# date    :  20250603
# author  :
# desc    :

import os.path
import tempfile
import unittest

import parse_character_data as pcd


class TestRemoveCost(unittest.TestCase):

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


class TestParseData(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file_names = ['smiles', 'lucky', 'shorty', 'ox']
        for file in self.test_file_names:
            with open(os.path.join(self.test_dir.name, file), 'w') as f:
                f.write("{} (12p/mo) \n".format(file.title()))
                f.write("Rogue 3 (HD 1, HP 1, SD 0, SP 0)\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_parse_data(self):
        character = pcd.character_base.copy()
        character_file = os.path.join(self.test_dir.name, "smiles")
        c = pcd.parse_data(character_file, character)
        self.assertEqual(character["name"], "Smiles")

class TestRenderTemplate(unittest.TestCase):

    def test_render_template_base(self):
        data = {"name": "Smiles", "career": "Rogue"}
        template = "$name $career"
        expected = "Smiles Rogue"
        result      = pcd.render_template(template, data)
        self.assertEqual(expected, result)



