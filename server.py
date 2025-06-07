import asyncio

from client import PORT  # Importing PORT from client.py


async def handle_client(reader, writer):
    print("Client connected")
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received: {message}")
        writer.write(data)
        await writer.drain()
    print("Client disconnected")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PORT)
    print(f"Server started on port { PORT }")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
