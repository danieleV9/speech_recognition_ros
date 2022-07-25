#!/usr/bin/env python
from pepper_nodes.srv import ExecuteJS, ExecuteJSResponse, LoadUrl, LoadUrlResponse
import qi
import rospy
IP = "10.0.1.207" # 10.0.1.207
PORT = 9559
# The ip of the robot from the tablet is 198.18.0.1


def callback(req):
    transcription = str(req.text)
    transcription = transcription.upper()
    text = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ASR output</title>
    </head>
    <body style="background-color:white;">
    <div style="color: black;padding: 150px 0;border: 2px solid white;text-align: center;">
        <h1 style="font-size: 72px">{trans}</h1>
    </div>
    </body>
    </html>
    '''.format(trans = transcription)

    file = open("/home/webapp/templates/index.html","w")
    file.write(text)
    file.close()
    print("HTML file updated")
    show()
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

def show():
    try:
        #tablet.loadUrl("https://www.unisa.it")
        #tablet.loadUrl("http://127.0.0.1:5001/")
        res_web = tablet.showWebview("http://10.0.1.210:5001/")
        print(str(res_web))
        print("HTML loaded on tablet")
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )
        tablet = session.service("ALTabletService")
        #tablet.loadUrl("http://127.0.0.1:5001/")
        res_web = tablet.showWebview("http://10.0.1.210:5001/")
        print(str(res_web))
        print("HTML loaded on tablet")
    # time.sleep(0.5)

if __name__ == "__main__":
    tablet = connect_robot()
    rospy.init_node('tablet_service')
    rospy.Service('tablet_server', LoadUrl, callback)
    print("Ready to update the tablet screen.")
    rospy.spin()