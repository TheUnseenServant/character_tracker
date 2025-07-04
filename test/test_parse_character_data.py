#!/usr/bin/env python

# name    :  test/test_parse_character_data.py
# version :  0.0.1
# date    :  20250603
# author  :
# desc    :

from copy import deepcopy
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
        self.test_file_names = ["smiles", "lucky", "shorty", "ox"]
        for file in self.test_file_names:
            with open(os.path.join(self.test_dir.name, file), "w") as f:
                f.write("{} (12p/mo) \n".format(file.title()))
                f.write("Neutral Half-Orc Female\n")
                f.write("Rogue 3 (HD 1, HP 1, SD 0, SP 0)\n")
                f.write("Ability Scores: Int +1, Cha -1\n")
                f.write("Combat: +1 Backstab, +1 Morale\n")
                f.write("A&AC: D(D)/D(D)\n")
                f.write("Feats: Prowess, Strider\n")
                f.write("Skills: Burglar, Spy\n")
                f.write("Weapons: Short sword, self bow, several knives\n")
                f.write("Armor: Leather armor, helm, shield\n")
                f.write("Spells: Seduce Venturer, Wiggle Just Right\n")
                f.write("Divine Magic: Honesty\n")
                f.write("Powers: Charm Malte\n")
                f.write("Formulae: Love Potion #9\n")
                f.write("Tricks: Ciphers\n")
                f.write("Secrets: Lots\n")
                f.write(
                    "NPCs: Kat's kids (boys, girls); some lads (men, women)\n"
                )
        character = deepcopy(pcd.character_base)
        character_file = os.path.join(self.test_dir.name, "smiles")
        self.c = pcd.parse_data(character_file, character)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_parse_data_feats(self):
        expected_feats = [
            "Divine Magic(Honesty)",
            "Formula(Love Potion #9)",
            "Power(Charm Malte)",
            "Prowess",
            "Secret(Lots)",
            "Strider",
            "Trickery(Ciphers)",
        ]
        self.assertEqual(self.c["feats"], expected_feats)

    def test_parse_data_name(self):
        self.assertEqual(self.c["name"], "Smiles")

    def test_parse_data_stats(self):
        self.assertEqual(self.c["stats"], ["Cha -1", "Int +1"])

    def test_parse_data_career(self):
        self.assertEqual(self.c["career"], "Rogue")

    def test_parse_data_alignment(self):
        self.assertEqual(self.c["alignment"], "Neutral")

    def test_parse_data_species(self):
        self.assertEqual(self.c["species"], "Half-Orc")

    def test_parse_data_gender(self):
        self.assertEqual(self.c["gender"], "Female")

    def test_parse_data_aac(self):
        self.assertEqual(self.c["aac"], "D(D)/D(D)")

    def test_parse_data_skills(self):
        self.assertEqual(self.c["skills"], ["Burglar", "Spy"])

    def test_parse_data_weapons(self):
        self.assertEqual(
            self.c["weapons"], ["Short sword", "self bow", "several knives"]
        )

    def test_parse_data_armor(self):
        self.assertEqual(self.c["armor"], ["Leather armor", "helm", "shield"])

    def test_parse_data_combat(self):
        self.assertEqual(self.c["combat"], ["+1 Backstab", "+1 Morale"])

    def test_parse_data_spells(self):
        self.assertEqual(
            self.c["spells"], ["Seduce Venturer", "Wiggle Just Right"]
        )

    def test_parse_data_npcs(self):
        self.assertEqual(
            self.c["npcs"],
            ["Kat's kids (boys, girls)", "some lads (men, women)"],
        )

        ###  Keeping these in while awaiting format feedback
        # self.assertEqual(self.c["secrets"], ["Lots"])
        # self.assertEqual(self.c["tricks"], ["Ciphers"])
        # self.assertEqual(self.c["formulae"], ["Love Potion #9"])
        # self.assertEqual(self.c["powers"], ["Charm Malte"])
        # self.assertEqual(self.c["divine_magic"], ["Honest"])


class TestParseCareerLine(unittest.TestCase):
    def test_parse_career_line(self):
        line = "Fighter 3 (HP 4, HD 5, SD 0, SP 0)"
        result = pcd.parse_career_line(line)
        expected = {
            "career": "Fighter",
            "hd": "4",
            "hp": "5",
            "level": "3",
            "sd": "0",
            "sp": "0",
        }
        self.assertEqual(result, expected)


class TestParseBasicLine(unittest.TestCase):
    def test_parse_basic_line(self):
        line = "Neutral Half-orc Female"
        result = pcd.parse_basic_line(line)
        expected = {
            "alignment": "Neutral",
            "species": "Half-Orc",
            "gender": "Female",
        }
        self.assertEqual(expected, result)


class TestRenderTemplate(unittest.TestCase):

    def test_render_template_base(self):
        data = {"name": "Smiles", "career": "Rogue"}
        template = "$name $career"
        expected = "Smiles Rogue"
        result = pcd.render_template(template, data)
        self.assertEqual(expected, result)


class TestLineToList(unittest.TestCase):

    def test_weapons(self):
        line = "Short sword, self bow, several knives\n"
        expected = ["Short sword", "self bow", "several knives"]
        result = pcd.line_to_list(line)
        self.assertEqual(expected, result)

    def test_nested_lists(self):
        line = " Charger with caparison (3HD, 6hp, Decently Armed (shielded), Warhorse Skill+2); Courser (3HD, 4hp, Decently Armed, Hunt-horse Skill+2); 2x Rouncey (2HD, 4hp, Lightly Armed, Warhorse Skill); Sumpter (2HD, Poorly Armed, Packhorse Skill) "  # noqa
        expected = [
            "Charger with caparison (3HD, 6hp, Decently Armed (shielded), Warhorse Skill+2)",  # noqa
            "Courser (3HD, 4hp, Decently Armed, Hunt-horse Skill+2)",
            "2x Rouncey (2HD, 4hp, Lightly Armed, Warhorse Skill)",
            "Sumpter (2HD, Poorly Armed, Packhorse Skill)",
        ]
        result = pcd.line_to_list(line)
        for index, _ in enumerate(result):
            self.assertEqual(expected[index], result[index])
