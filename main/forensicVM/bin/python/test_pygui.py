import os
os.environ['DISPLAY'] = ':0'

import pyautogui
import vncdotool.client


# Connect to the VNC server

vnc = vncdotool.client.Client("localhost:5900")

vnc.keyboard.press_and_release('alt+tab')


# Locate the form fields on the screen

username_field = pyautogui.locateOnScreen('username_field.png')

password_field = pyautogui.locateOnScreen('password_field.png')

submit_button = pyautogui.locateOnScreen('submit_button.png')


# Fill in the form fields with the appropriate values

pyautogui.click(username_field)

pyautogui.typewrite("username")

pyautogui.click(password_field)

pyautogui.typewrite("password")


# Submit the form

pyautogui.click(submit_button)
