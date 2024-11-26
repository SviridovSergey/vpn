import asyncio
import sys
from scapy.layers.inet import IP, TCP

'''import subprocess
from scapy.layers.l2 import Ether'''
'''from scapy.all import send
'''
async def send_packet(writer, packet):
    writer.write(bytes(packet))
    await writer.drain()

async def client(server_ip, server_port):
    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)

        while True:
            # Создаем пакет с использованием IP и TCP
            pkt = IP(dst=server_ip) / TCP(dport=server_port, flags="S")
            await send_packet(writer, pkt)
            print(f"Отправлен пакет: {pkt.summary()}")
            await asyncio.sleep(1)  # Задержка между отправками пакетов

            # Проверка ввода пользователя для выхода
            quit = input("Для выхода введите '+': ")
            if quit == '+':
                break

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python client.py <ip_адрес_сервера> <порт_сервера>")
        sys.exit(1)
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    asyncio.run(client(server_ip, server_port))