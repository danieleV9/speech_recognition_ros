#!/usr/bin/env python
from pepper_nodes.srv import ExecuteJS, ExecuteJSResponse
import qi
import rospy
from flask import Flask
IP = "10.0.1.230" # 10.0.1.230
PORT = 9559
# The ip of the robot from the tablet is 198.18.0.1

def update_html(content):

    app = Flask(__name__)

    @app.route('/')
    def index():
        return str(content)

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')


def callback(req):
    transcription = str(req.text)
    text = '''
    <html>
        <body bgcolor="#800000">
            <h1>{}</h1>
        </body>
    </html>
    '''.format(transcription)

    text = '''
    <!DOCTYPE html>
    <html>
    <body>

    <p>Same as color name "Tomato":</p>

    <h1 style="background-color:rgb(255, 99, 71);">rgb(255, 99, 71)</h1>
    <h1 style="background-color:#ff6347;">#ff6347</h1>
    <h1 style="background-color:hsl(9, 100%, 64%);">hsl(9, 100%, 64%)</h1>

    <p>Same as color name "Tomato", but 50% transparent:</p>
    <h1 style="background-color:rgba(255, 99, 71, 0.5);">rgba(255, 99, 71, 0.5)</h1>
    <h1 style="background-color:hsla(9, 100%, 64%, 0.5);">hsla(9, 100%, 64%, 0.5)</h1>

    <p>In addition to the predefined color names, colors can be specified using RGB, HEX, HSL, or even transparent colors using RGBA or HSLA color values.</p>

    </body>
    </html>
    '''

    #file = open("/home/speech_ws/src/pepper_nodes/src/j-tablet-browser/index.html","w")
    #file.write(text)
    #file.close()
    update_html(transcription)
    print("html updated")
    show(transcription)
    return ExecuteJSResponse("ACK0")

def connect_robot():
    # Connect to the robot
    print("Connecting to robot...")
    session = qi.Session()
    session.connect('tcp://%s:9559' % IP )  # Robot IP
    print("Robot connected")

    motion_service = session.service("ALMotion")
    motion_service.wakeUp()

    #Tablet service
    tablet = session.service("ALTabletService")
    tablet.resetTablet()
    #tablet.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")
    #tablet.showWebview()
    return tablet

def show(out_str):
    try:
        #tablet.executeJS("/home/speech_ws/src/pepper_nodes/src/j-tablet-browser/index.html")
        #tablet.loadUrl("https://www.unisa.it")
        tablet.loadUrl("http://127.0.0.1:5000/")
        tablet.showWebview()
        #tablet.executeJS(script)
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )
        tablet = session.service("ALTabletService")
        tablet.loadUrl("http://127.0.0.1:5000/")
        tablet.showWebview()
        #tablet.executeJS(script)
    # time.sleep(0.5)

if __name__ == "__main__":
    tablet = connect_robot()
    rospy.init_node('tablet_service')
    rospy.Service('tablet_server', ExecuteJS, callback)
    print("Ready to update the tablet screen.")
    rospy.spin()