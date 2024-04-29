# test/test_career.py

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
