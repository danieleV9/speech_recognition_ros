#!/usr/bin/env python
from pepper_nodes.srv import ExecuteJS, ExecuteJSResponse
import qi
import rospy
IP = "10.0.1.207" # 10.0.1.207
PORT = 9559
# The ip of the robot from the tablet is 198.18.0.1

def callback(req):
    transcription = str(req.text)
    text = '''
    <html>
        <body>
            <h1>{}</h1>
        </body>
    </html>
    '''.format(transcription)
    file = open("/home/speech_ws/src/pepper_nodes/src/j-tablet-browser/index.html","w")
    file.write(text)
    file.close()
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
        tablet.loadUrl("https://www.unisa.it")
        tablet.showWebview()
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )
        tablet = session.service("ALTabletService")
        #tablet.executeJS("/home/speech_ws/src/pepper_nodes/src/j-tablet-browser/index.html")
        tablet.loadUrl("https://www.unisa.it")
        tablet.showWebview()
    # time.sleep(0.5)

if __name__ == "__main__":
    tablet = connect_robot()
    rospy.init_node('tablet_service')
    rospy.Service('tablet_server', ExecuteJS, callback)
    print("Ready to update the tablet screen.")
    rospy.spin()