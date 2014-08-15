#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
import os #handy system and path functions
from psychopy import visual, core, data, event, logging, gui, sound, info
import psychopy.log #import like this so it doesn't interfere with numpy.log

#setup the Window
win = visual.Window(size=(1366, 768), fullscr=True, screen=0, allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

people = ['af1','af2','af3','af4','am1','am2','am3','am4','cf1']
emotions = ['happy','sad','mad','scared']

for exemplar in people:
    for emotion in emotions:
        for duration in ['6','10','12','20']:
            try: mov = visual.MovieStim(win=win, filename='videos/%s/%s_%s/%s_%s_mov_%s.mov' % (exemplar, exemplar, emotion, exemplar, emotion, duration), pos = [0,80], opacity = 1, name='movie')
            except: print 'could not load', 'videos/%s/%s_%s/%s_%s_mov_%s.mov' % (exemplar, exemplar, emotion, exemplar, emotion, duration)