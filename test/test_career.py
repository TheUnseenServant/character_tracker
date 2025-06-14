# test/test_career.py

import unittest

import careers as wc


class TestCareer(unittest.TestCase):
    def setUp(self):
        self.fighter_info = {
            "career": "fighter",
            "hd": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;",
            "sd": "",
            "sp": "",
        }
        self.f = wc.Career(self.fighter_info)

        self.rogue_info = {
            "career": "rogue",
            "hd": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;",
            "sd": "",
            "sp": "",
        }
        self.r = wc.Career(self.rogue_info)

        self.cleric_info = {
            "career": "cleric",
            "hd": "1,1,2,3,3,4,5,5,6,7,7,8,9,9,10",
            "sd": "0,1,1,1,2,2,2,3,3,3,4,4,4,5,5",
            "sp": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14",
        }
        self.c = wc.Career(self.cleric_info)

        self.mage_info = {
            "career": "mage",
            "hd": "1,1,2,2,3,3,4,4,5,5,6,6,7,7,8",
            "sd": "0,1,1,2,2,3,3,4,4,5,5,6,6,7,7",
            "sp": "0,2,3,5,6,8,9,11,12,14,15,17,18,20,21",
        }
        self.m = wc.Career(self.mage_info)

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

    def test_get_info_fighter(self):
        xp = 7999
        expected = {"level": 3, "hd": 4, "sd": 0, "sp": 0}
        result = self.f.get_info(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 5, "sd": 0, "sp": 0}
        result = self.f.get_info(xp)
        self.assertEqual(expected, result)

    def test_get_info_rogue(self):
        xp = 7999
        expected = {"level": 3, "hd": 4, "sd": 0, "sp": 0}
        result = self.r.get_info(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 5, "sd": 0, "sp": 0}
        result = self.f.get_info(xp)
        self.assertEqual(expected, result)

    def test_get_info_cleric(self):
        xp = 7999
        expected = {"level": 3, "hd": 3, "sd": 1, "sp": 3}
        result = self.c.get_info(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 3, "sd": 2, "sp": 4}
        result = self.c.get_info(xp)
        self.assertEqual(expected, result)

    def test_get_info_mage(self):
        xp = 7999
        expected = {"level": 3, "hd": 2, "sd": 2, "sp": 5}
        result = self.m.get_info(xp)
        self.assertEqual(expected, result)

        xp = 8000
        expected = {"level": 4, "hd": 3, "sd": 2, "sp": 6}
        result = self.m.get_info(xp)
        self.assertEqual(expected, result)

    def test_career_info(self):
        ci = wc.CareerInfo(wc.career_data)

        f4_expected = {"level": 4, "hd": 5, "sd": 0, "sp": 0}
        f4_result = ci.get_info("fighter", 8000)
        self.assertEqual(f4_expected, f4_result)

        r4_expected = {"level": 4, "hd": 5, "sd": 0, "sp": 0}
        r4_result = ci.get_info("rogue", 8000)
        self.assertEqual(r4_expected, r4_result)

        c4_expected = {"level": 4, "hd": 3, "sd": 2, "sp": 4}
        c4_result = ci.get_info("cleric", 8000)
        self.assertEqual(c4_expected, c4_result)

        m4_expected = {"level": 4, "hd": 3, "sd": 2, "sp": 6}
        m4_result = ci.get_info("mage", 8000)
        self.assertEqual(m4_expected, m4_result)

        sm3_expected = {"level": 3, "hd": 4, "sd": 2, "sp": 5}
        sm3_result = ci.get_info("swordmage", 8000)
        self.assertEqual(sm3_expected, sm3_result)

        st3_expected = {"level": 3, "hd": 3, "sd": 2, "sp": 5}
        st3_result = ci.get_info("spellthief", 8000)
        self.assertEqual(st3_expected, st3_result)
