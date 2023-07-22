import functools
import itertools as it
from card import Card, CardType


def group_by_value(value_list):
    result = {}
    for v in value_list:
        result.setdefault(str(v), 0)
        result[str(v)] = result[str(v)] + 1
    return result


# 按照数值分组
def get_cards_group_value(cards):
    card_values = list(map(lambda card: card.int_value, cards))
    group_value = group_by_value(card_values)
    return group_value


def cmp(a, b):
    if a[1] != b[1]:
        return b[1] - a[1]
    return int(b[0]) - int(a[0])


# 按照数值分组，并按照分组大小排序.如果分组大小一样，再按照数值排序
def group_and_sort(cards):
    group_value = get_cards_group_value(cards)
    return list(map(lambda v: int(v[0]), sorted(group_value.items(), key=functools.cmp_to_key(cmp))))


# 降序排列
def compare(a, b):
    if a == b:
        return 0
    return b - a


def value_list_compare(value_list, another_value_list):
    for i in range(len(value_list)):
        value = value_list[i]
        another_value = another_value_list[i]
        if value == another_value:
            continue
        return 1 if value > another_value else -1
    return 0


# 升序排列
def compare_between_compose_type(compose_type, another):
    if compose_type.rank == another.rank:
        return compose_type.self_compare(another)
    return -1 if compose_type.rank > another.rank else 1


# 皇家同花顺  > 同花顺 Straight Flush > 四条 > 葫芦 > 同花 > 顺子 > 三条 > 两对 > 一对 > 高牌

class ComposeTypeBase:

    def compare(self, another):
        return compare_between_compose_type(self, another)

    def __repr__(self):
        return f'牌型: {self.name} 排名: {self.rank + 1} 详情: {Card.format_cards(self.cards)}'


# 皇家同花顺
class BestStraightFlush(ComposeTypeBase):
    name = '皇家同花顺'
    rank = 0

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        if not StraightFlush.satisfy(cards):
            return False
        sorted_cards = sorted(cards, key=lambda x: x.int_value)
        card_values = list(map(lambda card: card.int_value, sorted_cards))
        if card_values != [10, 11, 12, 13, 14]:
            return False
        return True

    # 皇家同花顺一样大
    def self_compare(self, another):
        return 0


# 同花顺
class StraightFlush(ComposeTypeBase):
    name = '同花顺'
    rank = 1

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        return Flush.satisfy(cards) and Straight.satisfy(cards)

    def self_compare(self, another):
        return HighCard.normal_compare(self.cards, another.cards)


# 四条
class FourOfAKind(ComposeTypeBase):
    name = '四条'
    rank = 2

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        group_value = get_cards_group_value(cards)
        for count in group_value.values():
            if count == 4:
                return True
        return False

    def self_compare(self, another):
        value_list = group_and_sort(self.cards)
        another_value_list = group_and_sort(another.cards)
        return value_list_compare(value_list, another_value_list)


# 葫芦
class FullHouse(ComposeTypeBase):
    name = '葫芦'
    rank = 3

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        return ThreeOfAKind.satisfy(cards) and OnePair.satisfy(cards)

    def self_compare(self, another):
        value_list = group_and_sort(self.cards)
        another_value_list = group_and_sort(another.cards)
        return value_list_compare(value_list, another_value_list)


# 同花
class Flush(ComposeTypeBase):
    name = '同花'
    rank = 4

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        type_name = None
        for card in cards:
            if type_name is None:
                type_name = card.type_name
                continue
            if type_name != card.type_name:
                return False
        return True

    def self_compare(self, another):
        return HighCard.normal_compare(self.cards, another.cards)


# 顺子
class Straight(ComposeTypeBase):
    name = '顺子'
    rank = 5

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        sorted_cards = sorted(cards, key=lambda x: x.int_value)
        card_values = list(map(lambda card: card.int_value, sorted_cards))
        if card_values == [2, 3, 4, 5, 14]:
            return True
        last_value = None
        for value in card_values:
            if last_value is None:
                last_value = value
                continue
            if value - last_value != 1:
                return False
            last_value = value
        return True

    def self_compare(self, another):
        return HighCard.normal_compare(self.cards, another.cards)


# 三条
class ThreeOfAKind(ComposeTypeBase):
    name = '三条'
    rank = 6

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        group_value = get_cards_group_value(cards)
        for count in group_value.values():
            if count == 3:
                return True
        return False

    def self_compare(self, another):
        value_list = group_and_sort(self.cards)
        another_value_list = group_and_sort(another.cards)
        return value_list_compare(value_list, another_value_list)

# 两对
class TwoPairs(ComposeTypeBase):
    name = '两对'
    rank = 7

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        group_value = get_cards_group_value(cards)
        pair_count = 0
        for count in group_value.values():
            if count == 2:
                pair_count += 1
        return pair_count == 2

    def self_compare(self, another):
        value_list = group_and_sort(self.cards)
        another_value_list = group_and_sort(another.cards)
        return value_list_compare(value_list, another_value_list)


# 一对
class OnePair(ComposeTypeBase):
    name = '一对'
    rank = 8

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy(cards):
        group_value = get_cards_group_value(cards)
        pair_count = 0
        for count in group_value.values():
            if count == 2:
                pair_count += 1
        return pair_count == 1

    def self_compare(self, another):
        value_list = group_and_sort(self.cards)
        another_value_list = group_and_sort(another.cards)
        return value_list_compare(value_list, another_value_list)


# 高牌
class HighCard(ComposeTypeBase):
    name = '高牌'
    rank = 9

    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def satisfy():
        return True

    def self_compare(self, another):
        card_values = sorted(list(map(lambda card: card.int_value, self.cards)), key=functools.cmp_to_key(compare))
        another_card_values = sorted(list(map(lambda card: card.int_value, another.cards)), key=functools.cmp_to_key(compare))
        return value_list_compare(card_values, another_card_values)

    @staticmethod
    def normal_compare(cards, another):
        card_values = sorted(list(map(lambda card: card.int_value, cards)), key=functools.cmp_to_key(compare))
        another_card_values = sorted(list(map(lambda card: card.int_value, another)), key=functools.cmp_to_key(compare))
        return value_list_compare(card_values, another_card_values)


match_list = [BestStraightFlush, StraightFlush, FourOfAKind, FullHouse, Flush, Straight, ThreeOfAKind, TwoPairs,
              OnePair]


# 获取牌型
def get_compose_type(cards):
    for m in match_list:
        if m.satisfy(cards):
            return m(cards)
    return HighCard(cards)


# 获取最大可能牌型
def get_best_compose_type(user_cards, common_cards):
    possible_list = []
    for item in it.combinations(common_cards, 3):
        all = list(item)
        all.extend(user_cards)
        possible_list.append(all)
    compose_type_list = [get_compose_type(cards) for cards in possible_list]
    rank_list = sorted(compose_type_list, key=functools.cmp_to_key(compare_between_compose_type))
    return rank_list


if __name__ == '__main__':
    cards = [Card(CardType(2).name, '8'), Card(CardType(1).name, 'a'), Card(CardType(1).name, 'k'),
             Card(CardType(3).name, '5'), Card(CardType(1).name, '4')]
    another = [Card(CardType(2).name, '6'), Card(CardType(1).name, '6'), Card(CardType(4).name, '4'),
               Card(CardType(3).name, '4'), Card(CardType(1).name, '5')]

    compose_type = get_compose_type(cards)
    another = get_compose_type(another)
    print(compose_type)
    print(another)
    print(compose_type.compare(another))
