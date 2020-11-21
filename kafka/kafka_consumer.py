import threading
from kafka import KafkaConsumer
import json
import logging
import sys
# import cv2
import numpy as np
from kafka import KafkaProducer
logger = logging.getLogger("kafka")
from PIL import Image
import io
import base64
#logger.addHandler(logging.StreamHandler(sys.stdout))
#logger.setLevel(logging.DEBUG)

class Kafka_Consumer(threading.Thread):
    def __init__(self, broker, input_queue):
        threading.Thread.__init__(self)
        self.broker = broker["address"]
        self.topic = broker["topic"]
        self.input_queue = input_queue
        
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 auto_offset_reset='latest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe([self.topic])
        cnt=0
        while (True):
            for message in consumer:
                # print(message)
                # try:
                # print(type(message.value))
                my_json = message.value.decode('utf-8')
                # print(my_json)
                data = json.loads(my_json)
                # print(data)

                ###################
                # SAVE IMAGE
                ###################
                # print(data)
                # print(data["faces"][0].keys()) 
                # img_arr = data["faces"][0]["faceImage"]
                #img_arr = data["image"]
                # print(img_arr)
                # print(data)
                # print(data["image"])
                #data = base64.b64decode(img_arr)
                # #print(data)
                # # imgx = np.fromstring(img_arr, dtype='float')

                #image = Image.open(io.BytesIO(img_arr))
                # # #print(img_arr)
                #image = Image.open(io.BytesIO(data))
                #img = np.array(image)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                #cv2.imshow("XXX", img)
                #cv2.waitKey(5)
                #print(img.shape)
                # img = cv2.imdecode(data, cv2.IMREAD_COLOR)

                ###################
                # SAVE JSON MESSAGE
                ###################
                mess = open('message.json','a')  
                mess.write("{},\n".format(data))
                mess.close()

                # print("_____DATA: ", type(data))
                    #self.input_queue.append(data)
                # except Exception as e:
                #     print (message)
                #     print("ERROR", e)

                cnt+=1
                print(cnt)
    
        #consumer.close()
import sys
if __name__=='__main__':
    # topic = sys.argv[s1]
    topic = "DAN_FACES"
    address = "192.168.40.92:9094"
    cons = Kafka_Consumer({"address":[address],"topic":topic}, None)
    cons.start()
    cons.join()
