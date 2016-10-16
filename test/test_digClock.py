import unittest
import time
import sys
import os

from mock import patch

from app.get_time import DigClock
import app.menu


class TestDigClock(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        f = open(os.devnull, 'w')
        sys.stdout = f
        self.clock_test = DigClock()

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_defaults_are_set_if_c_l_args_have_dash_d(self):
        testargs = ['get_time', '-d']
        with patch.object(sys, 'argv', testargs):
            self.clock_test.read_switches()
            self.clock_test.set_menu_option()
            self.assertEqual(self.clock_test.chosen, self.clock_test.DEFAULTS)

    def test_time_is_set_to_specified_time_if_c_l_args_have_dash_t(self):
        testargs = ['get_time', '-t', '22:27:14']
        with patch.object(sys, 'argv', testargs):
            self.clock_test.read_switches()
            app.menu.raw_input = lambda _: '\n'
            self.clock_test.set_menu_option()
            self.clock_test.set_cur_time()
            self.assertEqual(time.strftime('%H:%M:%S', self.clock_test.cur_time), '22:27:14')
