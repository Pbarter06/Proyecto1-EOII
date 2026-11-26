import random
import time
from datetime import datetime
import argparse
import json 
import socket

if __name__ == "__main__":
    #recogida de argumentos de la linea de comandos
    parser = argparse.ArgumentParser(description="Servidor UDP simulador de sensor (EOII)") 
    parser.add_argument("--port", type=int, default=3000, help="Puerto UDP de conexion") 
    parser.add_argument("--scada-port", type=int, default=3001, help="Puerto UDP de conexion") #futura implementacion
    parser.add_argument("--num-iter", type=int, default=360, help="Tramas por sensor (0 = sin fin)")
    parser.add_argument("--period", type=float, default=0.5, help="Segundos entre envíos, 0.5 por defecto") 
    # los valores quedan en args.port, args.scada_port y args.num_iter 
    args = parser.parse_args() 

    #Inicio conexion puerto UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', args.port)
    #Fin conexion puerto UDP

    #Inicialización de variables
    random.seed(datetime.now().timestamp())
    n_iter = 0
    posx, posy = 5, 5
    battery = 100
    temp_motor = 35
    status = "MOVING" #Modo de operación que informa el robot: MOVING, IDLE o CHARGING 
    #Fin inicialización de variables

    while n_iter < args.num_iter or args.num_iter == 0:
        time_before = time.time()
        #inicio generacion de datos
        if status == "CHARGING":
            battery = min(battery + 2, 100)
        elif status == "MOVING":
            battery = max(battery - 2, 0)
            movex = random.randint(-1, 1)
            movey = random.randint(-1, 1)
            if posx + movex >= 0 and posx + movex <= 10:
                posx += movex
            if posy + movey >= 0 and posy + movey <= 10:
                posy += movey

            vtemp = random.choice([-0.15, 0.40])
            if(temp_motor + vtemp >= 30 and temp_motor + vtemp <= 45):
                temp_motor += vtemp
        else: #status = "IDLE"
            if temp_motor - 0.25 >= 30:
                temp_motor -= 0.25


        message = {
            "robot_id": "ROBOT_AGV_01",
            "seq": n_iter,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "pos_x": round(posx, 2), 
            "pos_y": round(posy, 2), 
            "battery": battery,
            "temp_motor": round(temp_motor, 2),
            "status": status
        }

        if battery < 15:
            status = "CHARGING"
        elif status == "CHARGING" and battery >= 95:
            status = "MOVING"
        #seleccion MOVING o IDLE con probabilidad de 0.8 y 0.2 respectivamente
        if status == "MOVING" or status == "IDLE":
            if random.random() < 0.2:
                status = "IDLE"
            else:
                status = "MOVING"
        #fin generacion de datos aleatorios

        #Inicio envio del json codificado en UTF-8
        message_json = json.dumps(message)
        udp_socket.sendto(message_json.encode('utf-8'), server_address)
        #Fin envio de datos
        n_iter += 1
        time_after = time.time()
        time.sleep(max(0, args.period - (time_after - time_before)))

    udp_socket.close()
