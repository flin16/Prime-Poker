import asyncio
from game import Game
from client import PORT  # Importing PORT from client.py
from dataclasses import dataclass
import lib
import parser

players_names = []
queue = asyncio.Queue()
queue_lock = asyncio.Lock()
G = None


@dataclass
class Message:
    sender: str
    content: str


async def send_game_state(writer):
    peername = str(writer.get_extra_info("peername"))
    while True:
        if G:
            game_state = G.public_info()
            game_state["your_hand"] = G.get_player(peername).cards
            writer.write(str(game_state).encode())
            await writer.drain()
        await asyncio.sleep(1)  # Adjust the frequency of updates as needed


def append_player(name: str) -> str:
    players_names.append(name)
    return name


async def handle_client(reader, writer):
    peername = writer.get_extra_info("peername")
    peername = append_player(str(peername))
    print("New client connected:", peername)
    players_names.append(writer)
    task = asyncio.create_task(send_game_state(writer))
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            async with queue_lock:
                queue.put_nowait(Message(sender=peername, content=message))
    finally:
        task.cancel()
        await task
        print("Client disconnected")
        writer.close()


async def process_queue():
    while True:
        message = await queue.get()
        content = message.content.strip()
        sender = message.sender
        if content is None:
            continue
        if content.startswith("s"):
            global G
            if G is None:
                G = Game(players_names)
        elif content.startswith("c"):
            if G is None:
                players_names[players_names.index(sender)] = content[1:].strip()
        else:
            if G is None:
                continue
            expr = content.replace(" ", "")
            if not parser.is_valid_input(expr):
                continue
            cards = lib.filter_numbers(expr)
            value = parser.evaluate_expression(expr)
            if value is None:
                continue
            if G.play_cards(cards, value):
                print(f"Player {sender} played cards: {cards} with value {value}")


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PORT)
    asyncio.create_task(process_queue())
    print(f"Server started on port { PORT }")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
