import asyncio
from game import Game
from client import PORT  # Importing PORT from client.py

G = Game(["Alice", "Bob", "Charlie"])  # Example player names


async def send_game_state(writer):
    while True:
        game_state = str(G.public_info())
        writer.write(game_state.encode())
        await writer.drain()
        await asyncio.sleep(1)  # Adjust the frequency of updates as needed


async def handle_client(reader, writer):
    print("Client connected")
    task = asyncio.create_task(send_game_state(writer))
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            print(f"Received: {message}")
            writer.write(data)
            await writer.drain()
    finally:
        task.cancel()
        await task
        print("Client disconnected")
        writer.close()


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PORT)
    print(f"Server started on port { PORT }")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
