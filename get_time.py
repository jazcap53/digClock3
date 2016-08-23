from __future__ import print_function
import sys
import os
import time
""" For documentation of PyAudio, see
https://people.csail.mit.edu/hubert/pyaudio/docs/i\
#example-callback-mode-audio-i-o """
import pyaudio
import wave
import nums

LIGHTCYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'

# for more colors see e.g.
# http://www.unknownerror.org/opensource/mrmrs/colors/q/stackoverflow/287871/
#        print-in-terminal-with-colors-using-python


class DigClock(object):
    """ Show a digital clock, in the terminal, that advances once per second.
    Play the Westminster Chimes for each quarter hour """

    # the characters of the clock face
    digits = {'0': nums.zero, '1': nums.one, '2': nums.two, '3': nums.three,
              '4': nums.four, '5': nums.five, '6': nums.six, '7': nums.seven,
              '8': nums.eight, '9': nums.nine, ':': nums.colon, ' ': nums.space}

    def __init__(self):
        self.w_f = None     # w_f: .wav file
        self.stream = None  # stream: to which wave file is output
        self.face = None    # face: clock face
        self.p_aud = None   # p_aud: instance of PyAudio
        self.sys_args = [arg for arg in sys.argv[1:]]
        self.arg_str = None

    def run_clock(self):
        """ Run the clock and chimes """
        try:
            os.system('tput civis')  # make cursor invisible
            print(LIGHTCYAN)
            print(BOLD)
            # PyAudio provides Python bindings for PortAudio audio i/o library
            self.p_aud = pyaudio.PyAudio()
            self.face = ' ' * 3 + time.strftime("%H:%M:%S")
            while True:
                self.print_face()
                chime_file_name = self.check_for_chimes()
                if chime_file_name is not None:
                    self.play_chime(chime_file_name)
                self.await_new_sec()
        finally:
            print(ENDC)
            os.system('tput cnorm')  # restore normal cursor
            self.p_aud.terminate()

    def print_face(self):
        """ Display the face of the clock """
        _ = os.system('clear')
        print('\n' * 7)
        self.face = ' ' * 3 + time.strftime("%H:%M:%S")
        for i in range(9):  # each digit of the clock has nine rows
            for ch in self.face:
                print(self.digits[ch].lines[i], sep='', end='')
            print()
        print()
        print()

    def check_for_chimes(self):
        """ If a chime or bell should begin playing now,
        return the name of its .wav file """
        chime_file_name = None
        if not self.face:
            return None
        # face is 3 spaces plus time as 'hh:mm:ss'
        secs = self.face[9:]
        mins = self.face[6:8]
        hrs = self.face[3:5]
        if mins == '59' and secs == '38':
            # start hourly bells 22 seconds early
            chime_file_name = 'chimes/q4mono.wav'
        elif secs == '00' and mins == '15':
            chime_file_name = 'chimes/q1mono.wav'
        elif secs == '00' and mins == '30':
            chime_file_name = 'chimes/q2mono.wav'
        elif secs == '00' and mins == '45':
            chime_file_name = 'chimes/q3mono.wav'
        elif secs == '00' and mins == '00':
            # convert '00'..'23' hrs to '01'..'12'
            this_hr = self.day_to_half_day(hrs)
            hr_file_name = 'chimes/h' + this_hr + 'mono.wav'
            chime_file_name = hr_file_name
        return chime_file_name

    @staticmethod
    def day_to_half_day(hrs):
        """ Convert '00'..'23' hours to '01'..'12' """
        bells_as_int = 12 if hrs == '00' or hrs == '12' else int(hrs) % 12
        bells_as_str = '{:02d}'.format(bells_as_int)
        return bells_as_str

    def play_chime(self, chime_file_name):
        """ Play a chime or bell """
        self.w_f = wave.open(chime_file_name, 'rb')
        self.stream = self.p_aud.open(
                format=self.p_aud.get_format_from_width(self.w_f.getsampwidth()),
                channels=self.w_f.getnchannels(),
                rate=self.w_f.getframerate(),
                output=True,
                # callback function is called in a separate thread
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
        """ Sleep until the number of seconds on the system clock changes """
        old_face = self.face
        while old_face == self.face:
            time.sleep(.05)
            self.face = ' ' * 3 + time.strftime("%H:%M:%S")

    def callback(self, in_data, frame_count, time_info, status):
        """ Return a chunk of audio data, and whether there is more data """
        data = self.w_f.readframes(frame_count)
        return data, pyaudio.paContinue

if __name__ == '__main__':
    clk = DigClock()
    clk.run_clock()
