import unittest

from mock import patch

import sys
from app.get_time import DigClock
# import app.menu


class TestDigClock(unittest.TestCase):

    def setUp(self):
        self.clk_test = DigClock()

    def test_defaults_are_set_if_c_l_args_have_dash_d(self):
        testargs = ['get_time', '-d']
        with patch.object(sys, 'argv', testargs):
            self.clk_test.set_up_c_l_args()
            self.assertEqual(self.clk_test.chosen, self.clk_test.DEFAULTS)

