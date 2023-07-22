from card import Card
from card_compose import get_best_compose_type


class User:
    def __init__(self, name):
        self.cards = []
        self.common_cards = []
        self.name = name

    def format_cards(self):
        return Card.format_cards(self.cards)

    def receive_card(self, card):
        self.cards.append(card)

    def get_all_possible_type(self):
        return get_best_compose_type(self.cards, self.common_cards)
