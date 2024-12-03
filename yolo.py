import cv2
from ultralytics import YOLO
import torch
from pythonosc import udp_client
from pythonosc import osc_message_builder
import time
the_port=12498
client = udp_client.SimpleUDPClient('127.0.0.1', the_port)



def send_osc(client,ip, port, address, value):
    msg = osc_message_builder.OscMessageBuilder(address = address)
    msg.add_arg(value, arg_type='f')  
    msg = msg.build()
    client.send(msg)

model = YOLO("yolov8n-pose.pt")
video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(0) 
while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Inference", annotated_frame)
        # Break the loop if 'q' is pressed
        if results[0].keypoints.xyn[0].shape == torch.Size([17,2]):
            x1=float(results[0].keypoints.xyn[0][11][0])
            y1=float(results[0].keypoints.xyn[0][11][1])
            x2=float(results[0].keypoints.xyn[0][12][0])
            y2=float(results[0].keypoints.xyn[0][12][1])
            x3=float(results[0].keypoints.xyn[0][15][0])
            y3=float(results[0].keypoints.xyn[0][15][1])
            x4=float(results[0].keypoints.xyn[0][16][0])
            y4=float(results[0].keypoints.xyn[0][16][1])
            
        
            flag=0

            if x1!=0:
                send_osc(client,'127.0.0.1', the_port, '/righthand_x', x1)
            if y1!=0:
               send_osc(client,'127.0.0.1', the_port, '/righthand_y', y1)
            if x2!=0:
                send_osc(client,'127.0.0.1', the_port, '/lefthand_x', x2)
            if y2!=0:
                send_osc(client,'127.0.0.1', the_port, '/lefthand_y', y2)
            if x3!=0:
                send_osc(client,'127.0.0.1', the_port, '/rightfoot_x', x3)
            if y3!=0:
                send_osc(client,'127.0.0.1', the_port, '/rightfoot_y', y3)
            if x4!=0:
                send_osc(client,'127.0.0.1', the_port, '/leftfoot_x', x4)
            if y4!=0:
                send_osc(client,'127.0.0.1', the_port, '/leftfoot_y', y4)
            time.sleep(0.01)
            print('==================')
        else:
            pass

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()