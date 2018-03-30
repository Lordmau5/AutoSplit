import sys
import os
import pymouse
import time
import keyboard
import numpy as np
import mss
import threading
from PIL import Image
from PIL import ImageChops
from PIL import ImageGrab
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMouseEvent
from PyQt4 import QtTest

#initial values
split_image_directory='No Folder Selected'
x1='none'
y1='none'
x2='none'
y2='none'
split_hotkey='none'
reset_hotkey='none'
undo_split_hotkey='none'
skip_split_hotkey='none'
mean_percent_diff=100
mean_percent_diff_threshold=10
pause=10


class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(440,420)
        self.setWindowTitle("Auto Splitter")
        self.statusBar()
        self.home()
        
    #all buttons, labels, lineedits in the window.
    def home(self):
        global split_image_directory
        global split_image_path
        global x1,y1,x2,y2
        global mean_percent_diff_threshold
        global FilePathLine
        global TopLeftLabel
        global TopLeftButton
        global BottomRightLabel
        global BottomRightButton
        global split_hotkey
        global reset_hotkey
        global undo_split_hotkey
        global skip_split_hotkey
        global SplitHotkeyLine
        global ResetHotkeyLine
        global CheckFPSLabel
        global CheckFPSButton
        global CurrentSplitImageLabel
        global StartAutoSplitterButton
        global SplitHotkeyButton
        global ResetHotkeyButton
        global BrowseButton
        global ShowLivePercentDifferenceLabel
        global CheckBox
        global UndoHotkeyButton
        global UndoHotkeyLine
        global UndoHotkeyLabel
        global SkipHotkeyButton
        global SkipHotkeyLine
        global SkipHotkeyLabel
        global ThresholdDropdown
        global PauseDropdown
        #SPLIT IMAGE FOLDER
        
        FilePathLabel=QtGui.QLabel('Split Image Folder:', self)
        FilePathLabel.move(10,20)
        
        FilePathLine=QtGui.QLineEdit(split_image_directory,self)
        FilePathLine.move(110,23)
        FilePathLine.resize(200,25)
        FilePathLine.setReadOnly(True)
        
        BrowseButton = QtGui.QPushButton("Browse..",self)
        BrowseButton.clicked.connect(self.browse)
        BrowseButton.move(320,20)
        
        #GAME REGION
        
        GameRegionLabel=QtGui.QLabel('------------------ Game Screen Region --------------------', self)
        GameRegionLabel.move(93,60)
        GameRegionLabel.resize(250,30)
        
        TopLeftLabel=QtGui.QLabel('Top Left Coordinates:'+'                         '+x1+', '+y1, self)
        TopLeftLabel.move(10,90)
        TopLeftLabel.resize(250,20)
        
        TopLeftButton=QtGui.QPushButton("Set Top Left",self)
        TopLeftButton.clicked.connect(self.set_top_left)
        TopLeftButton.move(320,90)
        TopLeftButton.resize(100,20)
        
        BottomRightLabel=QtGui.QLabel('Bottom Right Coordinates:'+'                 '+x2+', '+y2, self)
        BottomRightLabel.move(10,110)
        BottomRightLabel.resize(250,20)
        
        BottomRightButton=QtGui.QPushButton("Set Bottom Right",self)
        BottomRightButton.clicked.connect(self.set_bottom_right)
        BottomRightButton.move(320,110)
        BottomRightButton.resize(100,20)
        
        #HOTKEYS
        HotkeysLabel=QtGui.QLabel('--------------------- Timer Hotkeys ----------------------', self)
        HotkeysLabel.move(94,140)
        HotkeysLabel.resize(250,30)
        
        SplitHotkeyLabel=QtGui.QLabel('Split:', self)
        SplitHotkeyLabel.move(10,165)
        
        SplitHotkeyLine=QtGui.QLineEdit(split_hotkey,self)
        SplitHotkeyLine.move(167,170)
        SplitHotkeyLine.resize(95,20)
        SplitHotkeyLine.setReadOnly(True)
        
        SplitHotkeyButton=QtGui.QPushButton("Set Hotkey",self)
        SplitHotkeyButton.clicked.connect(self.set_split_hotkey)
        SplitHotkeyButton.move(320,170)
        SplitHotkeyButton.resize(100,20)
        
        ResetHotkeyLabel=QtGui.QLabel('Reset:', self)
        ResetHotkeyLabel.move(10,190)
        
        ResetHotkeyLine=QtGui.QLineEdit(reset_hotkey,self)
        ResetHotkeyLine.move(167,195)
        ResetHotkeyLine.resize(95,20)
        ResetHotkeyLine.setReadOnly(True)
        
        ResetHotkeyButton=QtGui.QPushButton("Set Hotkey",self)
        ResetHotkeyButton.clicked.connect(self.set_reset_hotkey)
        ResetHotkeyButton.move(320,195)
        ResetHotkeyButton.resize(100,20)
        
        UndoHotkeyLabel=QtGui.QLabel('Undo Split:', self)
        UndoHotkeyLabel.move(10,215)
        
        UndoHotkeyLine=QtGui.QLineEdit(undo_split_hotkey,self)
        UndoHotkeyLine.move(167,220)
        UndoHotkeyLine.resize(95,20)
        UndoHotkeyLine.setReadOnly(True)
        
        UndoHotkeyButton=QtGui.QPushButton("Set Hotkey",self)
        UndoHotkeyButton.clicked.connect(self.set_undo_hotkey)
        UndoHotkeyButton.move(320,220)
        UndoHotkeyButton.resize(100,20)
        
        SkipHotkeyLabel=QtGui.QLabel('Skip Split:', self)
        SkipHotkeyLabel.move(10,240)
        
        SkipHotkeyLine=QtGui.QLineEdit(skip_split_hotkey,self)
        SkipHotkeyLine.move(167,245)
        SkipHotkeyLine.resize(95,20)
        SkipHotkeyLine.setReadOnly(True)
        
        SkipHotkeyButton=QtGui.QPushButton("Set Hotkey",self)
        SkipHotkeyButton.clicked.connect(self.set_skip_hotkey)
        SkipHotkeyButton.move(320,245)
        SkipHotkeyButton.resize(100,20)
        
        #OPTIONS
        
        OptionsLabel=QtGui.QLabel('------------------------- Options -------------------------', self)
        OptionsLabel.move(93,280)
        OptionsLabel.resize(250,30)
        
        StartAutoSplitterButton=QtGui.QPushButton("Start Auto Splitter",self)
        StartAutoSplitterButton.clicked.connect(self.auto_splitter)
        StartAutoSplitterButton.move(320,385)
        StartAutoSplitterButton.resize(100,30)
        
        CheckFPSButton=QtGui.QPushButton("Check FPS",self)
        CheckFPSButton.clicked.connect(self.check_fps)
        CheckFPSButton.move(320,310)
        CheckFPSButton.resize(100,25)
        
        CheckFPSLabel=QtGui.QLabel('FPS:   ', self)
        CheckFPSLabel.move(257,312)
        CheckFPSLabel.resize(50,20)
        
        CurrentSplitImageLabel=QtGui.QLabel('Current Split Image: none (Auto Splitter is not running)', self)
        CurrentSplitImageLabel.move(10,390)
        CurrentSplitImageLabel.resize(300,20)
        
        ShowLivePercentDifferenceLabel=QtGui.QLabel('', self)
        ShowLivePercentDifferenceLabel.move(257,335)
        
        CheckBox=QtGui.QCheckBox('Show Live % Match',self)
        CheckBox.move(305,335)
        CheckBox.resize(270,30)
        CheckBox.stateChanged.connect(self.show_live_percent_difference)
        
        ThresholdDropdownLabel=QtGui.QLabel("% Match Threshold:",self)
        ThresholdDropdownLabel.move(10,335)
        ThresholdDropdownLabel.resize(150,30)
        
        ThresholdDropdown=QtGui.QComboBox(self)
        ThresholdDropdown.move(130,340)
        ThresholdDropdown.resize(70,20)
        ThresholdDropdown.addItem("test")
        ThresholdDropdown.addItem("95%")
        ThresholdDropdown.addItem("94%")
        ThresholdDropdown.addItem("93%")
        ThresholdDropdown.addItem("92%")
        ThresholdDropdown.addItem("91%")
        ThresholdDropdown.addItem("90%")
        ThresholdDropdown.addItem("89%")
        ThresholdDropdown.addItem("88%")
        ThresholdDropdown.addItem("87%")
        ThresholdDropdown.addItem("86%")
        ThresholdDropdown.addItem("85%")
        ThresholdDropdown.setCurrentIndex(6)
        ThresholdDropdown.activated[str].connect(self.threshold)
        
        PauseLabel=QtGui.QLabel("Pause after split for:",self)
        PauseLabel.move(10,310)
        PauseLabel.resize(150,30)
        
        PauseDropdown=QtGui.QComboBox(self)
        PauseDropdown.move(130,315)
        PauseDropdown.resize(70,20)
        PauseDropdown.addItem("10 sec")
        PauseDropdown.addItem("20 sec")
        PauseDropdown.addItem("30 sec")
        PauseDropdown.addItem("40 sec")
        PauseDropdown.addItem("50 sec")
        PauseDropdown.addItem("60 sec")
        PauseDropdown.addItem("70 sec")
        PauseDropdown.addItem("80 sec")
        PauseDropdown.addItem("90 sec")
        PauseDropdown.addItem("100 sec")
        PauseDropdown.addItem("110 sec")
        PauseDropdown.addItem("120 sec")
        PauseDropdown.activated[str].connect(self.pause)
        
        self.show()
    
    #get split image directory from user from clicking browse..
    def browse(self):
        global split_image_directory
        split_image_directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Split Image Directory"))+'\\'
        FilePathLine.setText(split_image_directory)
    
    #activate when using match% threshold dropdown
    def threshold(self, text):
        global mean_percent_diff_threshold
        if text == 'test':
            mean_percent_diff_threshold=-1 #putting this to -1 just makes it so that auto_splitter will never split, so that the user can test their splits.
        else:
            mean_percent_diff_threshold=100-int(text[:-1]) #this flips match % different threshold text from the dropdown to a mean_percent_diff_threshold int
    
    #activates when using pause dropdown
    def pause(self,text):
        global pause
        pause = int(text[:-4]) #changes text from pause dropdown to an int to pause after a split
    
            
    def show_live_percent_difference(self, state):
            if state == QtCore.Qt.Checked:
                ShowLivePercentDifferenceLabel.setText('n/a')
            else:
                ShowLivePercentDifferenceLabel.setText(str(''))
    
    #activates when pressing set top left button, hover mouse over top left of game screen. 5 seconds to do so
    def set_top_left(self):
        global x1,y1
        self.disable_buttons()
        i=5
        while i > 0:
            TopLeftButton.setText(str(i)+'..')
            QtGui.QApplication.processEvents()
            time.sleep(1)
            i=i-1
        mouse = pymouse.PyMouse()
        top_left=(mouse.position())
        top_left=np.asarray(top_left)
        x1,y1=top_left
        x1,y1=int(x1),int(y1)
        TopLeftLabel.setText('Top Left Coordinates:'+'                         '+str(x1)+', '+str(y1))
        TopLeftButton.setText('Set Top Left')
        self.enable_buttons()
    
    #activates when pressing set bottom right button, hover mouse over bottom right of game screen. 5 seconds to do so
    def set_bottom_right(self):
        global x2,y2
        self.disable_buttons()
        i=5
        while i > 0:
            BottomRightButton.setText(str(i)+'..')
            QtGui.QApplication.processEvents()
            time.sleep(1)
            i=i-1
        mouse = pymouse.PyMouse()
        bottom_right=(mouse.position())
        bottom_right=np.asarray(bottom_right)
        x2,y2=bottom_right
        x2,y2=int(x2),int(y2)
        BottomRightLabel.setText('Bottom Right Coordinates:'+'                 '+str(x2)+', '+str(y2))
        BottomRightButton.setText('Set Bottom Right')
        self.enable_buttons()
        
    #wait for user to enter hotkey then edit its string  
    def set_split_hotkey(self):
        global split_hotkey
        self.disable_buttons()
        SplitHotkeyButton.setText('press a key..')
        QtGui.QApplication.processEvents()
        split_hotkey = str(keyboard.read_key())
        split_hotkey = split_hotkey.replace('KeyboardEvent(','')
        split_hotkey = split_hotkey.replace('down)','')
        split_hotkey = split_hotkey.replace('up)','')
        split_hotkey = split_hotkey.strip()
        SplitHotkeyLine.setText(split_hotkey)
        SplitHotkeyButton.setText('Set Hotkey')
        self.enable_buttons()
    
    #wait for user to enter hotkey then edit its string      
    def set_reset_hotkey(self):
        global reset_hotkey
        self.disable_buttons()
        ResetHotkeyButton.setText('press a key..')
        QtGui.QApplication.processEvents()
        reset_hotkey = str(keyboard.read_key())
        reset_hotkey = reset_hotkey.replace('KeyboardEvent(','')
        reset_hotkey = reset_hotkey.replace('down)','')
        reset_hotkey = reset_hotkey.replace('up)','')
        reset_hotkey = reset_hotkey.strip()
        ResetHotkeyLine.setText(reset_hotkey)
        ResetHotkeyButton.setText('Set Hotkey')
        self.enable_buttons()
    
    #wait for user to enter hotkey then edit its string      
    def set_undo_hotkey(self):
        global undo_split_hotkey
        self.disable_buttons()
        UndoHotkeyButton.setText('press a key..')
        QtGui.QApplication.processEvents()
        undo_split_hotkey = str(keyboard.read_key())
        undo_split_hotkey = undo_split_hotkey.replace('KeyboardEvent(','')
        undo_split_hotkey = undo_split_hotkey.replace('down)','')
        undo_split_hotkey = undo_split_hotkey.replace('up)','')
        undo_split_hotkey = undo_split_hotkey.strip()
        UndoHotkeyLine.setText(undo_split_hotkey)
        UndoHotkeyButton.setText('Set Hotkey')
        self.enable_buttons()
    
    #wait for user to enter hotkey then edit its string      
    def set_skip_hotkey(self):
        global skip_split_hotkey
        self.disable_buttons()
        SkipHotkeyButton.setText('press a key..')
        QtGui.QApplication.processEvents()
        skip_split_hotkey = str(keyboard.read_key())
        skip_split_hotkey = skip_split_hotkey.replace('KeyboardEvent(','')
        skip_split_hotkey = skip_split_hotkey.replace('down)','')
        skip_split_hotkey = skip_split_hotkey.replace('up)','')
        skip_split_hotkey = skip_split_hotkey.strip()
        SkipHotkeyLine.setText(skip_split_hotkey)
        SkipHotkeyButton.setText('Set Hotkey')
        self.enable_buttons()
    
    #activates when undo split hotkey is is hit from the user. goes back 1 split image unless its the first split.
    def undo_split(self):
        global split_image_number
        global split_image_file
        global split_image_path
        global split_image
        global split_image_resized
        global CurrentSplitImageLabel
        
        if split_image_number == 0:
            split_image_number=split_image_number
        else:
            split_image_number = split_image_number-1
            split_image_file=os.listdir(split_image_directory)[0+split_image_number]
            split_image_path=split_image_directory+split_image_file
            split_image = Image.open(split_image_path)
            split_image_resized=split_image.resize((120,90)) #turn split image into 120x90 image
            CurrentSplitImageLabel.setText('Current Split Image: '+split_image_file)
            QtGui.QApplication.processEvents()
            time.sleep(0.2)
    
    #activates when skip split hotkey is is hit from the user. goes forward 1 split image its the last split      
    def skip_split(self):
        global split_image_number
        global number_of_split_images
        global split_image_file
        global split_image_path
        global split_image
        global split_image_resized
        global CurrentSplitImageLabel
        
        if split_image_number == number_of_split_images-1:
            split_image_number=split_image_number
        else:
            split_image_number = split_image_number+1
            split_image_file=os.listdir(split_image_directory)[0+split_image_number]
            split_image_path=split_image_directory+split_image_file
            split_image = Image.open(split_image_path)
            split_image_resized=split_image.resize((120,90)) #turn split image into 120x90 image
            CurrentSplitImageLabel.setText('Current Split Image: '+split_image_file)
            QtGui.QApplication.processEvents()
            time.sleep(0.2)
    
    def disable_buttons(self):
        BrowseButton.setEnabled(False)
        TopLeftButton.setEnabled(False)
        BottomRightButton.setEnabled(False)
        SplitHotkeyButton.setEnabled(False)
        ResetHotkeyButton.setEnabled(False)
        UndoHotkeyButton.setEnabled(False)
        SkipHotkeyButton.setEnabled(False)
        CheckFPSButton.setEnabled(False)
        StartAutoSplitterButton.setEnabled(False)
        ThresholdDropdown.setEnabled(False)
        PauseDropdown.setEnabled(False)
        
    
    def enable_buttons(self):
        BrowseButton.setEnabled(True)
        TopLeftButton.setEnabled(True)
        BottomRightButton.setEnabled(True)
        SplitHotkeyButton.setEnabled(True)
        ResetHotkeyButton.setEnabled(True)
        UndoHotkeyButton.setEnabled(True)
        SkipHotkeyButton.setEnabled(True)
        CheckFPSButton.setEnabled(True)
        StartAutoSplitterButton.setEnabled(True)
        ThresholdDropdown.setEnabled(True)
        PauseDropdown.setEnabled(True)
        
    def coordinate_error_message(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("error: invalid coordinates!")
        msgBox.exec_()
    
    def split_image_directory_error_message(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("error: no split image folder found")
        msgBox.exec_()
    
    def split_hotkey_error_message(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("set your split hotkey!")
        msgBox.exec_()
    
    def reset_hotkey_error_message(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("set your reset hotkey!")
        msgBox.exec_()
    
    def image_type_error(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("error: all images in folder must be .jpg")
        msgBox.exec_()
    
        def check_fps(self):
        global split_image_directory
        global x1,y1,x2,y2
        global split_hotkey
        global reset_hotkey
        global FPS
        if split_image_directory == 'No Folder Selected' or split_image_directory == '/':
            self.split_image_directory_error_message()
            return
        if not all(File.endswith(".jpg") or File.endswith(".JPG") for File in os.listdir(split_image_directory)):
            self.image_type_error()
            return
        if x2 <= x1 or y2 <= y1 or type(x1)==str or type(x2)==str:
            self.coordinate_error_message()
            return
        CheckFPSButton.setText('Calculating...')
        self.disable_buttons()
        QtGui.QApplication.processEvents()
        split_image_file=os.listdir(split_image_directory)[0]
        split_image_path=split_image_directory+split_image_file
        split_image = Image.open(split_image_path)
        split_image_resized=split_image.resize((120,90))
        #END SPLIT IMAGE STUFF
            
        bbox=x1,y1,x2,y2
        mean_percent_diff=100
        count=0
        t0=time.time()
        while count <= 100:
            with mss.mss() as sct:
                QtGui.QApplication.processEvents()
                sct_img = sct.grab(bbox)
                game_image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
                game_image_resized = game_image.resize((120,90))
                diff=ImageChops.difference(split_image_resized,game_image_resized)
                diff_pix_val=np.asarray(list(diff.getdata()))
                percent_diff=diff_pix_val/255.*100.
                mean_percent_diff=np.mean(percent_diff)
                count=count+1
        t1 = time.time()
        FPS=int(100/(t1-t0))
        FPS=str(FPS)
        CheckFPSLabel.setText('FPS: '+FPS)
        CheckFPSButton.setText('Check FPS')
        self.enable_buttons()
        return
    
    def auto_splitter(self):
        #set global variables
        global split_image_directory
        global split_image_file
        global x1,y1,x2,y2
        global split_hotkey
        global reset_hotkey
        global undo_split_hotkey
        global skip_split_hotkey
        global split_image_number
        global number_of_split_images
        global split_image_file
        global split_image_path
        global split_image
        global split_image_resized
        global CurrentSplitImageLabel
        global mean_percent_diff
        global mean_percent_diff_threshold
        global pause
       
        #multiple checks to see if an error message needs to display
        if split_image_directory == 'No Folder Selected' or split_image_directory == '/':
            self.split_image_directory_error_message()
            return
        if x2 <= x1 or y2 <= y1 or type(x1)==str or type(x2)==str:
            self.coordinate_error_message()
            return
        if split_hotkey == 'none':
            self.split_hotkey_error_message()
            return
        if reset_hotkey == 'none':
            self.reset_hotkey_error_message()
            return
        if not all(File.endswith(".jpg") or File.endswith(".JPG") for File in os.listdir(split_image_directory)):
            self.image_type_error()
            return
        
        #disable buttons, set button text, start timer, get number of split images in the folder.
        self.disable_buttons()
        StartAutoSplitterButton.setText('Running..')
        QtGui.QApplication.processEvents()
        keyboard.press_and_release(split_hotkey)
        number_of_split_images=len(os.listdir(split_image_directory))
        
        #grab split image from folder, resize, and set current split image text
        split_image_number=0
        while split_image_number < number_of_split_images:
            split_image_file=os.listdir(split_image_directory)[0+split_image_number]
            split_image_path=split_image_directory+split_image_file
            split_image = Image.open(split_image_path)
            split_image_resized=split_image.resize((120,90)) #turn split image into 120x90 image
            CurrentSplitImageLabel.setText('Current Split Image: '+split_image_file)
            QtGui.QApplication.processEvents()

            #while loop: constantly take screenshot of user-defined area, resize, and compare to split image. if the images meet the user-defined match threshold, exit while loop and split.
            bbox=x1,y1,x2,y2
            mean_percent_diff=100
            while mean_percent_diff > mean_percent_diff_threshold:
                with mss.mss() as sct:
                    QtGui.QApplication.processEvents()
                    sct_img = sct.grab(bbox)
                    game_image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
                    game_image_resized = game_image.resize((120,90))
                    diff=ImageChops.difference(split_image_resized,game_image_resized)
                    diff_pix_val=np.asarray(list(diff.getdata()))
                    percent_diff=diff_pix_val/255.*100.
                    mean_percent_diff=np.mean(percent_diff)
                    #if checkbox is checked, show live percent difference to a few decimal places.
                    if CheckBox.isChecked():
                        ShowLivePercentDifferenceLabel.setText(str(100-mean_percent_diff)[0:5]+'%')
                        QtGui.QApplication.processEvents()
                    #if reset hotkey is pressed, stop autosplitter and reset some text.
                    if keyboard.is_pressed(reset_hotkey):
                        CurrentSplitImageLabel.setText('Current Split Image: none (Auto Splitter is not running)')
                        StartAutoSplitterButton.setText('Start Auto Splitter')
                        ShowLivePercentDifferenceLabel.setText('n/a')
                        self.enable_buttons()
                        QtGui.QApplication.processEvents()
                        print('Reset')
                        return
                    #if undo split hotkey is pressed, go back one split
                    if keyboard.is_pressed(undo_split_hotkey):
                        self.undo_split()
                    #if skip split hotkey is pressed, go forward one split.
                    if keyboard.is_pressed(skip_split_hotkey):
                        self.skip_split()
            
            #loop breaks to here when match threshold is met. splits the timer, goes to next split, and pauses for a user-defined amount of time before comparing the next split.
            print('split!')
            keyboard.press_and_release(split_hotkey)
            split_image_number=split_image_number+1
            if number_of_split_images != split_image_number:
                CurrentSplitImageLabel.setText('Current Split Image: (paused, waiting to go to next split)')
                QtGui.QApplication.processEvents()
                pause=pause*1000
                QtTest.QTest.qWait(pause)
                
        #loop breaks to here when the last image splits. 
        CurrentSplitImageLabel.setText('Current Split Image: none (Auto Splitting finished)')
        StartAutoSplitterButton.setText('Start Auto Splitter')
        self.enable_buttons()
        QtGui.QApplication.processEvents()
        print('done splitting')
    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
