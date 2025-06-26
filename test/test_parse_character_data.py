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
                f.write("Neutral Half-Orc Female\n")
                f.write("Rogue 3 (HD 1, HP 1, SD 0, SP 0)\n")
                f.write("A&AC: D(D)/D(D)\n")
                f.write("Feats: Prowess, Strider\n")
                f.write("Skills: Spy\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_parse_data(self):
        character = pcd.character_base.copy()
        character_file = os.path.join(self.test_dir.name, "smiles")
        c = pcd.parse_data(character_file, character)
        self.assertEqual(character["name"], "Smiles")
        self.assertEqual(character["career"], "Rogue")
        self.assertEqual(character["alignment"], "Neutral")
        self.assertEqual(character["species"], "Half-Orc")
        self.assertEqual(character["gender"], "Female")
        self.assertEqual(character["aac"], "D(D)/D(D)")
        self.assertEqual(character["feats"], ["Prowess", "Strider"])
        self.assertEqual(character["skills"], ["Spy"])

class TestParseCareerLine(unittest.TestCase):
    def test_parse_career_line(self):
        line    = "Fighter 3 (HP 4, HD 5, SD 0, SP 0)"
        result  = pcd.parse_career_line(line)
        expected    = {
            'career': 'Fighter',
            'hd': '4',
            'hp': '5',
            'level': '3',
            'sd': '0',
            'sp': '0',
        }
        self.assertEqual(result, expected)

class TestParseBasicLine(unittest.TestCase):
    def test_parse_basic_line(self):
        line    = "Neutral Half-orc Female"
        result  = pcd.parse_basic_line(line)
        expected    = {
            'align': 'Neutral',
            'species': 'Half-orc',
            'gender': 'Female',
        }


class TestRenderTemplate(unittest.TestCase):

    def test_render_template_base(self):
        data = {"name": "Smiles", "career": "Rogue"}
        template = "$name $career"
        expected = "Smiles Rogue"
        result      = pcd.render_template(template, data)
        self.assertEqual(expected, result)



