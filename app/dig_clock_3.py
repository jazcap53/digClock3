"""
This is the top-level file for DigClock3.

For documentation of wave, see
https://docs.python.org/2/library/wave.html

For documentation of PyAudio, see
https://people.csail.mit.edu/hubert/pyaudio/docs/i\
#example-callback-mode-audio-i-o
"""
import os
import time
import argparse
import threading

from playsound import playsound, PlaysoundException
import pyaudio
import wave

import nums
from menu import CycleMenus
from args_actions import ParseTime


ENDC = '\033[0m'
BOLD = '\033[01m'


class DigClock(object):
    """
    Class provided:
        Shows a digital clock, in the terminal, that advances once per second.
        Plays the Westminster Chimes for each quarter hour if selected.
        Text color, background color, 12- or 24-hour format, and chime or silent
            modes may be chosen by the user from menus.
        Default mode (skip the menus) and Test mode (start from a specified time)
            may be enabled with command-line switches -d and -t, respectively
    """
    # the characters of the clock face
    digits = {'0': nums.Zero, '1': nums.One, '2': nums.Two, '3': nums.Three,
              '4': nums.Four, '5': nums.Five, '6': nums.Six, '7': nums.Seven,
              '8': nums.Eight, '9': nums.Nine, ':': nums.Colon, ' ': nums.Space}

    DEFAULTS = [['text color', ' 7', 'LIGHTCYAN', '\x1b[96m'],
                ['background color', ' 1', 'BLACK', '\x1b[40m'],
                ['display mode', ' 2', '12-HOUR'],
                ['chime mode', ' 1', 'CHIME']]  # default menu choices

    def __init__(self):
        self.face = None  # clock face
        self.chosen = None  # menu choices
        self.cur_time = None  # current time as time.struct_tm
        self.arg_parser = None  # argument parser object
        self.args = None  # c. l. arguments
        self.secs_since_start = 0

    def run_clock(self):
        """
        Run the clock and chimes
        :return: None
        Called by: client code
        """
        self.read_switches()
        self.set_menu_option()
        try:
            os.system('tput civis')   # make cursor invisible
            print(BOLD)
            print(self.chosen[0][3])  # set text color
            print(self.chosen[1][3])  # set background color
            while True:
                self.set_cur_time()
                self.get_cur_time_str()
                self.print_face()
                if not self.args.a:  # skip chime check in alarm mode
                    chime_file_name = self.check_for_chimes()
                    if chime_file_name is not None:  # we should play a chime now
                        self.play_chime(chime_file_name)
                if self.check_for_alarm():
                    self.play_chime('app/chimes/alarm.wav')
                    while True:
                        pass  # wait for termination signal
                self.await_new_sec()
        finally:
            print(ENDC)
            os.system('tput cnorm')  # restore normal cursor
            print("\033[H\033[J", end="")

    def read_switches(self):
        """
        Handle command-line switches
        :return: None
        Called by: self.set_up_c_l_args()
        """
        self.arg_parser = argparse.ArgumentParser(description='Run a digital clock in the terminal.')
        self.arg_parser.add_argument('-d',
                                     help='skip the menus: accept all'
                                     ' default arguments',
                                     action='store_true')
        self.arg_parser.add_argument('-t', metavar='timestring', type=str,
                                     help='test mode: start clock from given time'
                                          ' (in 24-hour HH:MM:SS format)',
                                          action=ParseTime)
        self.arg_parser.add_argument('-a', metavar='alarmstring', type=str,
                                     help='alarm mode: start clock from given time'
                                          ' (in 24-hour HH:MM:SS format) and play alarm at 00:00:00',
                                     action=ParseTime)
        self.args = self.arg_parser.parse_args()

    def set_cur_time(self):
        if self.args.a:
            if self.face and self.face.lstrip() == '00:00:00':
                return
            self.cur_time = time.localtime(self.args.a - self.secs_since_start)
        elif self.args.t:
            self.cur_time = time.localtime(self.args.t + self.secs_since_start)
        else:
            self.cur_time = time.localtime()

    def set_menu_option(self):
        if self.args.d or self.args.a:
            self.chosen = self.DEFAULTS
            if self.args.a:
                self.chosen[2][2] = '24-HOUR'  # overwrite display mode to 24-HOUR in alarm mode
                self.chosen[3][2] = 'SILENT'  # overwrite chime mode to SILENT in alarm mode
        else:
            # present the menus and get the choices
            self.chosen = CycleMenus().cycle()

    def get_cur_time_str(self):
        """
        Get a formatted time string with current time
        :return: None
        Called by: self.run_clock(), self.play_chime()
        """
        self.face = ' ' * 3
        time_str = "%I:%M:%S" if (self.chosen[2][2] == '12-HOUR') else "%H:%M:%S"
        self.face += time.strftime(time_str, self.cur_time)

    def print_face(self):
        """
        Display the face of the clock
        :return: None
        Called by: self.run_clock()
        """
        print("\033[H\033[J", end="")
        self.print_digits()
        if self.chosen[2][2] == '12-HOUR':
            self.print_am_pm()

    def print_digits(self):
        """
        Display the digits showing the time
        :return: None
        Called by: self.print_face()
        """
        print('\n' * 7)
        for i in range(9):  # each digit of the clock has nine rows
            for ch in self.face:
                print(self.digits[ch].lines[i], sep='', end='')
            print()
        print()
        print()

    def print_am_pm(self):
        """
        In 12-HOUR mode, print AM or PM
        :return: None
        Called by: self.print_face()
        """
        if time.strftime('%p', self.cur_time)[0] == 'A':
            print(' ' * 83 + nums.dblConcDn + ' ' + nums.dblTeeDn)
            print(' ' * 83 + nums.dblHoriz + ' ' + nums.dbl3Vert)
            print(' ' * 83 + nums.dbl2Vert + ' ' + nums.dbl2Vert)
        else:
            print(' ' * 83 + nums.dblConcDn + ' ' + nums.dblTeeDn)
            print(' ' * 83 + nums.dblHorizRUp + ' ' + nums.dbl3Vert)
            print(' ' * 83 + nums.dblLVert + ' ' + nums.dbl3Vert)

    def check_for_alarm(self):
        if self.args.a and self.face.lstrip() == '00:00:00':
            return True
        return False

    def check_for_chimes(self):
        """
        Check whether a sound should begin playing now
        :return: if a sound should begin now:
                     the name of its .wav file
                 else:
                     None
        Called by: self.run_clock()
        """
        if self.chosen[3][2] == 'SILENT' or self.args.a:  # if chimes are off or in alarm mode
            return None
        chime_file_name = None
        hrs, mins, secs = self.face.lstrip().split(':')
        if mins == '59' and secs == '38':
            # start hourly bells 22 seconds early
            chime_file_name = 'app/chimes/q4mono.wav'
        elif secs == '00' and mins == '15':
            chime_file_name = 'app/chimes/q1mono.wav'
        elif secs == '00' and mins == '30':
            chime_file_name = 'app/chimes/q2mono.wav'
        elif secs == '00' and mins == '45':
            chime_file_name = 'app/chimes/q3mono.wav'
        elif secs == '00' and mins == '00':
            hrs = self.get_hrs(hrs)
            hr_file_name = 'app/chimes/h' + hrs + 'mono.wav'
            chime_file_name = hr_file_name
        return chime_file_name

    def get_hrs(self, h_str):
        """
        Make chime pattern the same for 12-Hour and 24-hour display
        :param h_str: the hour as a string in 12- or 24- hour format
        :return: the hour as a string in 12-hour format
        Called by: self.check_for_chimes()
        """
        if self.chosen[2][2] == '12-HOUR':  # output already in 12-HOUR format
            return h_str
        else:
            hrs_as_int = 12 if h_str == '00' or h_str == '12' else\
                               int(h_str) % 12
            hrs_as_str = '{:02d}'.format(hrs_as_int)
            return hrs_as_str

    def play_chime(self, chime_file_name):
        """
        Play an audio file
        :param chime_file_name: the name of a .wav file to play
        :return: None
        Called by: self.run_clock()
        """
        sound_thread = threading.Thread(target=playsound, args=(chime_file_name,))
        sound_thread.start()

        self.print_face()
        while sound_thread.is_alive():
            try:
                self.await_new_sec()
                self.set_cur_time()
                self.get_cur_time_str()
                self.print_face()
            except PlaysoundException:
                # Handle any exceptions raised by playsound
                break

    def await_new_sec(self):
        """
        Sleep until the number of seconds on the system clock changes
        :return: None
        Called by: self.run_clock(), self.play_chime()
        """
        old_secs = time.strftime('%S')
        while time.strftime('%S') == old_secs:
            time.sleep(.01)
        self.secs_since_start += 1

    def callback(self, in_data, frame_count, time_info, status):
        """
        Return a chunk of audio data, and whether there is more data
        Called by: PyAudio instance
        """
        data = self.w_f.readframes(frame_count)
        return data, pyaudio.paContinue


if __name__ == '__main__':
    clk = DigClock()
    clk.run_clock()
