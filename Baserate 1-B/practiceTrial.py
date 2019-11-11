import common, time, config, random
from psychopy import visual, core, event

#Only used for practice trials
textIntro = u'Welcome, 6 practice trials await. \n When ready press: Enter'
textStudyContains = u'This study contains:'
textPersonIs = u'The person is:'
textThereAre = u'There are:'
textLikelyToBe = u'Is the person more likely to be:'
textNextTrail = u'Next trial, please pay attention:'

def practicetrial(window, workBook):
    
    instruction1 = visual.TextStim(window, text = textIntro, font = 'Arial', units = 'norm', pos=[0,0], height=0.10, wrapWidth=None)
    instruction1.draw()
    window.flip()
    common.waitforconfirm()
    
    time.sleep(0.5)
    common.fixationCross("small", 1, 0, window)
    
    for runNumber in range(1,7): #1-6
    #for runNumber in range(6,7):
        testpractice(window,textStudyContains, textPersonIs, textThereAre, textLikelyToBe, runNumber, workBook)

def testpractice(window, textStudyContains, textPersonIs, textThereAre, textLikelyToBe, run_number, workBook):
    #start at practice trial 1, end at 6, which is the run_number
    timer = core.Clock()
    
    value_dict = {"Profession1": "", "Profession2": "", "Attribute": "", 
    "Baserate1": "", "Baserate2": "", "Answeroption1": "", "Answeroption2": "",
    "Correct": ""} 
    
    #Fetch values from excel
    for column in range (3, 11): #3-10, Profession1 - > Correct
        row_name = workBook.cell(row = 1, column = column) #Profession1 - > Correct
        cell_name = workBook.cell(row = run_number + 1, column = column) #Americans -> Answeroption1/2
        value_dict[row_name.value] = cell_name.value
            
    #Added if tests to remove text after iterations
    if (run_number > 1 and run_number < 6):
        textLikelyToBe = "?"
        
    if (run_number > 2):
        textThereAre = ""
        if (run_number > 3):
            textPersonIs = ""
            if (run_number == 6):
                textPersonIs = ""
                textThereAre = ""
                textLikelyToBe = ""
    
    common.fixationCross("small", 1, 0, window)
    
    #Professions:
    frame1 = visual.TextStim(window, text = textStudyContains, font = 'Arial', units = 'norm', pos = [0, 0.5], height = 0.07, wrapWidth=None)
    frame1_profession1 = visual.TextStim(window, text = value_dict['Profession1'], font = 'Arial', units = 'norm', pos =  [0.25, 0.2], height = 0.07, wrapWidth=None)
    frame1_and = visual.TextStim(window, text = "and", font = 'Arial', units = 'norm', pos =  [0, 0.2], height = 0.07, wrapWidth=None)
    frame1_profession2 = visual.TextStim(window, text = value_dict['Profession2'], font = 'Arial', units = 'norm', pos =  [-0.25, 0.2], height = 0.07, wrapWidth=None)
    frames_list = [frame1, frame1_profession1, frame1_and, frame1_profession2]

    for frames in frames_list:
        frames.draw()

    window.flip()
    time.sleep(1.8)
    
    common.fixationCross("small", 1, 0, window)
    
    #Attribute:
    frame2 = visual.TextStim(window, text = textPersonIs, font = 'Arial', units = 'norm', pos = [0, 0.5], height = 0.07, wrapWidth=None)
    frame2_attribute = visual.TextStim(window, text = value_dict['Attribute'], font = 'Arial', units = 'norm', pos = [0,0], height = 0.07, wrapWidth=None)
    
    frame2.draw()
    frame2_attribute.draw()
    window.flip()
    time.sleep(1.799)

    common.fixationCross("small", 1, 0, window)

    #Frame 3 
    frame3 = visual.TextStim(window, text = textThereAre, font = 'Arial', units = 'norm', pos = [0, 0.5], height = 0.07, wrapWidth=None)
    frame3_baserate1 = visual.TextStim(window, text = value_dict['Baserate1'], font = 'Arial', units = 'norm', pos = [0.25, -0.2], height = 0.07, wrapWidth=None)
    frame3_baserate2 = visual.TextStim(window, text = value_dict['Baserate2'], font = 'Arial', units = 'norm', pos = [-0.25, -0.2], height = 0.07, wrapWidth=None)
    frame1_profession1.pos = [0.25, 0.2]
    frame1_profession2.pos = [-0.25, 0.2]

    if run_number == 1:

        textTutorial_1 = u'This part will only be displayed once, so make sure you understand before moving on:'
        textTutorial_2 = u'The user has to chose between left and right, and can do that by using '+ config.answer_left + ' or ' + config.answer_right +", try it out, and press enter when you are ready to move on to the next 5 practice trials"

        box_left = visual.ImageStim(window, image = config.left_image, units = "pix", pos = (-0.28 * 1000, -0.05 *1000))
        box_right = visual.ImageStim(window, image = config.right_image, units = "pix", pos = (0.28 * 1000, -0.05 * 1000))
        
        frame_tut1 = visual.TextStim(window, text = textTutorial_1, font = 'Arial', units = 'norm', pos = [0, 0.7], height = 0.07, wrapWidth=None)
        frame_tut2 = visual.TextStim(window, text = textTutorial_2, font = 'Arial', units = 'norm', pos = [0, -0.7], height = 0.07, wrapWidth=None)

        frames_list = [frame3, frame3_baserate1, frame3_baserate2, frame1_profession1, frame1_profession2, frame_tut1, frame_tut2]

        for frame in frames_list:
            frame.draw()

        window.flip()

        while 1:
            keys=event.getKeys()
            if config.answer_left in keys:
                window.flip()
                for frame in frames_list:
                    frame.draw()
                box_left.draw()
                window.flip()
            elif config.answer_right in keys:
                window.flip()
                for frame in frames_list:
                    frame.draw()
                box_right.draw()
                window.flip()
            elif config.key_confirm in keys:
                break
            
    else:
        frames_list = [frame3, frame3_baserate1, frame3_baserate2, frame1_profession1, frame1_profession2]

        for frame in frames_list:
            frame.draw()
        
        window.flip()

        timer.reset()
        startTime = timer.getTime()

        event.clearEvents()
        #max 4 seconds to respond
        while (startTime < 4):
            keys=event.getKeys()
            if (config.answer_left) in keys:
                break
            elif (config.answer_right) in keys:
                break
            core.wait(0.1)
            startTime += 0.1
    
    window.flip()
    time.sleep(2)
    
    #NEXT TRIAL

    if run_number < 6:
        frame5 = visual.TextStim(window, text = textNextTrail, font = 'Arial', units = 'norm', pos = [0,0], height = 0.10, wrapWidth=None)
        frame5.draw()
        window.flip()

    time.sleep(2)
    