import socket
import threading
from queue import Queue

print_lock = threading.Lock()

target = input("Digite o alvo (ex.: 192.168.1.1): ")
port_range = range(1, 1025)  
queue = Queue()

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    with print_lock:
        if result == 0:
            try:
                service = socket.getservbyport(port)
                print(f"Porta {port} está aberta | Serviço: {service}")
            except:
                print(f"Porta {port} está aberta | Serviço: desconhecido")
    sock.close()

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

def main():
    print(f"Iniciando scan no alvo: {target}")
    for port in port_range:
        queue.put(port)

   
    thread_list = []
    for _ in range(100):  
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    
    for thread in thread_list:
        thread.join()

    print("Scan concluído!")

if __name__ == "__main__":
    main()
