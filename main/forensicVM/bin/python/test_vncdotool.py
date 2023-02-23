import vncdotool
from vncdotool import api


# Connect to a VNC server
client = api.connect('localhost:0', password=None)

client.captureScreen('screenshot.png')

# Fill in a form with values

client.keypress("Username: john\n")

client.keypress("Password: password123\n")

client.keyPress("Enter")

client.expectScreen('screenshot.png', maxrms=10)

# Close the connection

client.disconnect()
