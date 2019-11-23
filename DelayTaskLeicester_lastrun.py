#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.2),
    on Sat Nov 23 00:53:03 2019
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'DelayTask2'  # from the Builder filename that created this script
expInfo = {u'participant': u'1', u'delay_first': u'n', u'points_per_rnf': u'3', u'gender': u'f', u'age': u'20', u'credits_to_win': u'10000', u'credits': u'100', u'session': u'1', u'cost_responding': u'1', u'trial_duration': u'1', u'condition': u'a'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/omadav/Dropbox/Textos/programming_old/python/psychopy/DelayTaskLeicester/program/DelayTaskLeicester.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[1.000,1.000,1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
import csv, random

# Load images
#hand_img = 'hand_down.png'
#yoshi_img = 'yoshi_coin.png'
triangle_img = 'triangle.png'
button_pressed_img = 'button_img_pale.png'

#Load sounds
coin = sound.Sound('coin.wav')
reward = sound.Sound('reward2.wav')
begin_trial = sound.Sound('begin_trial.wav')
exp_finished = sound.Sound('exp_finished.wav')

# Parameters for the VI
#scheduleParameter = [int(expInfo['parameter1']),int(expInfo['parameter2'])] # schedule parameters 
#limit = int(expInfo['limit']) # variability of intervals


# interval to reinforce for first trial on a VI schedule
#intervalToRnf = scheduleParameter[0]

credits = int(expInfo['credits'])
credits_to_win = float(expInfo['credits_to_win'])
points_per_rnf = float(expInfo['points_per_rnf'])
cost_responding = int(expInfo['cost_responding'])

time_on_screen = 0.4 # how long the reward is gonna show on the screen

# initialise parameter for RIplus
tSinceLastRnf = 0

# initialise parameters for RPI 
#tRPI = 0
#RnfProbRPI = 0

# Initialise parameters for RI
shouldBeReinforced = False # flag to set next reinforcer for RI schedule

# Initialise parameters for FR and RI+
n_resp_since_last_rnf = 0

# create mouse event
#mouse = event.Mouse(visible=True)

# Messages to show when rewarded 
#img = visual.ImageStim(win, image=triangle_img, pos=(0, 0), size=1)
button_pressed = visual.ImageStim(win, image=button_pressed_img, pos=(-.5, -.2))
button_pressed.size = 0.5

class Schedule(object):
    ''' this class initialise the schedule according to type and
    parameter, and gives reinforcers by the method giveRnf. '''
    def __init__(self, type, parameter, m=5):
        self.type = type
        self.parameter = parameter
        self.m = m

    def giveRnf(self, t):
        global credits, trainingClock, tRPI, RnfProbRPI, shouldBeReinforced, nReinf, n_resp_since_last_rnf, reinf_times_delay#, intervalToRnf

        if self.type == "RR":
            if np.random.binomial(1, 1/self.parameter):
                reward_to_screen()
                wasRnf.append(1)
                nReinf += 1
            else:
                wasRnf.append(0)
 
        elif self.type == "RPI":            
            if len(response.rt) > self.m + 1:
                tRPI = response.rt[-1] - response.rt[-self.m - 1]
                RnfProbRPI = tRPI/(self.m*self.parameter) 
                if np.random.binomial(1, RnfProbRPI):
                    reward_to_screen()
                    wasRnf.append(1)
                    nReinf += 1
                else: 
                    wasRnf.append(0)
            else:
                wasRnf.append(0)

        elif self.type == 'RI':
            if shouldBeReinforced:
                reward_to_screen()
                shouldBeReinforced = not shouldBeReinforced
                wasRnf.append(1)
                nReinf += 1
            else: 
                wasRnf.append(0)
        
        elif self.type == 'Delay':
                reinf_times_delay.append(t + self.parameter)
                wasRnf.append(0)
            
        elif self.type == 'FR':
            if n_resp_since_last_rnf == self.parameter:
                reward_to_screen()
                wasRnf.append(1)
                nReinf += 1
                n_resp_since_last_rnf = 0 #reset this to start counting again
        
        elif self.type == 'CRF':
            reward_to_screen()
            wasRnf.append(1)
            nReinf += 1
            n_resp_since_last_rnf = 0 #reset this to start counting again

        return t, trainingClock, wasRnf#, reinf_time #, RnfProbRPI, intervalToRnf

def reward_to_screen():
    global credits
    reward.play()
    #img.draw()
    msg = visual.TextStim(win, text="You have won two shares of " + company_name +"!", pos=(0, 0.5), color= u'green', bold=True)
    msg.draw() # deleted for causal judgment task
    credits += points_per_rnf
    reinf_times.append(t)
    #wasRnf.append(1)
    win.flip()
    core.wait(time_on_screen)    
    return reinf_times, wasRnf

def msg_to_screen(msg,x,y, autodraw=False):
    text_object=visual.TextStim(win, text=msg, pos=(x,y), color=u'black')
    text_object.setAutoDraw(autodraw) # autodraw is false so that the txt doesn't appear constantly
    text_object.draw()

def img_to_screen(img, position=(0, 0), autodraw=False):
    ''' Draws an image into the screen '''
    img = visual.ImageStim(win, image=img, pos=position)
    img.draw()

def show_debugging_stuff():
    #nextIntRnf_txt = visual.TextStim(win, text="nextIntRnf: " + str(intervalToRnf), pos=(0, 0.8), color=u'black')
    #nextIntRnf_txt.draw()

    t_txt=visual.TextStim(win, text='t: ' + str(round(t,2)), pos=(-0.5, 0.6), color=u'black')
    t_txt.draw()

    timer_txt=visual.TextStim(win, text='timer: ' + str(round(timer.getTime(),2)), pos=(0.5, -0.6), color=u'black')
    timer_txt.draw()

    msg_to_screen('trial: ' + str(trial), -0.8, -0.9)
    #msg_to_screen('tSinceLastRnf: ' + str(round(tSinceLastRnf,2)), 0.6, -0.9)
    #msg_to_screen('RnfProbRPI: ' + str(round(RnfProbRPI,2)), -0.1, -0.9)
    #msg_to_screen('shouldBeRnf: ' + str(shouldBeReinforced), 0, -0.7)
    msg_to_screen('n_resp_since_last_rnf: ' + str(n_resp_since_last_rnf), -0.1, -0.8)
    msg_to_screen('reinf_times: ' + str(reinf_times), -0.7, -0.9)

trial = 0 # initialise trial number

# Show debugging stuff?
debugging = False

# create a csv file to save response times etc
file_name = 'data/S%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])
csv_file = open(file_name+'.csv', 'wb')
writer_object = csv.writer(csv_file, delimiter=",") 

writer_object.writerow(['session', 'participant', 'response.keys', 'response.rt', 'wasRnf', 'irt', 'trials.thisN', 'trial', 'schedule', 'parameter', 'nResp', 'nReinf', 'city', 'company1', 'company2', 'devalued_company']) # this is the first row with headers for columns



# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instructions1 = visual.TextStim(win=win, name='instructions1',
    text="You are a stockholder and control the shares of two companies, 'Globex Corporation' and 'Initech Corporation'. During the task you will be trading in two cities, London and Paris.\n\nYou must earn as many points as possible by pressing the letters 'a' and 'l' on the keyboard. The 'a' will press the button on the left and the 'l' the button on the right.\n\nPress 'c' to continue",
    font='Arial',
    pos=[0, 0], height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "instructions2"
instructions2Clock = core.Clock()
instructions2_txt = visual.TextStim(win=win, name='instructions2_txt',
    text=u"Every time you press one of the buttons to invest, you will be buying one share = 3 points. \n\nThere is also a processing fee of 1 point for each press that you make. \n\nRemember, try to earn as many points as possible. The participant that earns the most points at the end of the study will win a \xa310 Amazon gift card which can be used as you wish.\n\nGood luck!\n\nPress 'c' to continue\n",
    font='Arial',
    pos=[0, 0], height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "training"
trainingClock = core.Clock()
background = visual.ImageStim(
    win=win, name='background',units='norm', 
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=2,
    color=[1,1,1], colorSpace='rgb', opacity=.35,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
button_image1 = visual.ImageStim(
    win=win, name='button_image1',
    image='sin', mask=None,
    ori=0, pos=[-0.5, -0.2], size=[0.5, 0.5],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
button_image2 = visual.ImageStim(
    win=win, name='button_image2',
    image='sin', mask=None,
    ori=0, pos=[0.5, -0.2], size=[0.5, 0.5],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
crd_text = visual.TextStim(win=win, name='crd_text',
    text='Shares',
    font='Arial',
    pos=[0.0, 0.8], height=0.1, wrapWidth=None, ori=0, 
    color=[1.000,-1.000,-1.000], colorSpace='rgb', opacity=1,
    depth=-4.0);
condition_txt = visual.TextStim(win=win, name='condition_txt',
    text='default text',
    font='Arial',
    pos=[-0.5, -0.5], height=0.15, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=.3,
    depth=-5.0);
condition_txt_right = visual.TextStim(win=win, name='condition_txt_right',
    text='default text',
    font='Arial',
    pos=[0.5, -0.5], height=0.15, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=.3,
    depth=-6.0);
credits_txt = visual.TextStim(win=win, name='credits_txt',
    text=None,
    font='Arial',
    pos=(0, .7), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-7.0);
#I tested the code with RI because for RPI schedules around 7 or 6 response_times were lost from the csv file. The Ri works fine so that suggests that the memory size of 5-ish is causing the program not to save the responses before those 5ish. That I need to test next. 

rnfProb1=[] # here we save the rnf prob for each trial

#credits_txt =  visual.TextBox(window=win, text='text', font_size=30,
#                         font_color=[-1, -1, 1], size=(1.9, .3), pos=(0, 0.65), 
#                         grid_horz_justification='center', units='norm')


# Initialize components for Routine "ITI"
ITIClock = core.Clock()
text_ITI = visual.TextStim(win=win, name='text_ITI',
    text="Now press 'c' to go to the next trading session.",
    font='Arial',
    pos=[0, 0], height=0.10, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "devaluation"
devaluationClock = core.Clock()
image = visual.ImageStim(
    win=win, name='image',units='norm', 
    image='devaluation_img.png', mask=None,
    ori=0, pos=[0, 0], size=2,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
devaluation_text = visual.TextStim(win=win, name='devaluation_text',
    text='default text',
    font='Arial',
    pos=[0, .4], height=0.15, wrapWidth=None, ori=0, 
    color='red', colorSpace='rgb', opacity=1,
    depth=-2.0);
text_2 = visual.TextStim(win=win, name='text_2',
    text='The economy is booming, but not for all companies. The company below has crashed:\n\n\n\n',
    font='Arial',
    pos=[0, 0.5], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-3.0);
text_3 = visual.TextStim(win=win, name='text_3',
    text="Press 'c' to continue",
    font='Arial',
    pos=[0, -.7], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-4.0);
non_devaluation_text = visual.TextStim(win=win, name='non_devaluation_text',
    text='default text',
    font='Arial',
    pos=[0, -.2], height=0.15, wrapWidth=None, ori=0, 
    color='green', colorSpace='rgb', opacity=1,
    depth=-5.0);
text_4 = visual.TextStim(win=win, name='text_4',
    text='However, this company is doing better:',
    font='Arial',
    pos=[0, 0.1], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-6.0);

# Initialize components for Routine "devaluation_2"
devaluation_2Clock = core.Clock()
image_2 = visual.ImageStim(
    win=win, name='image_2',units='norm', 
    image='devaluation_img.png', mask=None,
    ori=0, pos=[0, 0], size=2,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
devaluation_text_2 = visual.TextStim(win=win, name='devaluation_text_2',
    text="You shall continue trading in London and Paris. However, due to a malfunction with the trading equipment you will not receive any feedback.\n\nPress 'c' to continue.",
    font='Arial',
    pos=[0, 0], height=0.10, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Initialize components for Routine "trial2"
trial2Clock = core.Clock()
# create a csv file to save response times etc
file_name1 = 'data/S%s_%s_%s_Test' %(expInfo['participant'], expName, expInfo['date'])
csv_file1 = open(file_name1+'.csv', 'wb')
writer_object1 = csv.writer(csv_file1, delimiter=",") 

writer_object1.writerow(['session', 'participant', 'response.keys', 'response.rt','trials', 'nResp', 'city', 'company1', 'company2', 'devalued_company']) # this is the first row with headers for columns

# this file saves ps for each session = 30 reinf, for ex.
#file_name2 = '%s_%s_model%i_Sessions-' %(schedule.name, schedule.parameter, model)
#csv_file2 = open(file_name2 + str(datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")) + '.csv', 'wb')
#writer_object2 = csv.writer(csv_file2, delimiter=",") 
#writer_object2.writerow(['session', 'prob_type', 'prob_value', 'rat', 'schedule', 'parameter'])


# Initialize components for Routine "ITI"
ITIClock = core.Clock()
text_ITI = visual.TextStim(win=win, name='text_ITI',
    text="Now press 'c' to go to the next trading session.",
    font='Arial',
    pos=[0, 0], height=0.10, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "training_2"
training_2Clock = core.Clock()
background_2 = visual.ImageStim(
    win=win, name='background_2',units='norm', 
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=2,
    color=[1,1,1], colorSpace='rgb', opacity=.35,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
button_image1_2 = visual.ImageStim(
    win=win, name='button_image1_2',
    image='sin', mask=None,
    ori=0, pos=[-0.5, -0.2], size=[0.5, 0.5],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
button_image2_2 = visual.ImageStim(
    win=win, name='button_image2_2',
    image='sin', mask=None,
    ori=0, pos=[0.5, -0.2], size=[0.5, 0.5],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
crd_text_2 = visual.TextStim(win=win, name='crd_text_2',
    text='Shares',
    font='Arial',
    pos=[0.0, 0.8], height=0.1, wrapWidth=None, ori=0, 
    color=[1.000,-1.000,-1.000], colorSpace='rgb', opacity=0,
    depth=-4.0);
condition_txt_2 = visual.TextStim(win=win, name='condition_txt_2',
    text='default text',
    font='Arial',
    pos=[-.5, -.7], height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=0,
    depth=-5.0);
condition_txt_2_right = visual.TextStim(win=win, name='condition_txt_2_right',
    text='default text',
    font='Arial',
    pos=[.5, -.7], height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-6.0);
#I tested the code with RI because for RPI schedules around 7 or 6 response_times were lost from the csv file. The Ri works fine so that suggests that the memory size of 5-ish is causing the program not to save the responses before those 5ish. That I need to test next. 

rnfProb1=[] # here we save the rnf prob for each trial
trial=0

# Initialize components for Routine "contingency_tests"
contingency_testsClock = core.Clock()
background_contingency_test = visual.ImageStim(
    win=win, name='background_contingency_test',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=2,
    color=[1,1,1], colorSpace='rgb', opacity=.35,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
contingency_question_txt = visual.TextStim(win=win, name='contingency_question_txt',
    text='default text',
    font='Arial',
    pos=(0, 0.7), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
company_name_txt = visual.TextStim(win=win, name='company_name_txt',
    text='default text',
    font='Arial',
    pos=(0, .55), height=0.2, wrapWidth=None, ori=0, 
    color='green', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Initialize components for Routine "contingency_tests2"
contingency_tests2Clock = core.Clock()
background_contingency_test2 = visual.ImageStim(
    win=win, name='background_contingency_test2',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=2,
    color=[1,1,1], colorSpace='rgb', opacity=.35,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
contingency_question_txt2 = visual.TextStim(win=win, name='contingency_question_txt2',
    text='Please press the button that gave you a share of this company in this city: ',
    font='Arial',
    pos=(0, 0.7), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);
company_name_txt2 = visual.TextStim(win=win, name='company_name_txt2',
    text='default text',
    font='Arial',
    pos=(0, .55), height=0.2, wrapWidth=None, ori=0, 
    color='green', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
thanks1 = visual.TextStim(win=win, name='thanks1',
    text='Experiment finished!                                                                 Press "f" to finish the experiment.',
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);
expFinished = visual.ImageStim(
    win=win, name='expFinished',
    image='Slide7.png', mask=None,
    ori=0, pos=[0, 0], size=[2, 2],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
finishedSound = sound.Sound('exp_finished.wav', secs=-1)
finishedSound.setVolume(0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(0.500000)
# update component parameters for each repeat

# keep track of which components have finished
trialComponents = [ISI]
for thisComponent in trialComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "trial"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = trialClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ISI* period
    if t >= 0.0 and ISI.status == NOT_STARTED:
        # keep track of start time/frame for later
        ISI.tStart = t
        ISI.frameNStart = frameN  # exact frame index
        ISI.start(0.5)
    elif ISI.status == STARTED:  # one frame should pass before updating params and completing
        ISI.complete()  # finish the static period
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_5 = event.BuilderKeyResponse()
# keep track of which components have finished
instructionsComponents = [instructions1, key_resp_5]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions1* updates
    if t >= 0.0 and instructions1.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions1.tStart = t
        instructions1.frameNStart = frameN  # exact frame index
        instructions1.setAutoDraw(True)
    
    # *key_resp_5* updates
    if t >= 0.0 and key_resp_5.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_5.tStart = t
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_5.status == STARTED:
        theseKeys = event.getKeys(keyList=['c'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_5.keys = theseKeys[-1]  # just the last key pressed
            key_resp_5.rt = key_resp_5.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_5.keys in ['', [], None]:  # No response was made
    key_resp_5.keys=None
thisExp.addData('key_resp_5.keys',key_resp_5.keys)
if key_resp_5.keys != None:  # we had a response
    thisExp.addData('key_resp_5.rt', key_resp_5.rt)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instructions2"-------
t = 0
instructions2Clock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_6 = event.BuilderKeyResponse()
# keep track of which components have finished
instructions2Components = [instructions2_txt, key_resp_6]
for thisComponent in instructions2Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions2"-------
while continueRoutine:
    # get current time
    t = instructions2Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions2_txt* updates
    if t >= 0.0 and instructions2_txt.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions2_txt.tStart = t
        instructions2_txt.frameNStart = frameN  # exact frame index
        instructions2_txt.setAutoDraw(True)
    
    # *key_resp_6* updates
    if t >= 0.0 and key_resp_6.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_6.tStart = t
        key_resp_6.frameNStart = frameN  # exact frame index
        key_resp_6.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_6.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_6.status == STARTED:
        theseKeys = event.getKeys(keyList=['c'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_6.keys = theseKeys[-1]  # just the last key pressed
            key_resp_6.rt = key_resp_6.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructions2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions2"-------
for thisComponent in instructions2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_6.keys in ['', [], None]:  # No response was made
    key_resp_6.keys=None
thisExp.addData('key_resp_6.keys',key_resp_6.keys)
if key_resp_6.keys != None:  # we had a response
    thisExp.addData('key_resp_6.rt', key_resp_6.rt)
thisExp.nextEntry()
# the Routine "instructions2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
training_trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(expInfo['condition']+'.xlsx'),
    seed=None, name='training_trials')
thisExp.addLoop(training_trials)  # add the loop to the experiment
thisTraining_trial = training_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTraining_trial.rgb)
if thisTraining_trial != None:
    for paramName in thisTraining_trial.keys():
        exec(paramName + '= thisTraining_trial.' + paramName)

for thisTraining_trial in training_trials:
    currentLoop = training_trials
    # abbreviate parameter names if possible (e.g. rgb = thisTraining_trial.rgb)
    if thisTraining_trial != None:
        for paramName in thisTraining_trial.keys():
            exec(paramName + '= thisTraining_trial.' + paramName)
    
    # ------Prepare to start Routine "training"-------
    t = 0
    trainingClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    background.setImage(background_colour)
    button_image1.setImage(button_img1)
    button_image2.setImage(button_img2)
    response = event.BuilderKeyResponse()
    condition_txt.setText(company1)
    condition_txt_right.setText(company2
)
    # these empty arrays below are filled as participant responds
    # they need to be erased after each trial, so they are put in "Begin Routine" and not "Begin Experiment"
    reinf_times = []
    wasRnf = []
    irt=[]
    company_names_rnf_delay = [] # this one is to save the company names to show on the screen for each reinforcer given in delay condition
    
    # to save reinf_times for delay reinforcement
    reinf_times_delay = []
    
    nResp = 0
    nReinf = 0
    
    #if continueRoutine:
    #begin_trial.play()
    
    # set a timer for the trial
    timer = core.CountdownTimer(float(expInfo['trial_duration']))
    
    # Current schedule and parameters
    if expInfo['delay_first'] == 'n':
        if trial %2 == 1: # if trial = 1,3,..., etc.
            schedule = Schedule('Delay', 5)
        elif trial % 2 == 0: # if trial = 0, 2, ..., etc.
            schedule = Schedule('CRF', 1) # the 1 does not mean anything
            #schedule = Schedule('FR', 1)
    else:
        if trial %2 == 1: # if trial = 1,3,..., etc.
            schedule = Schedule('CRF', 1)
        elif trial % 2 == 0: # if trial = 0, 2, ..., etc.
            schedule = Schedule('Delay', 5) # the 1 does not mean anything
            #schedule = Schedule('FR', 1)
    
    print(schedule.type)
    print(schedule.parameter)
    
    # Parameters for the RI and RI+ schedule: set tick each sec
    shouldBeReinforced = False # flag to set next reinforcer for RI schedule
    tickClock = core.CountdownTimer(1) # this is to tick every second
    
    # Clock for Debounce Time
    DebounceTimer = core.CountdownTimer(1)
    
    #reinf_delivery_time = 5 # this was to debug the delay schedule; it 
    # is replaced by reinf_times_delivery array
    # keep track of which components have finished
    trainingComponents = [background, button_image1, button_image2, response, crd_text, condition_txt, condition_txt_right, credits_txt]
    for thisComponent in trainingComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "training"-------
    while continueRoutine:
        # get current time
        t = trainingClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background* updates
        if t >= 0.0 and background.status == NOT_STARTED:
            # keep track of start time/frame for later
            background.tStart = t
            background.frameNStart = frameN  # exact frame index
            background.setAutoDraw(True)
        
        # *button_image1* updates
        if t >= 0.0 and button_image1.status == NOT_STARTED:
            # keep track of start time/frame for later
            button_image1.tStart = t
            button_image1.frameNStart = frameN  # exact frame index
            button_image1.setAutoDraw(True)
        
        # *button_image2* updates
        if t >= 0.0 and button_image2.status == NOT_STARTED:
            # keep track of start time/frame for later
            button_image2.tStart = t
            button_image2.frameNStart = frameN  # exact frame index
            button_image2.setAutoDraw(True)
        
        # *response* updates
        if t >= 0.0 and response.status == NOT_STARTED:
            # keep track of start time/frame for later
            response.tStart = t
            response.frameNStart = frameN  # exact frame index
            response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
        if response.status == STARTED:
            theseKeys = event.getKeys(keyList=['a', 'l'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                response.keys.extend(theseKeys)  # storing all keys
                response.rt.append(response.clock.getTime())
                # was this 'correct'?
                if (response.keys == str("'a','l'")) or (response.keys == "'a','l'"):
                    response.corr = 1
                else:
                    response.corr = 0
        
        # *crd_text* updates
        if t >= 0.0 and crd_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            crd_text.tStart = t
            crd_text.frameNStart = frameN  # exact frame index
            crd_text.setAutoDraw(True)
        
        # *condition_txt* updates
        if t >= 0.0 and condition_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            condition_txt.tStart = t
            condition_txt.frameNStart = frameN  # exact frame index
            condition_txt.setAutoDraw(True)
        
        # *condition_txt_right* updates
        if t >= 0.0 and condition_txt_right.status == NOT_STARTED:
            # keep track of start time/frame for later
            condition_txt_right.tStart = t
            condition_txt_right.frameNStart = frameN  # exact frame index
            condition_txt_right.setAutoDraw(True)
        
        # *credits_txt* updates
        if t >= 0.0 and credits_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            credits_txt.tStart = t
            credits_txt.frameNStart = frameN  # exact frame index
            credits_txt.setAutoDraw(True)
        if credits_txt.status == STARTED:  # only update if drawing
            credits_txt.setText('', log=False)
        #if mouse.isPressedIn(machine2_1):
        #    not_active1.pos = [-0.45, 0]
        #    schedule.type = 'RPI'
        #    schedule.parameter = 6
        
        #if mouse.isPressedIn(machine1):
        #    not_active1.pos = [0, 0]
        #    schedule.type = 'RR'
        #    schedule.parameter = 7
        
        
        
        if len(theseKeys)>0 and DebounceTimer.getTime() < 0: #DebounceTimer is the min IRT permitted
            #this_IRT = 0
            coin.play()
            if response.keys[-1] == 'a':
                button_pressed.pos = (-0.5, -0.2)
                company_name = str(company1)
            elif response.keys[-1] == 'l':
                button_pressed.pos = (0.5, -0.2)
                company_name = str(company2)
            print(str(schedule.type))
            print('company name:' + company_name)
            
            if schedule.type == "Delay":
                company_names_rnf_delay.append(company_name)
        
            DebounceTimer.reset() # re-start debounce timer 
        
            img_clock = core.Clock() # clock to show img for a n of sec
            while img_clock.getTime() < 0.10: # draw button pressed 
                if response.keys[-1] == 'a':
                    button_image1.setAutoDraw(False)
                elif response.keys[-1] == 'l':
                    button_image2.setAutoDraw(False)
                button_pressed.draw()
                win.flip()
                button_image1.setAutoDraw(True)
                button_image2.setAutoDraw(True)
        
            nResp += 1
            n_resp_since_last_rnf += 1
            credits -= int(expInfo['cost_responding'])
            schedule.giveRnf(response.rt[-1])
        
            if len(response.rt)>1:        
                irt.append(response.rt[-1]-response.rt[-2])
            else:
                irt.append(response.rt[-1]) 
            # write to csv on each frame in which there is a response
            try:
                writer_object.writerow([expInfo['session'], expInfo['participant'], response.keys[-1], response.rt[-1], wasRnf[-1], irt[-1], training_trials.thisN, trial, schedule.type, schedule.parameter, nResp, nReinf, background_colour[:-4], company1, company2, 'None'])
            except:
                pass
            
        
        if schedule.type == 'Delay' and len(reinf_times_delay)>0:
            if t >= reinf_times_delay[0] and t < int(expInfo['trial_duration']) - schedule.parameter: # give delayed reinforcer. Only if the response was such that the time left to the end of trial permits it.
                company_name = company_names_rnf_delay[0]
                company_names_rnf_delay.pop(0)
                reward_to_screen()
                reinf_times_delay.pop(0) # drop first reinf time
                wasRnf.append(1)
                response.keys.append('delayed_rnf')
                response.rt.append(t)
                nReinf += 1
                n_resp_since_last_rnf = 0 #reset this to start counting again
        #think about how to save the inter reinforcement intervals when delivering delayed rewards
        #            if len(response.rt)>1:        
        #                irt.append(response.rt[-1]-response.rt[-2])
        #            else:
        #                irt.append(response.rt[-1]) 
                writer_object.writerow([expInfo['session'], expInfo['participant'], response.keys[-1], response.rt[-1], wasRnf[-1], irt[-1], training_trials.thisN, trial, schedule.type, schedule.parameter, nResp, nReinf, background_colour[:-4], company1, company2, 'None'])
        #    except:
        #        pass
        
        if len(reinf_times) > 1:
            tSinceLastRnf = t - reinf_times[-1]
        
        # this is the tick for the RI and RI+ schedules
        if not shouldBeReinforced and tickClock.getTime() <= 0:
            shouldBeReinforced = np.random.binomial(1, 0.2)
            tickClock.reset()
        
        #if len(response.rt)>1:
        #    this_IRT = t - response.rt[-1] 
        #else: 
        #this_IRT = 0
            #print(this_IRT)
        
        #this_IRT = t - response.rt[-1] if nResp > 0 else t
        
        
        
        
        
        # this is just to debug
        #credits_txt = visual.TextStim(win, text=str(int(credits)), pos=(0.0, 0.65), color=u'black')
        
        credits_txt.setText(str(int(credits)))
        #credits_txt.draw()
        
        
        # this should be part of debug function; shows n of reinf and resp so far
        this_IRT_txt =  visual.TextStim(win, text=str(round(DebounceTimer.getTime(),2)), pos=(-0.5, 0.35), color=u'black')
        #nResp_txt = visual.TextStim(win, text=str(int(nResp)), pos=(0.8, 0.35), color=u'black')
        #nReinf_txt = visual.TextStim(win, text=str(int(nReinf)), pos=(0.8, 0.35), color=u'black')
        #this_IRT_txt.draw()
        #nResp_txt.draw()
        #nReinf_txt.draw()
        
        if debugging:
            show_debugging_stuff()
        
        #if timer.getTime() <= 0:
        #    continueRoutine=False
        
        if timer.getTime() <= 0 or credits >= credits_to_win:
            continueRoutine=False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trainingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "training"-------
    for thisComponent in trainingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if response.keys in ['', [], None]:  # No response was made
        response.keys=None
        # was no response the correct answer?!
        if str("'a','l'").lower() == 'none':
           response.corr = 1  # correct non-response
        else:
           response.corr = 0  # failed to respond (incorrectly)
    # store data for training_trials (TrialHandler)
    training_trials.addData('response.keys',response.keys)
    training_trials.addData('response.corr', response.corr)
    if response.keys != None:  # we had a response
        training_trials.addData('response.rt', response.rt)
    #intervalToRnf = scheduleParameter[1]# + np.random.permutation(limit)[0]
    
    #nResp = len(response_training.rt)
    #nReinf = len(reinf_times) 
    
    print("nResp: %f")%nResp
    print("nReinf: %f")%nReinf
    
    #if len(response.rt)>=1:
    #    rnfProb1.append(nReinf/nResp)
    #else: 
    #    rnfProb1.append(0) # if no responses, add zero
    #print("rnfProb: %f")%rnfProb1[-1]
    
    
    if response.keys != None:  # we had a response
        thisExp.addData('reinf_times', reinf_times)
        thisExp.addData('wasRnf', wasRnf)
        thisExp.addData('irts', irt)
        thisExp.addData('mean_irt', np.mean(irt))
        #thisExp.addData('rnf_prob', rnfProb1)
        thisExp.nextEntry()
    
    core.wait(2)
    
    trial += 1
    
    # the Routine "training" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "ITI"-------
    t = 0
    ITIClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_ITI = event.BuilderKeyResponse()
    # keep track of which components have finished
    ITIComponents = [text_ITI, key_resp_ITI]
    for thisComponent in ITIComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "ITI"-------
    while continueRoutine:
        # get current time
        t = ITIClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_ITI* updates
        if t >= 0.0 and text_ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_ITI.tStart = t
            text_ITI.frameNStart = frameN  # exact frame index
            text_ITI.setAutoDraw(True)
        
        # *key_resp_ITI* updates
        if t >= 0.0 and key_resp_ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_ITI.tStart = t
            key_resp_ITI.frameNStart = frameN  # exact frame index
            key_resp_ITI.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_ITI.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_ITI.status == STARTED:
            theseKeys = event.getKeys(keyList=['c'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_ITI.keys = theseKeys[-1]  # just the last key pressed
                key_resp_ITI.rt = key_resp_ITI.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ITIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "ITI"-------
    for thisComponent in ITIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_ITI.keys in ['', [], None]:  # No response was made
        key_resp_ITI.keys=None
    training_trials.addData('key_resp_ITI.keys',key_resp_ITI.keys)
    if key_resp_ITI.keys != None:  # we had a response
        training_trials.addData('key_resp_ITI.rt', key_resp_ITI.rt)
    # the Routine "ITI" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'training_trials'


# ------Prepare to start Routine "devaluation"-------
t = 0
devaluationClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_3 = event.BuilderKeyResponse()
devaluation_text.setText(devalued_company)
non_devaluation_text.setText(non_devalued_company)
# keep track of which components have finished
devaluationComponents = [image, key_resp_3, devaluation_text, text_2, text_3, non_devaluation_text, text_4]
for thisComponent in devaluationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "devaluation"-------
while continueRoutine:
    # get current time
    t = devaluationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *image* updates
    if t >= 0.0 and image.status == NOT_STARTED:
        # keep track of start time/frame for later
        image.tStart = t
        image.frameNStart = frameN  # exact frame index
        image.setAutoDraw(True)
    frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if image.status == STARTED and t >= frameRemains:
        image.setAutoDraw(False)
    
    # *key_resp_3* updates
    if t >= 0.0 and key_resp_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_3.tStart = t
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_3.status == STARTED:
        theseKeys = event.getKeys(keyList=['c'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_3.keys = theseKeys[-1]  # just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # *devaluation_text* updates
    if t >= 0.0 and devaluation_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        devaluation_text.tStart = t
        devaluation_text.frameNStart = frameN  # exact frame index
        devaluation_text.setAutoDraw(True)
    
    # *text_2* updates
    if t >= 0.0 and text_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_2.tStart = t
        text_2.frameNStart = frameN  # exact frame index
        text_2.setAutoDraw(True)
    
    # *text_3* updates
    if t >= 0.0 and text_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_3.tStart = t
        text_3.frameNStart = frameN  # exact frame index
        text_3.setAutoDraw(True)
    
    # *non_devaluation_text* updates
    if t >= 0.0 and non_devaluation_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        non_devaluation_text.tStart = t
        non_devaluation_text.frameNStart = frameN  # exact frame index
        non_devaluation_text.setAutoDraw(True)
    
    # *text_4* updates
    if t >= 0.0 and text_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_4.tStart = t
        text_4.frameNStart = frameN  # exact frame index
        text_4.setAutoDraw(True)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in devaluationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "devaluation"-------
for thisComponent in devaluationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys=None
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.nextEntry()
# the Routine "devaluation" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "devaluation_2"-------
t = 0
devaluation_2Clock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_4 = event.BuilderKeyResponse()
# keep track of which components have finished
devaluation_2Components = [image_2, key_resp_4, devaluation_text_2]
for thisComponent in devaluation_2Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "devaluation_2"-------
while continueRoutine:
    # get current time
    t = devaluation_2Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *image_2* updates
    if t >= 0.0 and image_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        image_2.tStart = t
        image_2.frameNStart = frameN  # exact frame index
        image_2.setAutoDraw(True)
    frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if image_2.status == STARTED and t >= frameRemains:
        image_2.setAutoDraw(False)
    
    # *key_resp_4* updates
    if t >= 0.0 and key_resp_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_4.tStart = t
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_4.status == STARTED:
        theseKeys = event.getKeys(keyList=['c'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_4.keys = theseKeys[-1]  # just the last key pressed
            key_resp_4.rt = key_resp_4.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # *devaluation_text_2* updates
    if t >= 0.0 and devaluation_text_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        devaluation_text_2.tStart = t
        devaluation_text_2.frameNStart = frameN  # exact frame index
        devaluation_text_2.setAutoDraw(True)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in devaluation_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "devaluation_2"-------
for thisComponent in devaluation_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_4.keys in ['', [], None]:  # No response was made
    key_resp_4.keys=None
thisExp.addData('key_resp_4.keys',key_resp_4.keys)
if key_resp_4.keys != None:  # we had a response
    thisExp.addData('key_resp_4.rt', key_resp_4.rt)
thisExp.nextEntry()
# the Routine "devaluation_2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "trial2"-------
t = 0
trial2Clock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat

# keep track of which components have finished
trial2Components = []
for thisComponent in trial2Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "trial2"-------
while continueRoutine:
    # get current time
    t = trial2Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trial2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "trial2"-------
for thisComponent in trial2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "trial2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
devaluation_test = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(expInfo['condition']+'.xlsx'),
    seed=None, name='devaluation_test')
thisExp.addLoop(devaluation_test)  # add the loop to the experiment
thisDevaluation_test = devaluation_test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisDevaluation_test.rgb)
if thisDevaluation_test != None:
    for paramName in thisDevaluation_test.keys():
        exec(paramName + '= thisDevaluation_test.' + paramName)

for thisDevaluation_test in devaluation_test:
    currentLoop = devaluation_test
    # abbreviate parameter names if possible (e.g. rgb = thisDevaluation_test.rgb)
    if thisDevaluation_test != None:
        for paramName in thisDevaluation_test.keys():
            exec(paramName + '= thisDevaluation_test.' + paramName)
    
    # ------Prepare to start Routine "ITI"-------
    t = 0
    ITIClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_ITI = event.BuilderKeyResponse()
    # keep track of which components have finished
    ITIComponents = [text_ITI, key_resp_ITI]
    for thisComponent in ITIComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "ITI"-------
    while continueRoutine:
        # get current time
        t = ITIClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_ITI* updates
        if t >= 0.0 and text_ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_ITI.tStart = t
            text_ITI.frameNStart = frameN  # exact frame index
            text_ITI.setAutoDraw(True)
        
        # *key_resp_ITI* updates
        if t >= 0.0 and key_resp_ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_ITI.tStart = t
            key_resp_ITI.frameNStart = frameN  # exact frame index
            key_resp_ITI.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_ITI.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_ITI.status == STARTED:
            theseKeys = event.getKeys(keyList=['c'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_ITI.keys = theseKeys[-1]  # just the last key pressed
                key_resp_ITI.rt = key_resp_ITI.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ITIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "ITI"-------
    for thisComponent in ITIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_ITI.keys in ['', [], None]:  # No response was made
        key_resp_ITI.keys=None
    devaluation_test.addData('key_resp_ITI.keys',key_resp_ITI.keys)
    if key_resp_ITI.keys != None:  # we had a response
        devaluation_test.addData('key_resp_ITI.rt', key_resp_ITI.rt)
    # the Routine "ITI" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "training_2"-------
    t = 0
    training_2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    background_2.setImage(background_colour)
    button_image1_2.setImage(button_img1)
    button_image2_2.setImage(button_img2)
    response_2 = event.BuilderKeyResponse()
    condition_txt_2.setText(company1
)
    condition_txt_2_right.setText(company2)
    # these empty arrays below are filled as participant responds
    # they need to be erased after each trial, so they are put in "Begin Routine" and not "Begin Experiment"
    reinf_times = []
    wasRnf = []
    irt=[]
    
    # to save reinf_times for delay reinforcement
    reinf_times_delay = []
    
    nResp = 0
    nReinf = 0
    
    #if continueRoutine:
    #begin_trial.play()
    
    # set a timer for the trial
    timer = core.CountdownTimer(float(expInfo['trial_duration']))
    
    # Current schedule and parameters
    if trial in [1,3,5,7,9,11,13,15]: # if trial = 1,3,..., etc.
        schedule = Schedule('Delay', 3)
    elif trial in [0,2,4,6,8,10,12,14]: # if trial = 0, 2, ..., etc.
        schedule = Schedule('FR', 1)
    print(schedule.type)
    print(schedule.parameter)
    
    # Parameters for the RI and RI+ schedule: set tick each sec
    shouldBeReinforced = False # flag to set next reinforcer for RI schedule
    tickClock = core.CountdownTimer(1) # this is to tick every second
    
    # Clock for Debounce Time
    DebounceTimer = core.CountdownTimer(1)
    
    #reinf_delivery_time = 5 # this was to debug the delay schedule; it 
    # is replaced by reinf_times_delivery array
    # keep track of which components have finished
    training_2Components = [background_2, button_image1_2, button_image2_2, response_2, crd_text_2, condition_txt_2, condition_txt_2_right]
    for thisComponent in training_2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "training_2"-------
    while continueRoutine:
        # get current time
        t = training_2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background_2* updates
        if t >= 0.0 and background_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            background_2.tStart = t
            background_2.frameNStart = frameN  # exact frame index
            background_2.setAutoDraw(True)
        
        # *button_image1_2* updates
        if t >= 0.0 and button_image1_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            button_image1_2.tStart = t
            button_image1_2.frameNStart = frameN  # exact frame index
            button_image1_2.setAutoDraw(True)
        
        # *button_image2_2* updates
        if t >= 0.0 and button_image2_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            button_image2_2.tStart = t
            button_image2_2.frameNStart = frameN  # exact frame index
            button_image2_2.setAutoDraw(True)
        
        # *response_2* updates
        if t >= 0.0 and response_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            response_2.tStart = t
            response_2.frameNStart = frameN  # exact frame index
            response_2.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(response_2.clock.reset)  # t=0 on next screen flip
        if response_2.status == STARTED:
            theseKeys = event.getKeys(keyList=['a', 'l'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                response_2.keys.extend(theseKeys)  # storing all keys
                response_2.rt.append(response_2.clock.getTime())
        
        # *crd_text_2* updates
        if t >= 0.0 and crd_text_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            crd_text_2.tStart = t
            crd_text_2.frameNStart = frameN  # exact frame index
            crd_text_2.setAutoDraw(True)
        frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if crd_text_2.status == STARTED and t >= frameRemains:
            crd_text_2.setAutoDraw(False)
        
        # *condition_txt_2* updates
        if t >= 0.0 and condition_txt_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            condition_txt_2.tStart = t
            condition_txt_2.frameNStart = frameN  # exact frame index
            condition_txt_2.setAutoDraw(True)
        frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if condition_txt_2.status == STARTED and t >= frameRemains:
            condition_txt_2.setAutoDraw(False)
        
        # *condition_txt_2_right* updates
        if t >= 0.0 and condition_txt_2_right.status == NOT_STARTED:
            # keep track of start time/frame for later
            condition_txt_2_right.tStart = t
            condition_txt_2_right.frameNStart = frameN  # exact frame index
            condition_txt_2_right.setAutoDraw(True)
        frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if condition_txt_2_right.status == STARTED and t >= frameRemains:
            condition_txt_2_right.setAutoDraw(False)
        #if mouse.isPressedIn(machine2_1):
        #    not_active1.pos = [-0.45, 0]
        #    schedule.type = 'RPI'
        #    schedule.parameter = 6
        
        #if mouse.isPressedIn(machine1):
        #    not_active1.pos = [0, 0]
        #    schedule.type = 'RR'
        #    schedule.parameter = 7
        
        if schedule.type == 'Delay' and len(reinf_times_delay)>0:
            if t >= reinf_times_delay[0]: # give delayed reinforcer
                reward_to_screen()
                reinf_times_delay.pop(0) # drop first reinf time
                wasRnf.append(1)
                response_2.keys.append('None')
                response_2.rt.append(t)
                nReinf += 1
                n_resp_since_last_rnf = 0 #reset this to start counting again
        #think about how to save the inter reinforcement intervals when delivering delayed rewards
        #            if len(response_2.rt)>1:        
        #                irt.append(response_2.rt[-1]-response_2.rt[-2])
        #            else:
        #                irt.append(response_2.rt[-1]) 
                writer_object1.writerow([expInfo['session'], expInfo['participant'], response_2.keys[-1], response_2.rt[-1], trial, nResp, background_colour[:-4], company1, company2, devalued_company])
        #    except:
        #        pass
        
        if len(reinf_times) > 1:
            tSinceLastRnf = t-reinf_times[-1]
        
        # this is the tick for the RI and RI+ schedules
        if not shouldBeReinforced and tickClock.getTime() <= 0:
            shouldBeReinforced = np.random.binomial(1, 0.2)
            tickClock.reset()
        
        #this_IRT = t - response_2.rt[-1] if nResp > 0 else t # current IRT
        
        if len(theseKeys)>0 and DebounceTimer.getTime() < 0:
            coin.play()    
            nResp += 1
            print("Resp:%i")%nResp
        
            if response_2.keys[-1] == 'a':
                button_pressed.pos = (-0.5, -0.2)
            else:
                button_pressed.pos = (0.5, -0.2)
            DebounceTimer.reset() # re-start debounce timer 
        
            img_clock = core.Clock() # clock to show img for a n of sec
            while img_clock.getTime() < 0.10: # draw button pressed 
                if response_2.keys[-1] == 'a':
                    button_image1_2.setAutoDraw(False)
                else:
                    button_image2_2.setAutoDraw(False)
                button_pressed.draw()
                win.flip()
                button_image1_2.setAutoDraw(True)
                button_image2_2.setAutoDraw(True)
        
            n_resp_since_last_rnf += 1
            credits -= int(expInfo['cost_responding'])
            #schedule.giveRnf(response_2.rt[-1]) # erased for extinction
        
            if len(response_2.rt)>1:        
                irt.append(response_2.rt[-1]-response_2.rt[-2])
            else:
                irt.append(response_2.rt[-1]) 
            # write to csv on each frame in which there is a response_2
            try:
                writer_object1.writerow([expInfo['session'], expInfo['participant'], response_2.keys[-1], response_2.rt[-1], trial, nResp, background_colour[:-4], company1, company2, devalued_company])
            except:
                pass
            
        
        # this is just to debug
        credits_txt = visual.TextStim(win, text=str(int(credits)), pos=(0.0, 0.65), color=u'black')
        #credits_txt.draw() # don't show this on this extinction test
        
        # this should be part of debug function; shows n of reinf and resp so far
        #this_IRT_txt =  visual.TextStim(win, text=str(int(this_IRT)), pos=(-0.8, 0.35), color=u'black')
        #nResp_txt = visual.TextStim(win, text=str(int(nResp)), pos=(0.8, 0.35), color=u'black')
        #nReinf_txt = visual.TextStim(win, text=str(int(nReinf)), pos=(0.8, 0.35), color=u'black')
        #this_IRT.draw()
        #nResp_txt.draw()
        #nReinf_txt.draw()
        
        if debugging:
            show_debugging_stuff()
        
        #if timer.getTime() <= 0:
        #    continueRoutine=False
        
        if timer.getTime() <= 0 or credits >= credits_to_win:
            continueRoutine=False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in training_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "training_2"-------
    for thisComponent in training_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if response_2.keys in ['', [], None]:  # No response was made
        response_2.keys=None
    devaluation_test.addData('response_2.keys',response_2.keys)
    if response_2.keys != None:  # we had a response
        devaluation_test.addData('response_2.rt', response_2.rt)
    #intervalToRnf = scheduleParameter[1]# + np.random.permutation(limit)[0]
    
    #nResp = len(response_training.rt)
    #nReinf = len(reinf_times) 
    
    print("nResp: %f")%nResp
    print("nReinf: %f")%nReinf
    
    # deleted this chunk because this trial is on extinction so no rnfProb
    #if len(response_2.rt)>=1:
    #    rnfProb1.append(nReinf/nResp)
    #else: 
    #    rnfProb1.append(0) # if no responses, add zero
    #print("rnfProb: %f")%rnfProb1[-1]
    
    
    if response_2.keys != None:  # we had a response
        thisExp.addData('reinf_times', reinf_times)
        thisExp.addData('wasRnf', wasRnf)
        thisExp.addData('irts', irt)
        thisExp.addData('mean_irt', np.mean(irt))
        #thisExp.addData('rnf_prob', rnfProb1)
        thisExp.nextEntry()
    
    core.wait(2)
    
    trial += 1
    
    # the Routine "training_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'devaluation_test'


# set up handler to look after randomisation of conditions etc
trials_contingency_test = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(expInfo['condition']+'.xlsx'),
    seed=None, name='trials_contingency_test')
thisExp.addLoop(trials_contingency_test)  # add the loop to the experiment
thisTrials_contingency_test = trials_contingency_test.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrials_contingency_test.rgb)
if thisTrials_contingency_test != None:
    for paramName in thisTrials_contingency_test.keys():
        exec(paramName + '= thisTrials_contingency_test.' + paramName)

for thisTrials_contingency_test in trials_contingency_test:
    currentLoop = trials_contingency_test
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_contingency_test.rgb)
    if thisTrials_contingency_test != None:
        for paramName in thisTrials_contingency_test.keys():
            exec(paramName + '= thisTrials_contingency_test.' + paramName)
    
    # ------Prepare to start Routine "contingency_tests"-------
    t = 0
    contingency_testsClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    background_contingency_test.setImage(background_colour)
    contingency_question_txt.setText('Please press the button that gave you a share of this company in this city: ')
    company_name_txt.setText(company1)
    key_resp_contingency_test = event.BuilderKeyResponse()
    # keep track of which components have finished
    contingency_testsComponents = [background_contingency_test, contingency_question_txt, company_name_txt, key_resp_contingency_test]
    for thisComponent in contingency_testsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "contingency_tests"-------
    while continueRoutine:
        # get current time
        t = contingency_testsClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background_contingency_test* updates
        if t >= 0.0 and background_contingency_test.status == NOT_STARTED:
            # keep track of start time/frame for later
            background_contingency_test.tStart = t
            background_contingency_test.frameNStart = frameN  # exact frame index
            background_contingency_test.setAutoDraw(True)
        
        # *contingency_question_txt* updates
        if t >= 0.0 and contingency_question_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            contingency_question_txt.tStart = t
            contingency_question_txt.frameNStart = frameN  # exact frame index
            contingency_question_txt.setAutoDraw(True)
        
        # *company_name_txt* updates
        if t >= 0.0 and company_name_txt.status == NOT_STARTED:
            # keep track of start time/frame for later
            company_name_txt.tStart = t
            company_name_txt.frameNStart = frameN  # exact frame index
            company_name_txt.setAutoDraw(True)
        
        # *key_resp_contingency_test* updates
        if t >= 0.0 and key_resp_contingency_test.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_contingency_test.tStart = t
            key_resp_contingency_test.frameNStart = frameN  # exact frame index
            key_resp_contingency_test.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_contingency_test.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_contingency_test.status == STARTED:
            theseKeys = event.getKeys(keyList=['a', 'l'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_contingency_test.keys = theseKeys[-1]  # just the last key pressed
                key_resp_contingency_test.rt = key_resp_contingency_test.clock.getTime()
                # was this 'correct'?
                if (key_resp_contingency_test.keys == str(company1)) or (key_resp_contingency_test.keys == company1):
                    key_resp_contingency_test.corr = 1
                else:
                    key_resp_contingency_test.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in contingency_testsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "contingency_tests"-------
    for thisComponent in contingency_testsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_contingency_test.keys in ['', [], None]:  # No response was made
        key_resp_contingency_test.keys=None
        # was no response the correct answer?!
        if str(company1).lower() == 'none':
           key_resp_contingency_test.corr = 1  # correct non-response
        else:
           key_resp_contingency_test.corr = 0  # failed to respond (incorrectly)
    # store data for trials_contingency_test (TrialHandler)
    trials_contingency_test.addData('key_resp_contingency_test.keys',key_resp_contingency_test.keys)
    trials_contingency_test.addData('key_resp_contingency_test.corr', key_resp_contingency_test.corr)
    if key_resp_contingency_test.keys != None:  # we had a response
        trials_contingency_test.addData('key_resp_contingency_test.rt', key_resp_contingency_test.rt)
    # the Routine "contingency_tests" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "contingency_tests2"-------
    t = 0
    contingency_tests2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    background_contingency_test2.setImage(background_colour)
    company_name_txt2.setText(company2)
    key_resp_contingency_test2 = event.BuilderKeyResponse()
    # keep track of which components have finished
    contingency_tests2Components = [background_contingency_test2, contingency_question_txt2, company_name_txt2, key_resp_contingency_test2]
    for thisComponent in contingency_tests2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "contingency_tests2"-------
    while continueRoutine:
        # get current time
        t = contingency_tests2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background_contingency_test2* updates
        if t >= 0.0 and background_contingency_test2.status == NOT_STARTED:
            # keep track of start time/frame for later
            background_contingency_test2.tStart = t
            background_contingency_test2.frameNStart = frameN  # exact frame index
            background_contingency_test2.setAutoDraw(True)
        
        # *contingency_question_txt2* updates
        if t >= 0.0 and contingency_question_txt2.status == NOT_STARTED:
            # keep track of start time/frame for later
            contingency_question_txt2.tStart = t
            contingency_question_txt2.frameNStart = frameN  # exact frame index
            contingency_question_txt2.setAutoDraw(True)
        
        # *company_name_txt2* updates
        if t >= 0.0 and company_name_txt2.status == NOT_STARTED:
            # keep track of start time/frame for later
            company_name_txt2.tStart = t
            company_name_txt2.frameNStart = frameN  # exact frame index
            company_name_txt2.setAutoDraw(True)
        
        # *key_resp_contingency_test2* updates
        if t >= 0.0 and key_resp_contingency_test2.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_contingency_test2.tStart = t
            key_resp_contingency_test2.frameNStart = frameN  # exact frame index
            key_resp_contingency_test2.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_contingency_test2.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_contingency_test2.status == STARTED:
            theseKeys = event.getKeys(keyList=['a', 'l'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_contingency_test2.keys = theseKeys[-1]  # just the last key pressed
                key_resp_contingency_test2.rt = key_resp_contingency_test2.clock.getTime()
                # was this 'correct'?
                if (key_resp_contingency_test2.keys == str(company2)) or (key_resp_contingency_test2.keys == company2):
                    key_resp_contingency_test2.corr = 1
                else:
                    key_resp_contingency_test2.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in contingency_tests2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "contingency_tests2"-------
    for thisComponent in contingency_tests2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_contingency_test2.keys in ['', [], None]:  # No response was made
        key_resp_contingency_test2.keys=None
        # was no response the correct answer?!
        if str(company2).lower() == 'none':
           key_resp_contingency_test2.corr = 1  # correct non-response
        else:
           key_resp_contingency_test2.corr = 0  # failed to respond (incorrectly)
    # store data for trials_contingency_test (TrialHandler)
    trials_contingency_test.addData('key_resp_contingency_test2.keys',key_resp_contingency_test2.keys)
    trials_contingency_test.addData('key_resp_contingency_test2.corr', key_resp_contingency_test2.corr)
    if key_resp_contingency_test2.keys != None:  # we had a response
        trials_contingency_test.addData('key_resp_contingency_test2.rt', key_resp_contingency_test2.rt)
    # the Routine "contingency_tests2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials_contingency_test'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
thanksComponents = [thanks1, key_resp_2, expFinished, finishedSound]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thanks1* updates
    if t >= 0.0 and thanks1.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanks1.tStart = t
        thanks1.frameNStart = frameN  # exact frame index
        thanks1.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['f'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_2.keys = theseKeys[-1]  # just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # *expFinished* updates
    if t >= 0.0 and expFinished.status == NOT_STARTED:
        # keep track of start time/frame for later
        expFinished.tStart = t
        expFinished.frameNStart = frameN  # exact frame index
        expFinished.setAutoDraw(True)
    frameRemains = 0.0 + 0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if expFinished.status == STARTED and t >= frameRemains:
        expFinished.setAutoDraw(False)
    # start/stop finishedSound
    if t >= 0.0 and finishedSound.status == NOT_STARTED:
        # keep track of start time/frame for later
        finishedSound.tStart = t
        finishedSound.frameNStart = frameN  # exact frame index
        finishedSound.play()  # start the sound (it finishes automatically)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_2.keys in ['', [], None]:  # No response was made
    key_resp_2.keys=None
thisExp.addData('key_resp_2.keys',key_resp_2.keys)
if key_resp_2.keys != None:  # we had a response
    thisExp.addData('key_resp_2.rt', key_resp_2.rt)
thisExp.nextEntry()
finishedSound.stop()  # ensure sound has stopped at end of routine
# the Routine "thanks" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


csv_file.close()

csv_file1.close()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
