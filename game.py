from card import Card, Deck
from typing import Literal, cast

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
            return num1 > 0
        if self.reverted:
            return num1 < num2
        return num1 > num2

    def __init__(self, player_names: list[str]):
        self.player = [Player(name) for name in player_names]
        self.deck.shuffle()
        for player in self.player:
            player.cards = [self.deck.draw() for _ in range(INIT_CARDS)]
        self.current_state = "playing"

    def get_current_hand(self) -> list[Card]:
        """Get the current player's hand"""
        return self.player[self.current_player].cards

    def get_player(self, name: str) -> Player:
        """Get a player by name"""
        for player in self.player:
            if player.name == name:
                return player
        raise ValueError(f"Player {name} not found")

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.player)

    def end_game(self):
        assert not self.player[self.current_player].cards
        print(
            f"Player {self.player[self.current_player].name} has no cards left. Game over!"
        )

    # TODO: add 57 and 1728 logic
    def play_cards(self, cards: list[Card] | list[int], value: int) -> bool:
        """Play a list of cards from the current player's hand"""
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")
        if not cards:
            raise ValueError("No cards to play")
        if not self.cmp(value, self.highest):
            return False
        if isinstance(cards[0], int):
            cards = [Card("JOKER", rank) for rank in cards]
        cards = cast(list[Card], cards)
        if not self.check_enough(cards):
            return False
        for card in cards:
            self.play_card(card)
        if not self.check_win():
            self.next_player()
        return True

    def check_enough(self, cards: list[Card]) -> bool:
        def count(cards: list[Card]) -> list[int]:
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

    def check_win(self) -> bool:
        if not self.player[self.current_player].cards:
            self.current_state = "end"
            self.end_game()
            return True
        return False

    def play_card(self, card: Card):
        # Do not add side effects to the card, just remove it from the player's hand
        if self.current_state != "playing":
            raise ValueError("Game is not in playing state")

        for card in self.player[self.current_player].cards:
            if card.rank == card.rank:
                self.player[self.current_player].cards.remove(card)
                break


def test1():
    game = Game(["Alice", "Bob"])
    game.player[0].cards = [Card("♠️", 1), Card("♥️", 3)]
    print(game.public_info())
    print(game.play_cards([Card("♠️", 3)], 3))
    print(game.public_info())


if __name__ == "__main__":
    test1()
