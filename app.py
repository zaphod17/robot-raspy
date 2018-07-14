from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)


#Define pins numbers of motor controll pins
mRight=18
mForward=23
mLeft=24
mBack=25

# Create a dictionary called Light to store the pin number, and pin state of LED lights:
Light = {'pin' : 8 ,'state' : GPIO.LOW}



# Set each pin as an output and make it low:
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(mRight, GPIO.OUT)
GPIO.setup(mForward, GPIO.OUT)
GPIO.setup(mLeft, GPIO.OUT)
GPIO.setup(mBack, GPIO.OUT)
GPIO.output(mRight , 0)
GPIO.output(mForward , 0)
GPIO.output(mLeft, 0)
GPIO.output(mBack, 0)
GPIO.setup(Light['pin'], GPIO.OUT)
GPIO.output(Light['pin'], GPIO.LOW)




print ("Ready")

@app.route("/")
def index():
   # Read the Light state and store it in the Light dictionary:
   Light['state'] = GPIO.input(Light['pin'])
   # Put the Light dictionary into the template data dictionary:
   templateData = {
      'Light' : Light
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route('/left')
def left_side():
    GPIO.output(mLeft , 1)
    return 'true'

@app.route('/right')
def right_side():
   GPIO.output(mRight , 1)
   return 'true'

@app.route('/up')
def up_side():
   GPIO.output(mForward , 1)
   return 'true'

@app.route('/down')
def down_side():
   GPIO.output(mBack , 1)
   return 'true'

@app.route('/stopFB')
def stopFB():
   GPIO.output(mForward , 0)
   GPIO.output(mBack , 0)
   return  'true'


@app.route('/stopLR')
def stopLR():
   GPIO.output(mRight , 0)
   GPIO.output(mLeft , 0)
   return  'true'


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
    
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      

   # Read the Light state and store it in the Light dictionary:  
   Light['state'] = GPIO.input(Light['pin'])

   # Pass the template data into the template main.html and return it to the user
   templateData = {
      'Light' : Light
   }

   return render_template('main.html', **templateData)


if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)


