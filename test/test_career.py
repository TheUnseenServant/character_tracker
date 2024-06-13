# test/test_career.py

import os.path
import tempfile
import unittest

import write_char as wc


class TestCareer(unittest.TestCase):
    def setUp(self):
        self.fighter_info = {
            "career": "fighter",
            "hd": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;",
            "sd": "",
        }
        self.f = wc.Career(self.fighter_info)

        self.cleric_info = {
            "career": "cleric",
            "hd": "1,1,2,3,3,4,5,5,6,7,7,8,9,9,10",
            "sd": "0,1,1,1,2,2,2,3,3,3,4,4,4,5,5",
        }
        self.c = wc.Career(self.cleric_info)

        self.mage_info = {
            "career": "mage",
            "hd": "1,1,2,2,3,3,4,4,5,5,6,6,7,7,8",
            "sd": "0,1,1,2,2,3,3,4,4,5,5,6,6,7,7",
        }
        self.m = wc.Career(self.mage_info)

        self.test_dir = tempfile.TemporaryDirectory()
        self.level_data_file = os.path.join(self.test_dir.name, "levels.csv")
        with open(self.level_data_file, "w") as f:
            f.write("career;hd;sd\n")
            f.write("fighter;1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;\n")
            f.write(
                "mage;1,1,2,2,3,3,4,4,5,5,6,6,7,7,8;0,1,1,2,2,3,3,4,4,5,5,6,6,7,7\n"
            )
            f.write(
                "cleric;1,1,2,3,3,4,5,5,6,7,7,8,9,9,10;0,1,1,1,2,2,2,3,3,3,4,4,4,5,5\n"
            )

    def tearDown(self):
        self.test_dir.cleanup()

    def test_career_get_level(self):
        self.assertEqual(self.f.get_level(7999), 3)
        self.assertEqual(self.f.get_level(8000), 4)

    def test_career_get_hd_sd(self):
        self.assertEqual(self.c.get_hd(3), 3)
        self.assertEqual(self.c.get_sd(3), 1)
        self.assertEqual(self.c.get_hd(5), 4)
        self.assertEqual(self.c.get_sd(5), 2)

        self.assertEqual(self.f.get_hd(4), 5)
        self.assertEqual(self.f.get_sd(4), 0)

    def test_get_level_hd_sd_fighter(self):
        xp = 7999
        expected = {"level": 3, "hd": 4, "sd": 0}
        result = self.f.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 5, "sd": 0}
        result = self.f.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

    def test_get_level_hd_sd_cleric(self):
        xp = 7999
        expected = {"level": 3, "hd": 3, "sd": 1}
        result = self.c.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 3, "sd": 2}
        result = self.c.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

    def test_get_level_hd_sd_mage(self):
        xp = 7999
        expected = {"level": 3, "hd": 2, "sd": 2}
        result = self.m.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 3, "sd": 2}
        result = self.m.get_level_hd_sd(xp)
        self.assertEqual(expected, result)

    def test_career_info_builder(self):
        ci_builder = wc.CareerInfoBuilder(self.level_data_file)
        ci = ci_builder.build()

        f4_expected = {"level": 4, "hd": 5, "sd": 0}
        f4_result = ci.get_info("fighter", 8000)
        self.assertEqual(f4_expected, f4_result)

        c4_expected = {"level": 4, "hd": 3, "sd": 2}
        c4_result = ci.get_info("cleric", 8000)
        self.assertEqual(c4_expected, c4_result)

        m4_expected = {"level": 4, "hd": 3, "sd": 2}
        m4_result = ci.get_info("mage", 8000)
        self.assertEqual(m4_expected, m4_result)
