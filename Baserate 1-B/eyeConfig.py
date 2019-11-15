from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
import pylink, config, common, os
from psychopy import visual

def eyetrackersetup(tk, window):
    genv = EyeLinkCoreGraphicsPsychoPy(tk, window)
    pylink.openGraphicsEx(genv)
    
    tk.setOfflineMode()
    tk.sendCommand('sample_rate 500')
    tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (config.scnWidth-1, config.scnHeigth-1))
    tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (config.scnWidth-1, config.scnHeigth-1))

    # specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
    tk.sendCommand("calibration_type = HV9") # tk.setCalibrationType('HV9') also works, see the Pylink manual

    # specify the proportion of subject display to calibrate/validate (OPTIONAL, useful for wide screen monitors)
    # tk.sendCommand("calibration_area_proportion 0.85 0.83")
    # tk.sendCommand("validation_area_proportion  0.85 0.83")

    # Using a button from the EyeLink Host PC gamepad to accept calibration/dirft check target (optional)
    # tk.sendCommand("button_function 5 'accept_target_fixation'")

    # the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (100/1000Plus/DUO)
    eyelinkVer = tk.getTrackerVersion()

    # turn off scenelink camera stuff (EyeLink II/I only)
    if eyelinkVer == 2: tk.sendCommand("scene_camera_gazemap = NO")

    # Set the tracker to parse Events using "GAZE" (or "HREF") data
    tk.sendCommand("recording_parse_type = GAZE")

    # Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
    # the Parser for EyeLink I is more conservative, see below
    # [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
    if eyelinkVer>=2: tk.sendCommand('select_parser_configuration 0')

    # get Host tracking software version
    hostVer = 0
    if eyelinkVer == 3:
        tvstr  = tk.getTrackerVersionString()
        vindex = tvstr.find("EYELINK CL")
        hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

    # specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
    # See Section 4 Data Files of the EyeLink user manual
    tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
    tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
    if hostVer>=4: 
        tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
        tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
    else: #Add pupil         
        tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
        tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

    return tk

def eyeCalibration(dummyMode, tk, window):

    msg = visual.TextStim(window, text = "Press ENTER for calibration")
    msg.draw()
    window.flip()

    if not dummyMode:
        common.waitforconfirm()
        tk.doTrackerSetup()

def eyeConfigFile(expInfo):
    dataFolder = os.getcwd() + "/edfData/"
    if not os.path.exists(dataFolder): os.makedirs(dataFolder)
	
	#Name for Eyedata
    dataFileName = expInfo['SubjectNO'] + '.EDF'
    print(dataFileName)
    return dataFileName

def eyeRecording(eyeTracker, dummyMode):

    if not dummyMode:
        eyeTracker.startRecording(1,1,1,1)
        # pylink.pumpDelay(100) # wait for 100 ms to make sure data of interest is recorded - commented because: necessary if we start recording with training?

        #determine which eye(s) are available
        eyeTracked = eyeTracker.eyeAvailable() 
        if eyeTracked==2: eyeTracked = 1

        eyeTracker.sendMessage("task_start")

def eyeQuitRecording(eyeTracker, dataFileName):
    eyeTracker.setOfflineMode()
    eyeTracker.closeDataFile()
    pylink.pumpDelay(50)

    eyeTracker.receiveDataFile(dataFileName, dataFileName + ".EDF")
    eyeTracker.close()

