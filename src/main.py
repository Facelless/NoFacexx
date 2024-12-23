import pickle
import cv2
import socket
import struct
from config.colors import RED, RESET, GREEN, BOLD
from database.database import collection

class PanelAdmin:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _camCompiuter(self, ip: str, port: int):
        try:
            print(f"Tentando se conectar a {ip}:{port}...")
            self.client_socket.connect((ip, port))
            server_ip, server_port = self.client_socket.getpeername()
            print(RED + '[SERVER] ' + RESET + GREEN + 'CONECTADO' + RESET)
            print(RED + '[IP] ' + RESET + GREEN + f'{server_ip}' + RESET)
            print(RED + '[PORT] ' + RESET + GREEN + f'{server_port}' + RESET)

            data = b""
            payload_size = struct.calcsize("L")
            window_name = "Monitoramento em Tempo Real"

            while True:
                while len(data) < payload_size:
                    data += self.client_socket.recv(4096)

                packed_size = data[:payload_size]
                data = data[payload_size:]
                frame_size = struct.unpack("L", packed_size)[0]
                while len(data) < frame_size:
                    data += self.client_socket.recv(4096)

                frame_data = data[:frame_size]
                data = data[frame_size:]

                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow(window_name, frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            print(RED + f"Ocorreu um erro ao conectar ao servidor {ip}: {e}" + RESET)

        finally:
            self.client_socket.close()
            cv2.destroyAllWindows()

    def _scanConnections(self):
        dates = collection.find({})
        
        for dado in dates:
            ip = dado.get("ip")
            porta = dado.get("port")
            
            if ip and porta:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(5)
                        resultado = s.connect_ex((ip, porta))
                        
                        if resultado == 0:
                            print(RED + '[IP] ' + RESET + GREEN + f'{ip}' + RESET + ' | ' + RED + '[PORT] ' + RESET + GREEN + f'{porta}' + RESET + ' ✅')
                        else:
                            print(RED + '[IP] ' + RESET + GREEN + f'{ip}' + RESET + '   | ' + RED + '[PORT] ' + RESET + GREEN + f'{porta}' + RESET + ' ❌')
                except socket.timeout:
                    print(f"Timeout ao tentar conectar ao IP {ip}, Porta {porta}")
                except socket.gaierror:
                    print(f"Erro de nome de host para o IP {ip}, Porta {porta}")
                except ConnectionRefusedError:
                    print(f"Conexão recusada para o IP {ip}, Porta {porta}")
                except Exception as e:
                    print(f"Erro inesperado ao escanear o IP {ip}, Porta {porta}: {e}")
            else:
                print(f"IP ou Porta ausente para o dado: {dado}")

    def select_option(self):
        while True:
            print('')
            print(BOLD + '1 - Escanear Conexões' + RESET)
            print(BOLD + '2 - Conectar à Câmera' + RESET)
            i_int = int(input(RED + '=> ' + RESET))

            if i_int == 1:
                self._scanConnections()
            elif i_int == 2:
                ip = input("Digite o IP para se conectar à câmera: ")
                porta = int(input("Digite a porta para se conectar à câmera: "))
                self._camCompiuter(ip, porta)
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    panel_admin = PanelAdmin()
    panel_admin.select_option()
