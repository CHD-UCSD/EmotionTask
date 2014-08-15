#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
import os #handy system and path functions
from psychopy import visual, core, data, event, logging, gui, sound, info
import psychopy.log #import like this so it doesn't interfere with numpy.log
import pyxid, xlwt
from feedback import feedback

#print pyglet

touchscreen=True
trial_conditions = 'conditions/trial_final_new.csv'

plaintext_01=u'In this game, you will try to figure out how people are feeling as quickly as you can. Let\'s practice a few things before we begin. \n\nFirst, you will see a row of buttons like the ones below, with faces and feeling words on them that represent the feelings “happy”, “sad”, “mad”, and “scared”. Next, you will hear a voice that tells you which of these buttons to touch. \n\n\n\n\n\n\n\n                     Touch the “Next” button to try a few.'
plaintext_replay_01=u'Let\'s do that again. Touch the button that goes with each feeling.\n\n\n\n\n\n\n         Touch the "Next" button to continue.'
plaintext_02=u'Good. This time, you will see videos of people\'s faces. At the beginning of each video, you won\'t be able to tell how that person is feeling. As it continues, he or she will begin to look either happy, sad, mad, or scared. When each video is finished, see if you can figure out how that person is feeling. \n\n\n\n\n                             Touch the "Next" button  to try a few.'
plaintext_replay_02=u'Let\'s do that again. Tell me how each person is feeling.\n\n\n\n\n\n\n         Touch the "Next" button to continue.'
plaintext_03=u'Good. This time, you try controlling the video. Again, you won\'t be able to tell how the person is feeling at first. Before the start of each video, the border around the face will be red. Hold down the button on the button-box to start the video, and the border will turn green. Try to decide how each person is feeling as quickly as you can without making mistakes. As soon as you think you know how the person is feeling, lift your finger off the button. Once you lift your finger, the four buttons for happy, sad, mad, and scared will appear. Then touch the button that matches how the person is feeling. Remember to hold down the button on the button-box until you think you know how the person is feeling. \n\n                               Touch the "Next" button to try a few.'
plaintext_replay_03=u'Let''s do that again. Try to decide how each person is feeling as quickly as you can without making mistakes. Hold down the button on the button-box until you think you know how the person is feeling, and then touch the button that matches that feeling.\n\n\n\n\n         Touch the "Next" button to continue.'
plaintext_trial=u'Ok, we\'re ready to begin. Just like before, try to decide how each person is feeling as quickly as you can without making mistakes. Hold down the button on the button-box for each video until you know how the person is feeling. As soon as you think you know how the person is feeling, lift your finger off the button. Once the buttons for happy, sad, mad, and scared appear, choose the button that matches how the person is feeling. \n\n\n\n                                Touch the "Next" button to begin.'
plaintext_rank=u'For this last part, you will see different faces of the same emotion. Please rank each of them according to the intensity of the emotion displayed by touching the number on the line. For example, for happy, the least happy face would be ranked 1, and the happiest face would be ranked 4. You may not give two faces the same rank. Once you have assigned each face a ranking, you must touch each button below the scale to confirm your rankings. Once you confirm your rankings, you will automatically advance to the next emotion. \n\n\n\n                            Touch the "Next" button to continue.'

#store info about the experiment session
expName='None'#from the Builder filename that created this script
expInfo={'participant':'', 'session':'001'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
psychopy.log.console.setLevel(psychopy.log.WARNING)#this outputs to the screen, not a file
logFile=psychopy.log.LogFile(filename+'.log', level=psychopy.log.EXP)

# get a list of all attached XID devices
for i in range(5):
    devices = pyxid.get_xid_devices()
    if len(devices)>0: break
print devices
dev = devices[0] # get the first device to use
if dev.is_response_device():
    dev.reset_base_timer()
    dev.reset_rt_timer()
#set key_num as the inded key for responses
key_num = 3

def wait_for_response(dev, key_num, action):
    if action=='press': action=True
    elif action=='release': action=False
    
    dev.clear_response_queue()
    print 'response_queue:', dev.response_queue
    while True:
        dev.poll_for_response()
        if dev.response_queue_size()>0:
            response.get_next_response()
            if response['key'] == key_num and response['pressed']==action: break
#    if dev.response_queue_size() > 0:
#        response = dev.get_next_response()
#        if response['key'] == key_num: return response['pressed']
#        else: return None
#    else: return None

#method to get clicks
def click():
    if touchscreen and mouse.mouseMoved(): return True
    elif not touchscreen and mouse.getPressed()==[1,0,0]: return True
    else: return False

#setup the Window
win = visual.Window(size=(1366, 768), fullscr=True, screen=0, allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#all texts
text_intro=visual.TextStim(win=win, ori=0, name='text_intro',text=u'Hello! Touch anywhere on the screen to begin.',font=u'Arial',pos=[0, 0], height=0.09,wrapWidth=1.2,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_01=visual.TextStim(win=win, ori=0, name='text_01',text=plaintext_01,font=u'Arial',pos=[0, 0.1], height=0.07,wrapWidth=1.3,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_replay_01=visual.TextStim(win=win, ori=0, name='text_replay_01',text=plaintext_replay_01,font=u'Arial',pos=[0, -0.1], height=0.07,wrapWidth=None,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_02=visual.TextStim(win=win, ori=0, name='text_02',text=plaintext_02,font=u'Arial',pos=[0, -0.1], height=0.065,wrapWidth=1.3,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_replay_02=visual.TextStim(win=win, ori=0, name='text_replay_02',text=plaintext_replay_02,font=u'Arial',pos=[0, -0.1], height=0.07,wrapWidth=None,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_03=visual.TextStim(win=win, ori=0, name='text_03',text=plaintext_03,font=u'Arial',pos=[0, 0.05], height=0.065,wrapWidth=1.3,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_replay_03=visual.TextStim(win=win, ori=0, name='text_replay_03',text=plaintext_replay_03,font=u'Arial',pos=[0, -0.1], height=0.07,wrapWidth=None,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
text_trial=visual.TextStim(win=win, ori=0, name='text_trial',text=plaintext_trial,font=u'Arial',pos=[0, 0], height=0.065,wrapWidth=1.3,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)
instr = visual.TextStim(win, text=plaintext_rank, height=0.065, wrapWidth=1.3)
text_outro=visual.TextStim(win=win, ori=0, name='text_outro',text=u"We\'re finished. Thank you for your participation!",font=u'Arial',pos=[0, 0], height=0.09,wrapWidth=1.2,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0)

#Initialise all audio
file_root_audio=u'audio/New Instructions 20130508/Loud Versions/'
audio_instructions_01=sound.Sound(file_root_audio+u'audio_practice_01.wav',secs=30)
audio_instructions_01.setVolume(1)
audio_replay_01=sound.Sound(file_root_audio+u'audio_replay_01.wav',secs=20)
audio_replay_01.setVolume(1)
audio_instructions_02=sound.Sound(file_root_audio+u'audio_practice_02.wav',secs=30)
audio_instructions_02.setVolume(1)
audio_replay_02=sound.Sound(file_root_audio+u'audio_replay_02.wav',secs=20)
audio_replay_02.setVolume(1)
audio_instructions_03=sound.Sound(file_root_audio+u'audio_practice_03.wav',secs=30)
audio_instructions_03.setVolume(1)
audio_replay_03=sound.Sound(file_root_audio+u'audio_replay_03.wav',secs=20)
audio_replay_03.setVolume(1)
audio_instructions_trial=sound.Sound(file_root_audio+u'audio_trial.wav',secs=60)
audio_instructions_trial.setVolume(1)
audio_endchoice=sound.Sound(file_root_audio+u'audio_rank.wav',secs=60)
audio_endchoice.setVolume(1)

#Initialise mouse, images, and buttons
mouse=event.Mouse(win=win)
x,y=[None,None]
mouse.getPos()
next_button=visual.ImageStim(win=win, name='next_button',image=u'buttons/next_button.png', mask=u'None',ori=0, pos=[0, -0.65], size=[0.3, 0.2],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
play_button_up=visual.ImageStim(win=win, name='play_button_up', image=u'buttons/play_button_up.png', mask=None,ori=0, pos=[0, -0.5], size=[0.2, 0.3],color=[1,1,1], colorSpace=u'rgb', opacity=1)
play_button_down=visual.ImageStim(win=win, name='play_button_down', image=u'buttons/play_button_down.png', mask=None,ori=0, pos=[0, -0.5], size=[0.2, 0.3],color=[1,1,1], colorSpace=u'rgb', opacity=1)
rect_frame = visual.Rect(win=win, name='rect_frame', width=0.53, height=0.72, pos=[0,0.23], fillColor='FireBrick', lineColor='black', opacity=1)
option1a_run01=visual.ImageStim(win=win, name='option1a_run01',image=u'images/happy_black.gif', mask=u'None',ori=0, pos=[-0.36, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option2a_run01=visual.ImageStim(win=win, name='option2a_run01',image=u'images/sad_black.gif', mask=u'None',ori=0, pos=[-0.12, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option3a_run01=visual.ImageStim(win=win, name='option3a_run01',image=u'images/mad_black.gif', mask=u'None',ori=0, pos=[0.12, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option4a_run01=visual.ImageStim(win=win, name='option4a_run01',image=u'images/scared_black.gif', mask=u'None',ori=0, pos=[0.36, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option1_run01=visual.ImageStim(win=win, name='option1_run01',image=u'images/happy_white.gif', mask=u'None',ori=0, pos=[-0.36, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option2_run01=visual.ImageStim(win=win, name='option2_run01',image=u'images/sad_white.gif', mask=u'None',ori=0, pos=[-0.12, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option3_run01=visual.ImageStim(win=win, name='option3_run01',image=u'images/mad_white.gif', mask=u'None',ori=0, pos=[0.12, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
option4_run01=visual.ImageStim(win=win, name='option4_run01',image=u'images/scared_white.gif', mask=u'None',ori=0, pos=[0.36, -0.5], size=[0.2, 0.25],color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

options = {'happy': option1_run01, 'sad': option2_run01, 'mad': option3_run01, 'scared': option4_run01}
highlighted_options = {'happy': option1a_run01, 'sad': option2a_run01, 'mad': option3a_run01, 'scared': option4a_run01}

green_check=visual.ImageStim(win=win, name='green_check', image=u'buttons/green_check2.png', mask=None,ori=0, pos=[0, -0.78], size=[0.16, 0.24])
red_x=visual.ImageStim(win=win, name='red_x', image=u'buttons/red_x.png', mask=None,ori=0, pos=[0, -0.78], size=[0.16, 0.24])

feedback_options = [red_x, green_check]

#Initialize feedback
#fb = feedback.fb(win)

#create output structure
wb = xlwt.Workbook()
ws = wb.add_sheet('Emotion')
headers=['trial_number','trial_id','block','duration','intensity','exemplar','exemplar_gender','exemplar_adult','score','correct_response','selected_response','frame_displayed','response_time']
for col, header in enumerate(headers): ws.write(0,col,header)
trial_number=0

#Initialise clocks
trial_clock=core.Clock()

#set up variables
imagedict = {'a':'happy','b':'sad','c':'mad','d':'scared'}

def present_instructions(objects, audio_object=None, display_next_button=True):
    #present texts and pictures for instructions-- leave next button out of objects passed to function
    for object in objects: object.draw()
    if display_next_button: next_button.draw()
    win.flip()
    if audio_object: audio_object.play()
    
    while True:
        if display_next_button:
            if click() and next_button.contains(mouse): break
        else:
            if click(): break
        if 'escape' in event.getKeys(): save_and_quit()
    if audio_object: audio_object.stop()

def run_trial_no_images(dev, audio, thisTrial, trial_number):
    trial_clock.reset()
    correct = imagedict[thisTrial.condition]
    
    for option in options.values(): option.draw()
    audio.play()
    response_start = trial_clock.getTime()
    
    #wait for response
    event.clearEvents()
    choice=None
    while choice==None:
        if click():
            for key, option in options.iteritems():
                if option.contains(mouse): choice=key
        for option in options.values(): option.draw()
        win.flip()
        if 'escape' in event.getKeys(): save_and_quit()
    response_time=trial_clock.getTime() - response_start
    audio.stop()
    
    #highlight response and give feedback
    score = int(correct==choice)
    feedback = feedback_options[score]
    start_time = trial_clock.getTime()
    while trial_clock.getTime() - start_time < 1.:
        for key, option in options.iteritems():
            if choice!=key: option.draw()
        highlighted_options[choice].draw()
        feedback.draw()
        win.flip()
    
    #headers=['trial_number','trial_id','block','duration','intensity','exemplar','exemplar_gender','exemplar_adult','score','correct_response','selected_response','frame_displayed','response_time']
    output = dict(trial_number=trial_number, trial_id=thisTrial.trial_id, block=thisTrial.block, duration='NA', intensity='NA', 
        exemplar='NA', exemplar_gender='NA', exemplar_adult='NA', score=score, correct_response=correct, selected_response=choice,
        frame_displayed='NA', response_time=response_time)
    
    #next write the output variables
    for col,header in enumerate(headers):
        ws.write(trial_number,col,output[header])
    
    return output

def run_trial(dev, mov, thisTrial, trial_number):
    trial_clock.reset()
    correct=imagedict[thisTrial.condition]
    
    rect_frame.setFillColor('FireBrick')
    rect_frame.draw()
    mov.draw()
    mov.pause()
    nextFrameTime= mov._movie.get_next_video_timestamp()
    win.flip()
    
    #I don't know why, but this is also needed to clear the response queue (up to 50 button presses)
    for i in xrange(50): dev.poll_for_response()
    #clear events on button box
    dev.clear_response_queue()
    #wait for button press
    while True:
        dev.poll_for_response()
        if dev.response_queue_size()>0:
            response = dev.get_next_response()
            if response['key'] == key_num and response['pressed']: break
    response_start=trial_clock.getTime()
    
    #start movie
    rect_frame.setFillColor('Green')
    rect_frame.draw()
    mov.draw()
    mov.play()
    win.flip()
    frameCounter=1
    
    #wait for button to release
    pressed=True
    while pressed!=False:
        rect_frame.draw()
        mov.draw()
        if nextFrameTime != mov._movie.get_next_video_timestamp(): 
            frameCounter +=1
            print frameCounter
            nextFrameTime= mov._movie.get_next_video_timestamp()
        if frameCounter!=60: win.flip()
        #pressed = poll_for_response(dev,3)
        dev.poll_for_response()
        if dev.response_queue_size() > 0:
            response = dev.get_next_response()
            print 'response is', response
            if response['key'] == key_num: pressed = response['pressed']
            else: pressed = None
        else: pressed = None
        if 'escape' in event.getKeys(): save_and_quit()
    response_time = trial_clock.getTime() - response_start
    
    #change frame and pause movie
    rect_frame.setFillColor('FireBrick')
    mov.pause()
    
    #wait for response
    #event.clearEvents()
    mouse.getPos()
    choice=None
    while choice==None:
        if click():
            for key, option in options.iteritems():
                if option.contains(mouse): choice=key
        rect_frame.draw()
        mov.draw()
        for option in options.values(): option.draw()
        win.flip()
        if 'escape' in event.getKeys(): save_and_quit()
    
    #highlight response and give feedback
    score = int(correct==choice)
    feedback = feedback_options[score]
    start_time = trial_clock.getTime()
    while trial_clock.getTime() - start_time < 1.:
        rect_frame.draw()
        mov.draw()
        for key, option in options.iteritems():
            if choice!=key: option.draw()
        highlighted_options[choice].draw()
        feedback.draw()
        win.flip()
    
    #headers=['trial_number','trial_id','block','duration','intensity','exemplar','exemplar_gender','exemplar_adult','score','correct_response','selected_response','frame_displayed','response_time']
    output = dict(trial_number=trial_number, trial_id=thisTrial.trial_id, block=thisTrial.block, duration=thisTrial.duration, intensity=thisTrial.intensity, 
        exemplar=thisTrial.exemplar, exemplar_gender=thisTrial.Gender, exemplar_adult=str(thisTrial.Adult), score=score, correct_response=correct, selected_response=choice,
        frame_displayed=frameCounter, response_time=response_time)
    
    #next write the output variables
    for col,header in enumerate(headers):
        ws.write(trial_number,col,output[header])
    
    return output

def save_and_quit():
    wb.save(filename+'.xls')
    core.quit()

#intro text
present_instructions([text_intro], display_next_button=False)

#set positions of emotion icons and present instructions
#a_=data.importConditions('conditions/practice_01.csv')[0]['a']
#b_=data.importConditions('conditions/practice_01.csv')[0]['b']
#c_=data.importConditions('conditions/practice_01.csv')[0]['c']
#d_=data.importConditions('conditions/practice_01.csv')[0]['d']
#positions = [[0,0,0,0],[-0.1,0.1,0,0],[-0.2,0,0.2,0],[-0.36,-0.12,0.12,0.36]] #x-coordinates for 1,2,3, and 4 choice images
#option1_run01.setPos((positions[a_+b_+c_+d_-1][0],-0.1))
#option2_run01.setPos((positions[a_+b_+c_+d_-1][a_],-0.1))
#option3_run01.setPos((positions[a_+b_+c_+d_-1][a_+b_],-0.1))
#option4_run01.setPos((positions[a_+b_+c_+d_-1][a_+b_+c_],-0.1))
#present_instructions([option1_run01,option2_run01,option3_run01,option4_run01,text_01], audio_object=audio_instructions_01)
#
#reset positions of emotion icons
#option1_run01.setPos((positions[a_+b_+c_+d_-1][0],-0.5))
#option2_run01.setPos((positions[a_+b_+c_+d_-1][a_],-0.5))
#option3_run01.setPos((positions[a_+b_+c_+d_-1][a_+b_],-0.5))
#option4_run01.setPos((positions[a_+b_+c_+d_-1][a_+b_+c_],-0.5))

#start practice_01
#while True:
#    practice_trials_01=data.TrialHandler(nReps=1, method='random', trialList=data.importConditions('conditions/practice_01.csv'))
#    total_score = 0
#    for thisTrial in practice_trials_01:
#        if thisTrial!=None:
#            for paramName in thisTrial.keys():
#                exec(paramName+'=thisTrial.'+paramName)
#        trial_number+=1
#        
#        #set stimuli
#        trial_audio=sound.Sound(u'audio/New Instructions 20130508/Loud Versions/audio_%s.wav' % audio ,secs=2.5)
#        trial_audio.setVolume(1)
#        
#        #run trial
#        output = run_trial_no_images(dev,trial_audio,thisTrial, trial_number)
#        total_score+=output['score']
#        
#    if total_score == practice_trials_01.nTotal: break
#    
#    #replay instructions
#    present_instructions([text_replay_01], audio_object=audio_replay_01)
#
#start practice_02
#present_instructions([text_02],audio_object=audio_instructions_02)
#
#while True:
#    practice_trials_02=data.TrialHandler(nReps=1, method='random', trialList=data.importConditions('conditions/practice_02.csv'))
#    total_score = 0
#    
#    for thisTrial in practice_trials_02:
#        if thisTrial!=None:
#            for paramName in thisTrial.keys():
#                exec(paramName+'=thisTrial.'+paramName)
#        trial_number+=1
#        
#        mov = visual.MovieStim(win=win, filename='videos/%s/%s_%s/%s_%s_mov_%s.mov' % (exemplar, exemplar, imagedict[condition], exemplar, imagedict[condition], duration), pos = [0,80], opacity = 1, name='movie')
#        output = run_trial(dev,mov,thisTrial, trial_number)
#        
#        total_score+=output['score']
#    if total_score == practice_trials_02.nTotal: break
#    
#    #replay instructions
#    present_instructions([text_replay_02], audio_object=audio_replay_02)
#
#
#start practice_03
#present_instructions([text_03],audio_object=audio_instructions_03)
#
#while True:
#    practice_trials_03=data.TrialHandler(nReps=1, method='random', trialList=data.importConditions('conditions/practice_03.csv'))
#    total_score = 0
#    
#    for thisTrial in practice_trials_03:
#        if thisTrial!=None:
#            for paramName in thisTrial.keys():
#                exec(paramName+'=thisTrial.'+paramName)
#        trial_number+=1
#        
#        mov = visual.MovieStim(win=win, filename='videos/%s/%s_%s/%s_%s_mov_%s.mov' % (exemplar, exemplar, imagedict[condition], exemplar, imagedict[condition], duration), pos = [0,80], opacity = 1, name='movie')
#        output = run_trial(dev,mov,thisTrial, trial_number)
#        
#        total_score+=output['score']
#    if total_score == practice_trials_03.nTotal: break
#    
#    #replay instructions
#    present_instructions([text_replay_03], audio_object=audio_replay_03)
#
#start trial
#present_instructions([text_trial],audio_object=audio_instructions_trial)
#trials=data.TrialHandler(nReps=1, method='sequential', trialList=data.importConditions(trial_conditions))
#
#for thisTrial in trials:
#    trial_number+=1
#    #use this code if want to restart from a certain point
#    #if trial_number<12: continue
#    if thisTrial!=None:
#        for paramName in thisTrial.keys():
#            exec(paramName+'=thisTrial.'+paramName)
#    
#    mov = visual.MovieStim(win=win, filename='videos/%s/%s_%s/%s_%s_mov_%s.mov' % (exemplar, exemplar, imagedict[condition], exemplar, imagedict[condition], duration), pos = [0,80], opacity = 1, name='movie')
#    run_trial(dev,mov,thisTrial, trial_number)
#

#Ranking portion
present_instructions([instr],audio_object=audio_endchoice)

#create trial handler to save data
emotion_ranking=data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=None, originPath=None,
    trialList=[{'emotion': 'happy'}, {'emotion': 'sad'}, {'emotion': 'mad'}, {'emotion': 'scared'}])

leftward = -0.4 # use pix units, because the drawing window's units are pix
rightward = -1 * leftward

ScaleL1 = visual.RatingScale(win, mouseOnly=True, pos=(leftward,0.15),
    markerColor='DarkGreen', size=0.85,name='ScaleL1',
    scale = '', low=1, high=4)
ScaleL2 = visual.RatingScale(win, mouseOnly=True, pos=(leftward,-0.7),
    markerColor='DarkGreen', size=0.85,name='ScaleL2',
    scale = '', low=1, high=4)
ScaleR1 = visual.RatingScale(win, mouseOnly=True, pos=(rightward,0.15),
    markerColor='DarkGreen', size=0.85,name='ScaleR1',
    scale = '', low=1, high=4)
ScaleR2 = visual.RatingScale(win, mouseOnly=True, pos=(rightward,-0.7),
    markerColor='DarkGreen', size=0.85,name='ScaleR2',
    scale = '', low=1, high=4)# for logging, its useful to give names, esp when there are 2 on-scree]n
ScaleWarning=visual.TextStim(win, text="No two ratings may be the same.", pos = [0,-0.85], height=0.06, wrapWidth= 1, color=u'Red')
emotionLabel=visual.TextStim(win, text="", pos = [0,0.8], height = 0.1)

ImageL1 = visual.ImageStim(win, image="images/happy_black.gif", pos=[leftward, 0.45], size=[0.5, 0.5])
ImageL2 = visual.ImageStim(win, image="images/happy_black.gif", pos=[leftward, -0.40],size=[0.5, 0.5])
ImageR1= visual.ImageStim(win, image="images/happy_black.gif", pos=[rightward, 0.45], size=[0.5, 0.5])
ImageR2 = visual.ImageStim(win, image="images/happy_black.gif", pos=[rightward, -0.40],size=[0.5, 0.5])


emotionList=['happy', 'sad', 'mad', 'scared']
for thisTrial in emotion_ranking:
    if thisTrial!=None:
        for paramName in thisTrial.keys():
            exec(paramName+'=thisTrial.'+paramName)
    emotionLabel.setText(str.capitalize(emotion) + ' (1=least, 4=most)')
    ImageL1.setImage(u'images/am1/am1_%s/am1_%s_60.bmp' %(emotion, emotion))
    ImageL2.setImage(u'images/am2/am2_%s/am2_%s_60.bmp' %(emotion, emotion))
    ImageR1.setImage(u'images/af1/af1_%s/af1_%s_60.bmp' %(emotion, emotion))
    ImageR2.setImage(u'images/af4/af4_%s/af4_%s_60.bmp' %(emotion, emotion))

    event.clearEvents()
    continueScale = True

    emotionLabel.setAutoDraw(True)
    ImageL1.setAutoDraw(True)
    ImageL2.setAutoDraw(True)
    ImageR1.setAutoDraw(True)
    ImageR2.setAutoDraw(True)
    ScaleL1.setAutoDraw(True)
    ScaleL2.setAutoDraw(True)
    ScaleR1.setAutoDraw(True)
    ScaleR2.setAutoDraw(True)

    while continueScale:
        ScaleL1.reset()
        ScaleL2.reset()
        ScaleR1.reset()
        ScaleR2.reset()
        ScaleL1.marker.setFillColor('DarkGreen')
        ScaleL2.marker.setFillColor('DarkGreen')
        ScaleR1.marker.setFillColor('DarkGreen')
        ScaleR2.marker.setFillColor('DarkGreen')
        while ScaleL1.noResponse or ScaleL2.noResponse or ScaleR1.noResponse or ScaleR2.noResponse:
            if 'escape' in event.getKeys(): save_and_quit()
            event.mouseButtons=[1,0,0]
            ScaleL1.frame = 0
            ScaleL2.frame = 0
            ScaleR1.frame = 0
            ScaleR2.frame = 0
            win.flip()
        ScaleL1.response = ScaleL1.getRating()
        ScaleL2.response = ScaleL2.getRating()
        ScaleR1.response = ScaleR1.getRating()
        ScaleR2.response = ScaleR2.getRating()
        if (ScaleL1.response**2)+(ScaleL2.response**2)+(ScaleR1.response**2)+(ScaleR2.response**2) != 30:
            continueScale = True
            ScaleWarning.setAutoDraw(True)
        else: 
            continueScale = False
            ScaleWarning.setAutoDraw(False)
            emotion_ranking.addData('am1',ScaleL1.response)
            emotion_ranking.addData('am2',ScaleL2.response)
            emotion_ranking.addData('af1',ScaleR1.response)
            emotion_ranking.addData('af4',ScaleR2.response)

emotion_ranking.saveAsExcel(filename+'_ranking.xlsx', sheetName='emotion_ranking',
    #stimOut=['intensity','duration','audio'],
    dataOut=['am1_raw', 'am2_raw', 'af1_raw', 'af4_raw'],#['n','all_mean','all_std', 'all_raw', 'responserate_mean'],
    appendFile=True)

save_and_quit()
