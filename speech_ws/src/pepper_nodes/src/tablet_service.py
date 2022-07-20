#!/usr/bin/env python
from pepper_nodes.srv import ExecuteJS, ExecuteJSResponse, LoadUrl, LoadUrlResponse
import qi
import rospy
IP = "10.0.1.230" # 10.0.1.230
PORT = 9559
# The ip of the robot from the tablet is 198.18.0.1


def callback(req):
    transcription = str(req.text)
    text = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
      background-color: #CD5C5C;
    }
    </style>
    </head>
    <body>

    <h1>{trans}</h1>
    <p><a href="https://www.w3schools.com">Visit W3Schools.com!</a></p>

    </body>
    </html>
    '''.format(trans = transcription)

    file = open("/home/webapp/templates/index.html","w")
    file.write(text)
    file.close()
    print("file html updated")
    show(transcription)
    return LoadUrlResponse("ACK0")

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
    return tablet

def show(out_str):
    try:
        #tablet.loadUrl("https://www.unisa.it")
        tablet.loadUrl("http://127.0.0.1:5001/")
        tablet.showWebview()
        print("HTML loaded")
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )
        tablet = session.service("ALTabletService")
        tablet.loadUrl("http://127.0.0.1:5001/")
        tablet.showWebview()
    # time.sleep(0.5)

if __name__ == "__main__":
    tablet = connect_robot()
    rospy.init_node('tablet_service')
    rospy.Service('tablet_server', LoadUrl, callback)
    print("Ready to update the tablet screen.")
    rospy.spin()