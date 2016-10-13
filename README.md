# Dig, Clock!

## Summary

This is a (fully functional) work in progress. It is being refactored for testability.

Dig, Clock! is a menu-driven digital clock, written in Python 2.7, that runs in a Linux terminal. This version can play the Westminster Chimes on every quarter hour.

## Features

* Simple menus allow you to choose text color, background color, 12-hour or 24-hour display, and silent or chime mode
* Select all default choices and skip the menus by running with the **-d** switch
* Utf-8 encoded box-drawing characters make large, clear, gap-less digits
* Timekeeping as accurate as your system clock
* _(New!)_ Test Mode (**-t** switch) lets you start the clock from a specified time, with or without the **-d** switch

## Dependencies
Python 2.7 -- available via your package manager  
PortAudio v19 -- available via your package manager  
PyAudio -- available at https://pypi.python.org/pypi/PyAudio  
PySynth -- available as PySynth-1.1.tar.gz from http://mdoege.github.io/PySynth  

## Install and run
Download ```digClock2.tar.gz```.  
Run ```$ tar xvfz ./digClock2.tar.gz```.  
Run ```$ python get_time.py```.  

## Problems? Contact the doctor!
Take Dig, Clock! and call me at two in the morning.

## License
CC0, Creative Commons Zero, released into the public domain
