from psychopy import visual, core, event, monitors, data, gui
import eyeConfig, config, common, pylink, excelConfig, practiceTrial, mainTrial
from openpyxl import Workbook, load_workbook

dummyMode = True #True/False. True = No eyetracker, False = eyetracker 

class Experiment():

    def __init__(self):
        self.userInfo = config.expInfo
        self.baseRates = excelConfig.excelBaseRates()
        self.subjectExcel = excelConfig.excelNewSubject(self.userInfo)
        self.edfFile = eyeConfig.eyeConfigFile(self.userInfo)

    def eyeConfig(self):
        #Establish a connection to the eyetracker
        if not dummyMode:
            tk = pylink.EyeLink('100.1.1.1')
            self.eyeTracker = eyeConfig.eyetrackersetup(tk, self.monitor) #Not calibration, eye_tracker = tk
            eyeConfig.eyeCalibration(dummyMode, self.eyeTracker, self.monitor) #Calibration
            self.eyeTracker.openDataFile(self.edfFile)
        else:
            tk = pylink.EyeLink(None)
            self.eyeTracker = tk

    def monitorConfig(self):
        self.monitor = common.setupMonitor()

    def startRecording(self):
        eyeConfig.eyeRecording(self.eyeTracker, dummyMode)
    
    def saveData(self):
        eyeConfig.eyeQuitRecording(self.eyeTracker, self.userInfo["SubjectNO"], self.edfFile + self.userInfo["SubjectNO"])

    def practiceTrial(self):
        practiceTrial.practicetrial(self.monitor, self.baseRates)

    def Trial(self):
        mainTrial.runTrial(self.baseRates, self.monitor, self.subjectExcel, self.eyeTracker)

#When you run the file:
if __name__ == "__main__":
    task1 = Experiment() #create an experiment

    task1.userInfo = common.registerUser(config.useGUI) #Inital info-box with subjectNUM and INITALS
    task1.monitorConfig()
    task1.eyeConfig() #set up eyetracker, with calibration, and open the datafile

    while 1:
        msg = visual.TextStim(task1.monitor, text = "Press ENTER for practice trial, T for Trials")
        msg.draw()
        task1.monitor.flip()
        event.clearEvents()
        while 1:
            key = event.getKeys()
            if config.key_confirm in key:
                task1.practiceTrial()
                break
            elif "t" in key:
                task1.startRecording()
                task1.Trial()
                task1.saveData()
                quit
            else:
                continue
