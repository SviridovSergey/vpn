import asyncio
import random
import requests

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Подключение от {addr!r}")
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            print(f"Получено от клиента: {data}")

            # Изменяем IP-адрес клиента на случайный
            random_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            print(f"Измененный IP-адрес: {random_ip}")

            # Пересылаем пакет на прокси-сервер
            '''proxy_host = 'localhost'
            proxy_port = 8080
            proxies = {
                'http': f'http://{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_host}:{proxy_port}'
            }
            try:
                response = requests.post('http://example.com', data=data, proxies=proxies)
                response.raise_for_status()
                print(f"Ответ от прокси-сервера: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при отправке на прокси-сервер: {e}")'''

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Клиент {addr!r} отключился.")

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())