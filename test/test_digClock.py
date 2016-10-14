import unittest

from mock import patch

import sys
from app.get_time import DigClock
# import app.menu


class TestDigClock(unittest.TestCase):

    def setUp(self):
        self.clock_test = DigClock()

    def test_defaults_are_set_if_c_l_args_have_dash_d(self):
        testargs = ['get_time', '-d']
        with patch.object(sys, 'argv', testargs):
            self.clock_test.read_switches()
            self.clock_test.set_menu_option()
            self.assertEqual(self.clock_test.chosen, self.clock_test.DEFAULTS)

