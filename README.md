# Dig, Clock!

## Summary

Dig, Clock! is a menu-driven digital clock, written in Python 2.7, that runs in a Linux terminal. This version can be set to play the Westminster Chimes on every quarter hour.

A suite of unit tests is included.

## Features

* Simple menus allow you to choose text color, background color, 12-hour or 24-hour display, and silent or chime mode
* Select all default choices and skip the menus by running with the **-d** switch
* Utf-8 encoded box-drawing characters make large, clear, gap-less digits
* Timekeeping as accurate as your system clock
* Test Mode (**-t** switch) lets you start the clock from a specified time, with or without the **-d** switch

## Dependencies
Python 2.7 -- available via your package manager  
PortAudio v19 -- available via your package manager  
PyAudio -- available at https://pypi.python.org/pypi/PyAudio  
PySynth -- available as PySynth-1.1.tar.gz from http://mdoege.github.io/PySynth  

## Install and run
Download ```digClock2.tar.gz```.  
Run ```$ tar xvfz ./digClock2.tar.gz```.  
Run ```$ python dig_clock_2.py```.  

## License
CC0, Creative Commons Zero, released into the public domain
