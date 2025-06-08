from dataclasses import dataclass
from card import Card, Deck
from typing import Literal

INIT_CARDS = 5


class Player:
    name: str
    cards: list[Card] = []

    def __init__(self, name: str):
        self.name = name
        self.cards = []


class Game:
    player: list[Player] = []
    deck: Deck = Deck()
    current_state: Literal["init", "playing", "end"] = "init"
    current_player: int = 0
    highest = 0
    reverted = False

    def public_info(self) -> dict:
        return {
            "current_player": self.current_player,
            "highest": self.highest,
            "reverted": self.reverted,
            "current_state": self.current_state,
            "players": [
                {"name": player.name, "cards_num": len(player.cards)}
                for player in self.player
            ],
        }

    def cmp(self, num1: int, num2: int) -> bool:
        if num2 == 0:
            return True
        if self.reverted:
            return num1 < num2
        return num1 > num2

    def __init__(self, player_names: list[str]):
        self.player = [Player(name) for name in player_names]
        self.deck.shuffle()
        for player in self.player:
            player.cards = [self.deck.draw() for _ in range(INIT_CARDS)]
        self.current_state = "playing"

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.player)

    def end_game(self):
        assert not self.player[self.current_player].cards
        print(
            f"Player {self.player[self.current_player].name} has no cards left. Game over!"
        )

    # TODO: Implement the game logic for playing cards, dropping cards, and checking win conditions.
    def play_cards(self, cards: list[Card], value: int) -> bool:
        """Play a list of cards from the current player's hand"""
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")
        if not cards:
            raise ValueError("No cards to play")

        if not self.check_enough(cards):
            return False
        self.check_win()

    def check_enough(self, cards: list[Card]) -> bool:
        def count(card: list[Card]) -> list[int]:
            cnt = [0] * 14
            for c in cards:
                cnt[c.rank] += 1
            return cnt

        cur = count(self.player[self.current_player].cards)
        played = count(cards)
        for i in range(1, 14):
            if cur[i] < played[i]:
                return False
        return True

    def drop_card(self, card: Card):
        """Drop a card from the current player's hand"""
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")
        if card not in self.player[self.current_player].cards:
            raise ValueError("Card not in player's hand")

        self.player[self.current_player].cards.remove(card)
        self.check_win()

    def check_win(self):
        if not self.player[self.current_player].cards:
            self.current_state = "end"
            self.end_game()

    def play_card(self, card: Card):
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")
        if card not in self.player[self.current_player].cards:
            raise ValueError("Card not in player's hand")

        if self.cmp(card.rank, self.highest):
            self.highest = card.rank
            self.next_player()
            # TODO: add side effect for card played
        else:
            raise ValueError(
                f"Card rank is not higher({self.reverted}) than the current highest."
            )
