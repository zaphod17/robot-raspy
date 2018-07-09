from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

m11=18
m12=23
m21=24
m22=25
light=8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(light, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)
GPIO.output(light, 0)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   8 : {'name' : 'GPIO 8', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)



print ("Ready")

a=1
@app.route("/")
def index():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
       pins[pin]['state'] = GPIO.input(pin)

   # Put the pin dictionary into the template data dictionary:
       templateData = {
         'pins' : pins
         }
   # Pass the template data into the template main.html and return it to the user
    return render_template('robot.html', **templateData)

@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(m11 , 0)
    GPIO.output(m12 , 0)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return 'true'

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return 'true'

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   return 'true'

@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return  'true'

@app.route('/lighton')
def light_on():
   data1="LIGHT ON"
   GPIO.output(light , 1)
   return  'true'

@app.route('/lightoff')
def light_off():
   data1="LIGHT OFF"
   GPIO.output(light , 0)
   return  'true'

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
       # Set the pin high:
       GPIO.output(changePin, GPIO.HIGH)
       # Save the status message to be passed into the template:
       message = "Turned " + deviceName + " on."

   if action == "off":
       GPIO.output(changePin, GPIO.LOW)
       message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
      templateData = {
         'pins' : pins
      }

   # Along with the pin dictionary, put the message into the template data dictionary:
    return render_template('robot.html', **templateData)

if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
