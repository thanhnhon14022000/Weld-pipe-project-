##########################################
# WINDOWS VERSION
#
# This program is used to test send key by using lib pywinauto
# time.monotonic
# Fixed .sendkey() warning
# Processing runtime
#
###########################################

#================================================================================#
#   IMPORT MODULES ARE USED
#================================================================================#
import cv2 as cv
import numpy as np
import argparse
import math
import datetime
import os
import imutils
import time
import pywinauto
from pywinauto.application import Application  # import pywinauto lib
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
#================================================================================#
#   INITIALIZING GLOBAL VARIABLES WITH INITIAL VALUE
#================================================================================#
y_dis = 0
state = 0
alpha = 5
beta = 0
ppm = 44.06237571
# Set canny threshold and hough_theshold
# canny_threshold = 100
# hough_threshold = 120

# Image saved directory
# directory = r'/home/ubuntu/Learning/Image_Processing/image_processing_in_python/Welding_image_process/img_saved'
directory = r'D:\\Welding_image_process\\img_saved'


# Set the name of output file
timenow = datetime.datetime.now()
# filename_output = "/home/ubuntu/Learning/Image_Processing/image_processing_in_python/Welding_image_process/data/gcode_" + timenow.strftime("%d%m%y")+"_"+timenow.strftime("%H%M%S")+".txt"
filename_output = "D:\Welding_image_process\data\gcode_" + \
    timenow.strftime("%d%m%y")+"_"+timenow.strftime("%H%M%S")+".txt"

file_output = open(filename_output, "w+")
file_output.close()

# Define the codec and create VideoWriter object
filename_video = "D:\\Welding_image_process\\img_saved\\video_" + \
    timenow.strftime("%d%m%y")+"_"+timenow.strftime("%H%M%S")+".avi"
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(filename_video, fourcc, 20.0, (640,  480))

start_time = 0
FirstTO = 0
GlobalTO = 0

#================================================================================#
#   IMPLEMENTATION
#================================================================================#

#**
# @brief    line_prepend - add a line to the beginning of current lines
# @details
# 
# @return     none
# @retval     none
# 
# @pre None
# @post None
#
#================================================================================#


def line_prepend(newContent):
    file_output = open(filename_output, "r+")
    currentContent = file_output.read()
    # print(currentContent)
    file_output.seek(0, 0)
    file_output.write(newContent + "\n")
    file_output.write(currentContent)
    file_output.close()

#**
# @brief    state_0 - send home & move command to Mach3 software
# @details
# 
# @return     none
# @retval     none
# 
# @pre None
# @post None
#
#================================================================================#


def state_0():
    appMach3 = Application(backend='uia').connect(
        title="Mach3 CNC Controller ")
    # First step - Load Recent File
    loadRF = appMach3.Mach3CNCController.child_window(
        title="Recent File", auto_id="8349", control_type="Button").wrapper_object()
    loadRF.click()
    time.sleep(0.1)
    # Click 'OK'
    okBTN = appMach3.Mach3CNCController.child_window(
        title="OK", auto_id="1", control_type="Button").wrapper_object()
    okBTN.click()
    time.sleep(0.1)
    # Edit GCode
    okBTN = appMach3.Mach3CNCController.child_window(
        title="Edit G-Code", auto_id="8586", control_type="Button").wrapper_object()
    okBTN.click()
    time.sleep(0.1)
    # Edit gcode by notepad
    notepad = Application(backend='uia').connect(title="gcode.txt - Notepad")
    send_keys('^a')  # send key "alt + a" to mach3 software
    time.sleep(0.05)
    # Add "G0 Y5" into gcode file to control Mach3 Y Homing
    notepad.gcodetxtNotepad.Edit.type_keys("G0 X30 Y5", with_spaces=True)
    time.sleep(0.05)
    send_keys('{ENTER}')  # send key "Enter" to mach3 software
    time.sleep(0.05)
    notepad.gcodetxtNotepad.menu_select("File -> Save")
    time.sleep(0.05)
    notepad.gcodetxtNotepad.menu_select("File -> Exit")
    time.sleep(0.2)
    send_keys('%r')
    send_keys('%r')
    time.sleep(30)

    ################################
    loadRF.click()
    time.sleep(0.1)

    # Click 'OK'
    okBTN = appMach3.Mach3CNCController.child_window(
        title="OK", auto_id="1", control_type="Button").wrapper_object()
    okBTN.click()
    time.sleep(0.1)

    # Edit GCode
    okBTN = appMach3.Mach3CNCController.child_window(
        title="Edit G-Code", auto_id="8586", control_type="Button").wrapper_object()
    okBTN.click()
    time.sleep(0.1)

    # Edit gcode by notepad
    notepad = Application(backend='uia').connect(title="gcode.txt - Notepad")
    send_keys('^a')
    time.sleep(0.05)

    # Add "G1 Y180 F300" into gcode file to control Mach3 goto Y180 with Feedrate = 300 mm/p
    notepad.gcodetxtNotepad.Edit.type_keys("G1 Y135 F300", with_spaces=True)
    time.sleep(0.05)
    send_keys('{ENTER}')
    time.sleep(0.05)
    notepad.gcodetxtNotepad.menu_select("File -> Save")
    time.sleep(0.05)
    notepad.gcodetxtNotepad.menu_select("File -> Exit")
    time.sleep(0.1)
    send_keys('%r')
    send_keys('%r')
    time.sleep(0.05)
    # Set State_var = 1 to switch to state 1


#**
# @brief    state_2 - detect, recognize and creat gcode
# @details
# 
# @return     none
# @retval     none
# 
# @pre None
# @post None
#
#================================================================================#

def state_2():
    global y_dis
    global state
    global start_time
    # global FirstTO
    # global GlobalTO

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray_ct = cv.addWeighted(img_gray, alpha, np.zeros(
        img_gray.shape, img_gray.dtype), 0, beta)

    img_copy = np.copy(img)

    # Set canny threshold and hough theshold
    canny_threshold = 100
    hough_threshold = 120

    blur_img = cv.blur(img_gray_ct, (9, 9))
    binary_img = cv.adaptiveThreshold(
        blur_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 2)
    binary_img = cv.erode(binary_img, None, iterations=2)

    # Skeletonize the image
    skeleton_img = cv.ximgproc.thinning(binary_img, 0)

    # HoughLine
    lines = cv.HoughLines(skeleton_img, 1, np.pi / 180,
                          hough_threshold, None, 0, 0)

    all_point_x_top = []
    all_point_x_bottom = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]

            a = math.cos(theta)
            b = math.sin(theta)
            pt1 = (int(rho/a), 0)
            pt2 = (int((rho/a)-640*(b/a)), 640)

            if ((pt1[0] < 10000 and pt1[0] > -20000) and  # pt1[0] (X_1) must be in range (-20000;100000)
                # pt2[0] (X_2) must be in range (-20000;200000)
                (pt2[0] < 20000 and pt2[0] > -20000) and
                # pt1[0] (X_1) and pt2[0] (X_2) cannot be 0
                (pt1[0] != 0 and pt2[0] != 0) and
                    (pt1[0] != pt2[0])):  # pt1[0] (X_1) and pt2[0] (X_2) must be different
                #y1 != y2
                all_point_x_top.append(pt1)
                all_point_x_bottom.append(pt2)

        num_line = len(all_point_x_top)

        if (num_line != 0):
            ave_top_point = 0
            ave_bottom_point = 0

            for i in range(0, num_line):
                ave_top_point += all_point_x_top[i][0]
                ave_bottom_point += all_point_x_bottom[i][0]

            ave_top_point = int(ave_top_point/num_line)
            ave_bottom_point = int(ave_bottom_point/num_line)

            cv.line(img_copy, (ave_top_point, 0),
                    (ave_bottom_point, 640), (0, 0, 255), 1)

            for j in range(0, 640):
                if ((img_copy[240, j][0] == 0) and
                    (img_copy[240, j][1] == 0) and
                        (img_copy[240, j][2] == 255)):
                    # Distance of X
                    x_dis = (j/ppm) + 33.6848  # delta_X = 33.6848
#######
                    # Delta Time from the starting of state 3 to current
                    DeltaTime = (end_time - start_time)
                    # y_dis = round(((DeltaTime * (300/60)) - GlobalTO ),4) #old_value 99.5 #old_offset 0.1852
                    y_dis = round((DeltaTime*(300/60) + 105.6454), 4)
                    # #visme 33mm from base

                    # #DATA SAMPLE G90 G1 F2000 X Y
#######
                    str_gcode = "G1 X" + \
                        str(round(x_dis, 4)) + " Y" + str(y_dis) + " F300"

                    # Add the new str_gcode line above the previous one
                    line_prepend(str_gcode)

                    # cv.putText(img_copy,str(round(distance_line,4)),(50,50),fontFace=cv.FONT_HERSHEY_COMPLEX,fontScale=1,color=(150,100,200),thickness=2)
                    # cv.arrowedLine(img_copy,(0,240),(j,240),(255,255,0),5)
                    # cv.arrowedLine(img_copy,(j,240),(0,240),(255,255,0),5)
                    # cv.line(img_copy,(0,240),(640,240),(0,255,0),1)
                    break

    # else:
        #print("LINE NOT FOUND")
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", img_copy)
    if (y_dis >= 240):
        cv.destroyAllWindows()
        state = 3


######################
# MAIN CODE
######################
print("State 0 - SETUP MACHINE. PLEASE WAIT 30 SECONDS...")
#cap_camera = cv.VideoCapture(1)
if(state == 0):
    state_0()
    state = 2
    # FirstTO = time.monotonic() #The first time offset point

# print("State 1")

# if(state == 1):
#     time_record = time.monotonic()
#     while((time.monotonic()-time_record) <= 35):
#         ret,frame = cap_camera.read() #timing
#         print("current time: ", time.monotonic())
#         # if frame is read correctly ret is True
#         out.write(frame)


#     out.release()
#     state = 2 #set state variable = 2 to switch state
#     cap_camera.release()

print("State 1. ANALYZE AND GENERATE GCODE")

#cap = cv.VideoCapture("img_saved\\test_state.mp4")
# cap_video = cv.VideoCapture(filename_video)
cap_video = cv.VideoCapture(0,cv.CAP_DSHOW)
start_time = time.monotonic()

while(state == 2):
    ret, img = cap_video.read()  # timing
    end_time = time.monotonic()  # End of time delta
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    img = cv.flip(img, 1)
    img = cv.flip(img, 0)
    state_2()

    # Check key
    key = cv.waitKey(1)
    # if key & 0xFF == ord('p'): # Press "p" to pause
    #     cv.waitKey(-1)

    # elif key & 0xFF == ord('s'): # Press "s" to save a current frame
    #     timenow = datetime.datetime.now()
    #     filename = "img_saved_"+timenow.strftime("%d%m%y")+"_"+timenow.strftime("%H%M%S")+".jpg"
    #     print(filename)
    #     os.chdir(directory)
    #     cv.imwrite(filename, img)

    if key & 0xFF == ord('q'):  # Press "q" to quit
        break

print("DONE")
print("THE GCODE IS SAVED IN "+str(filename_output))
cap_video.release()
cv.destroyAllWindows()
