"""
This is the top-level file for DigClock2.

For documentation of wave, see
https://docs.python.org/2/library/wave.html

For documentation of PyAudio, see
https://people.csail.mit.edu/hubert/pyaudio/docs/i\
#example-callback-mode-audio-i-o
"""
from __future__ import print_function
import os
import time
import argparse

import pyaudio
import wave

import nums
import menu


ENDC = '\033[0m'
BOLD = '\033[01m'


class DigClock(object):
    """
    Class provided:
        Show a digital clock, in the terminal, that advances once per second.
        Play the Westminster Chimes for each quarter hour if selected.
        Text color, background color, 12- or 24-hour format, and chime or silent
            modes are chosen by user from menus.
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
        self.w_f = None         # .wav file
        self.stream = None      # stream to which wave file is output
        self.face = None        # clock face
        self.p_aud = None       # instance of PyAudio
        self.chosen = None      # holds menu choices
        self.cur_time = None    # holds current unformatted time
        self.arg_parser = None  # holds argument parser object
        self.args = None        # c. l. arguments

    def run_clock(self):
        """
        Run the clock and chimes
        Called by: client code
        """
        try:
            os.system('tput civis')   # make cursor invisible
            print(BOLD)
            print(self.chosen[0][3])  # set text color
            print(self.chosen[1][3])  # set background color
            # PyAudio provides Python bindings for PortAudio audio i/o library
            self.p_aud = pyaudio.PyAudio()
            while True:
                self.cur_time = time.localtime()
                self.get_face()
                self.print_face()
                chime_file_name = self.check_for_chimes()
                if chime_file_name is not None:  # we should play a chime now
                    self.play_chime(chime_file_name)
                self.await_new_sec()
        finally:
            print(ENDC)
            os.system('tput cnorm')  # restore normal cursor
            self.p_aud.terminate()
            os.system('clear')

    def read_switches(self):
        """
        Handle command-line switches
        Called by: self.run_clock()
        """
        self.arg_parser = argparse.ArgumentParser(description='Run a digital clock in the terminal.')
        self.arg_parser.add_argument('-d',
                                     help='skip the menus: accept all\
                                     default arguments',
                                     action='store_true')
        self.args = self.arg_parser.parse_args()

    def set_up_c_l_args(self):
        self.read_switches()
        if self.args.d:
            self.chosen = self.DEFAULTS
        else:
            self.chosen = menu.cycle_menus()

    def get_face(self):
        """
        Get a formatted time string
        Called by: self.run_clock()
        """
        self.face = ' ' * 3
        time_str = "%I:%M:%S" if (self.chosen[2][2] == '12-HOUR') else "%H:%M:%S"
        self.face += time.strftime(time_str)   # self.cur_time.strftime(time_str)

    def print_face(self):
        """
        Display the face of the clock
        Called by: self.run_clock()
        """
        _ = os.system('clear')
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

    def check_for_chimes(self):
        """
        If a chime or bell should begin playing now,
        return the name of its .wav file
        Called by: self.run_clock()
        """
        if self.chosen[3][2] == 'SILENT':  # if chimes are off
            return None
        chime_file_name = None
        if not self.face:
            return None
        # face is 3 spaces plus time as hh:mm:ss
        secs = self.face[9:]
        mins = self.face[6:8]
        hrs = self.face[3:5]
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
        Chime pattern is the same for 12-Hour and 24-hour display
        Called by: self.check_for_chimes()
        """
        if self.chosen[2][2] == '12-HOUR':  # output already in 12-HOUR format
            return h_str
        else:
            # Convert '00'..'23' hours to '01'..'12'
            hrs_as_int = 12 if h_str == '00' or h_str == '12' else int(h_str) % 12
            hrs_as_str = '{:02d}'.format(hrs_as_int)
            return hrs_as_str

    def play_chime(self, chime_file_name):
        """
        Play a chime or hourly bell
        Called by: self.run_clock()
        """
        self.w_f = wave.open(chime_file_name, 'rb')
        self.stream = self.p_aud.open(
                # PyAudio parameters
                format=self.p_aud.get_format_from_width(self.w_f.getsampwidth()),
                channels=self.w_f.getnchannels(),
                rate=self.w_f.getframerate(),
                output=True,
                # callback function is executed in a separate thread
                stream_callback=self.callback)
        self.stream.start_stream()
        self.print_face()
        while True:
            if not self.stream.is_active():
                break
            self.await_new_sec()
            self.print_face()
        self.stream.stop_stream()
        self.stream.close()
        self.w_f.close()

    def await_new_sec(self):
        """
        Sleep until the number of seconds on the system clock changes
        Called by: self.play_chime()
        """
        old_face = self.face
        while old_face == self.face:
            time.sleep(.01)
            self.get_face()

    def callback(self, in_data, frame_count, time_info, status):
        """
        Return a chunk of audio data, and whether there is more data
        Called by: PyAudio instance
        """
        data = self.w_f.readframes(frame_count)
        return data, pyaudio.paContinue


if __name__ == '__main__':
    clk = DigClock()
    clk.set_up_c_l_args()
    clk.run_clock()
