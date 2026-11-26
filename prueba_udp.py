import argparse
import json
import socket

#Programa de IA para comprobar si funciona el envio por UDP

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receptor UDP de prueba (EOII)")
    parser.add_argument("--port", type=int, default=3000, help="Puerto UDP de escucha")
    parser.add_argument("--num-iter", type=int, default=360, help="Tramas a recibir (0 = sin fin)")
    args = parser.parse_args()

    # Crear socket UDP y enlazarlo al puerto de escucha
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('localhost', args.port))
    print(f"Escuchando datagramas UDP en localhost:{args.port}...")

    n_iter = 0
    try:
        while n_iter < args.num_iter or args.num_iter == 0:
            # recvfrom bloquea la ejecución hasta que llega un datagrama (máx 4096 bytes)
            data, addr = udp_socket.recvfrom(4096)
            
            # Decodificar bytes a string y parsear el JSON a diccionario
            mensaje = json.loads(data.decode('utf-8'))
            
            print(f"[{n_iter}] Recibido desde {addr}: {json.dumps(mensaje, indent=2)}")
            n_iter += 1
    except KeyboardInterrupt:
        print("\nRecepción detenida por el usuario.")
    finally:
        udp_socket.close()