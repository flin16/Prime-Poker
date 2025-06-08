import curses
import socket
import threading
import logging

logging.basicConfig(
    filename="/tmp/client_ui.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
HOST = "127.0.0.1"
PORT = 8888

game_lines = []


def render_game_state(game_state: dict) -> list[str]:
    lines = []

    current_idx = game_state.get("current_player", -1)
    players = game_state.get("players", [])
    current_name = (
        players[current_idx]["name"] if 0 <= current_idx < len(players) else "???"
    )
    state = game_state.get("current_state", "unknown")
    highest = game_state.get("highest", "?")
    reverted = game_state.get("reverted", False)
    your_hand = game_state.get("your_hand", [])
    lines.append(f"State: {state:<12} Current Player: {current_name}")
    lines.append(f"Highest Bid: {highest:<10} Reverted: {'Yes' if reverted else 'No'}")
    lines.append("")
    lines.append("Players:")
    lines.append("┌────────────┬────────────┐")
    lines.append("│ Name       │ Cards Left │")
    lines.append("├────────────┼────────────┤")

    for i, player in enumerate(players):
        mark = " ← Your turn" if i == current_idx else ""
        display_cards = player.get("cards_num")
        if display_cards <= 5:
            display_cards = "🃏" * display_cards
        lines.append(f"│ {player['name']:<10} │ {display_cards:<10} │{mark}")

    lines.append("└────────────┴────────────┘")
    lines.append(
        your_hand and f"Your Hand: {' '.join(your_hand)}" or "Your Hand: Empty"
    )

    return lines


def recv_thread(sock):
    global game_lines
    while True:
        logging.debug(f"game_lines: {game_lines}")
        try:
            data = sock.recv(1024)
            if not data:
                break
            lines = data.decode().splitlines()
            game_lines.extend(lines)
            if len(game_lines) > 10:
                game_lines = game_lines[-10:]
        except Exception as e:
            logging.error(f"Error receiving data: {e}")
            break


def main(stdscr):
    curses.curs_set(1)
    stdscr.nodelay(False)  # 输入时阻塞
    stdscr.clear()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=recv_thread, args=(sock,), daemon=True).start()

    input_str = ""
    while True:
        stdscr.clear()

        raw = {}
        if game_lines:
            logging.debug(f"Game lines: {game_lines[-1]}")
            raw = eval(game_lines[-1])
        states = render_game_state(raw)

        for i, line in enumerate(states):
            stdscr.addstr(i, 0, line)

        height, _ = stdscr.getmaxyx()
        stdscr.addstr(height - 2, 0, "Input line:")
        stdscr.addstr(height - 1, 0, input_str)

        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (10, 13):  # Enter
            if input_str.strip().lower() == "exit":
                break
            sock.sendall((input_str.strip() + "\n").encode())
            input_str = ""
        elif ch in (8, 127):  # Backspace
            input_str = input_str[:-1]
        elif 0 <= ch <= 255:
            input_str += chr(ch)

    sock.close()


if __name__ == "__main__":
    curses.wrapper(main)
