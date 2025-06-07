from dataclasses import dataclass
from card import Card, Deck
from typing import Literal

INIT_CARDS = 5


@dataclass
class Player:
    name: str
    cards: list[Card] = []


class Game:
    player: list[Player] = []
    deck: Deck = Deck()
    current_state: Literal["init", "playing", "end"] = "init"
    current_player: int = 0
    highest = 0
    reverted = False

    def cmp(self, num1: int, num2: int) -> bool:
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

    def drop_card(self, card: Card):
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")
        if card not in self.player[self.current_player].cards:
            raise ValueError("Card not in player's hand")

        self.player[self.current_player].cards.remove(card)
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
