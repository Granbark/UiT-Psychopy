from psychopy.sound import Sound
from psychopy import visual, core, event
import soundfile as sf
import sounddevice as sd
import common, time, config, os, random

#Only used for practice trials
textIntro = u'Welcome, 3 practice trials await. \n When ready press: Enter'
textStudyContains = u'This study contains:'
textPersonIs = u'The person is:'
textThereAre = u'There are:'
textLikelyToBe = u'Is the person more likely to be:'
textNextTrail = u'Next trial, please pay attention:'

def call_frame(call_name, frame_name, window):
    frame_dict = {
        "Profession1":  visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos =  [-0.25, 0.2], height = 0.07, wrapWidth=None),
        "Profession2":  visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos =  [0.25, 0.2], height = 0.07, wrapWidth=None),
        "Attribute":    visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos = [0,0], height = 0.07, wrapWidth=None),
        "Baserate1":    visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos = [-0.25, -0.2], height = 0.07, wrapWidth=None), 
        "Baserate2":    visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos = [0.25, -0.2], height = 0.07, wrapWidth=None),
        "Answeroption1":visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos = [-0.3, 0], height = 0.07, wrapWidth=None),
        "Answeroption2":visual.TextStim(window, text = call_name, font = 'Arial', units = 'norm', pos = [0.3, 0], height = 0.07, wrapWidth=None)
        }
    #if we call the function with the right name, we return the visual stimuli
    if frame_name in frame_dict:
        return frame_dict[frame_name]

def practiceTrial(window, workBook, audioDevice):
    
    instruction1 = visual.TextStim(window, text = textIntro, font = 'Arial', units = 'norm', pos=[0,0], height=0.10, wrapWidth=None)
    instruction1.draw()
    window.flip()
    common.waitforconfirm()
    
    time.sleep(0.5)
    common.fixationCross("large", 1, 0, window)
    window.flip()
    
    for runNumber in range(1,4): #1,2,3
        testPratice(window, workBook, runNumber, audioDevice)

def testPratice(window, workBook, runNumber, audioDevice):
    timer = core.Clock()

    value_dict = {"Trial": "", "Condition": "", "Profession1": "", "Profession2": "", "Attribute": "", 
    "Baserate1": "", "Baserate2": "", "Answeroption1": "", "Answeroption2": "",
    "Correct": "", "wav_profession": ""} 
    
    for column in range (1, 12): #1-11, Trial - > Correct

        row_name = workBook.cell(row = 1, column = column) #Condition - > Correct answer
        cell_name = workBook.cell(row = runNumber + 1, column = column) #Americans -> Answeroption1/2
        value_dict[row_name.value] = cell_name.value #set value from excel file to dictionary
    
    likely_sound, likely_fs = sf.read("is_this_person_more_likely_a.wav")
    attribute_sound = value_dict["Attribute"] + ".wav"
    profession_sound = value_dict["wav_profession"]

    audio_folder = os.getcwd() + "\\audio_files"

    original_folder = os.getcwd()

    os.chdir(audio_folder)
    attribute_sound, attribute_fs = sf.read(attribute_sound)
    profession_sound, profession_fs = sf.read(profession_sound)

    os.chdir(original_folder)
    
    #Study contains
    frame1_studyContains = visual.TextStim(window, text = textStudyContains, font = 'Arial', units = 'norm', pos = [0, 0.5], height = 0.07, wrapWidth=None)
    frame1_profession1 = call_frame(value_dict["Profession1"], "Profession1", window)
    frame1_profession2 = call_frame(value_dict["Profession2"], "Profession2", window)
    
    frames_list = [frame1_studyContains, frame1_profession1, frame1_profession2]
    for frame in frames_list:
        frame.draw()
    
    window.flip()
    time.sleep(1.8)

    common.fixationCross("large", 1, 0, window)

    #Baserates
    frame2 = visual.TextStim(window, text = textThereAre, font = 'Arial', units = 'norm', pos = [0, 0.5], height = 0.07, wrapWidth=None)
    if runNumber > 2:
        frame2.text = " "

    frame2_baserate1 = call_frame(value_dict["Baserate1"], "Baserate1", window)
    frame2_baserate2 = call_frame(value_dict["Baserate2"], "Baserate2", window)

    frames_list = [frame2, frame2_baserate1, frame2_baserate2, frame1_profession1, frame1_profession2]
    for frame in frames_list:
        frame.draw()
    
    window.flip()
    time.sleep(3.6) #3.6?

    sd.play(attribute_sound, attribute_fs, device = audioDevice)

    common.fixationCross("large", 0, 3, window)

    window.flip()
    time.sleep(0.2)

    sd.play(likely_sound, likely_fs, device = audioDevice)

    common.fixationCross("large", 0, 3, window)
    sd.wait()
    sd.play(profession_sound, profession_fs, device = audioDevice)
    time.sleep(1.2) 

    if runNumber == 1:
        textTutorial_1 = u'This part will only be displayed once, so make sure you understand before moving on:'
        textTutorial_2 = u'The user has to chose between YES and NO, and can do that by using ' + config.answer_left + ' for YES or ' + config.answer_right+ ' for NO. If understood, press ' + 'ENTER' + ' to continue '

        frame_tut1 = visual.TextStim(window, text = textTutorial_1, font = 'Arial', units = 'norm', pos = [0, 0.7], height = 0.07, wrapWidth=None)
        frame_tut2 = visual.TextStim(window, text = textTutorial_2, font = 'Arial', units = 'norm', pos = [0, -0.7], height = 0.07, wrapWidth=None)

        frame_tut1.draw()
        frame_tut2.draw()
        window.flip()
        common.waitforconfirm()
    
    else: 
        timer.reset()
        startTime = timer.getTime()
        event.clearEvents()

        while (startTime < 4):
            keys = event.getKeys()

            if (config.answer_left) in keys:
                break
            elif (config.answer_right) in keys:
                break
        
            core.wait(0.1)
            startTime += 0.1

        if startTime > 4:
            return
    
    time_jitter = random.uniform(3,5)
    common.fixationCross("large", 0, time_jitter, window)

    window.flip()
    time.sleep(random.uniform(1,2.5))
