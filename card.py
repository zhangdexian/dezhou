from enum import Enum, unique

card_value = {
    "A": 14,
    "J": 11,
    "Q": 12,
    "K": 13
}


@unique
class CardType(Enum):
    Spade = 1
    Hearts = 2
    Club = 3
    Diamond = 4


class Card:
    def __init__(self, type_name, value):
        # 花色
        self.type_name = type_name
        # 牌值
        self.value = str(value).upper()
        # 计算值
        self.int_value = card_value[self.value] if self.value in card_value else int(self.value)

    def format(self):
        return self.value + self.type_name[:1]

    @staticmethod
    def format_cards(cards):
        return ','.join(map(lambda x: x.format(), cards))