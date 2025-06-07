import random

SUITS = ["♠️", "♥️", "♦️", "♣️"]
JOKERS = "🤡"
RANKS = list(range(1, 14))  # 1 to 13 representing Ace to King


class Card:
    suit: str
    rank: int

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"Card({self.suit!r}, {self.rank!r})"

    def __eq__(self, other):
        return (
            isinstance(other, Card)
            and self.suit == other.suit
            and self.rank == other.rank
        )


class Deck:
    cards: list[Card]

    def __init__(self, jokers=False):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        if jokers:
            self.cards.append(Card(JOKERS, 0))  # Joker represented by rank 0
            self.cards.append(Card(JOKERS, 0))  # Second Joker

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()


def test_deck():
    # Example usage
    deck = Deck(jokers=True)
    print(f"Deck created with {len(deck.cards)} cards.")
    deck.shuffle()
    print("Deck shuffled.")

    drawn_card = deck.draw()
    print(f"Drew card: {drawn_card}")

    print(f"Cards left in the deck: {len(deck.cards)}")
    print("Remaining cards:")
    for card in deck.cards:
        print(card)


if __name__ == "__main__":
    ...
