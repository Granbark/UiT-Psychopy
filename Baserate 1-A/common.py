#common methods
import config, time, random
from psychopy import event, monitors, visual, gui, core

"""Wait for Enter"""
def waitforconfirm():
   
    while 1:
        keys=event.getKeys()
        if config.key_confirm in keys:
            waitforconfirm.confirmed=True
            break
        else:
            continue

""" 
Returns a psychopy visual window, with settings from config file
"""
def setupMonitor():
    
    monitor = monitors.Monitor('display_name', width=53.0, distance=70.0) #width, dist?
    monitor.saveMon()
    monitor.setSizePix((config.scnWidth, config.scnHeigth))
    window = visual.Window((config.scnWidth, config.scnHeigth), fullscr=True, monitor = monitor, color=[0,0,0], 
                            colorSpace='rgb', units='pix', allowStencil=True,autoLog=False, useFBO=True)
    window.mouseVisible = False
    return window

"""Register user values, and return a dict with the values"""
def registerUser(use_gui):
    if use_gui:
        dlg = gui.DlgFromDict(dictionary=config.expInfo, title="Task-1", order=['SubjectNO', 'SubjectInitials'])
        if dlg.OK == False: core.quit()  # user pressed cancel
    else:
        config.expInfo['SubjectNO'] = input('Subject # (1-99): ') #raw_input()? Not working atm
        config.expInfo['SubjectInitials'] = input('Subject Initials (e.g., WZ): ') #raw_input()? Not working atm  
    return dlg #return config.userInfo

def fixationCross(size, randSelect, time_input, window): #can add a time here, so we can manually select a time for each fix_cross?

    fixation_display = visual.ImageStim(win = window, image = config.fixation_image, pos = [0,0], units = "pix")
    size_x = fixation_display.size[0]
    size_y = fixation_display.size[1]
    
    if size == "large":
        fixation_display.size = [size_x * 1, size_y * 1]
        fixation_display.draw()
    else: #"small" or default
        fixation_display.size = [size_x * 0.45, size_y * 0.45]
        fixation_display.draw()
    
    window.flip()

    if  randSelect == 1:
        time_jitter = random.uniform(0.5, 1.7)
        time.sleep(time_jitter)
    else:
        time_sleep = time_input
        time.sleep(time_sleep)
