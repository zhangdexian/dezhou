import functools
import random
from user import User
from logger import log
from card import Card, CardType
from card_compose import compare_between_compose_type

value_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K']


def users_compare(a, b):
    return compare_between_compose_type(a['card_type'], b['card_type'])


class CardGame:
    users = []
    all_cards = [Card(type_name.name, value) for value in value_list for type_name in CardType]
    common_cards = []

    def __init__(self):
        random.shuffle(self.all_cards)

    def reset(self):
        self.users = []
        self.common_cards = []

    def add_user(self, name):
        self.users.append(User(name))
        return self

    def start(self):
        for i in range(2):
            log.info(f'第{i + 1}轮发牌')
            for user in self.users:
                card = self.all_cards.pop(0)
                user.receive_card(card)
                log.info(f'玩家{user.name}获得第{len(user.cards)}张牌{card.format()}')
        log.info('玩家发牌完毕')
        for i in range(3):
            self.all_cards.pop(0)
            self.common_cards.append(self.all_cards.pop(0))
        log.info('翻牌发牌完毕')
        self.all_cards.pop(0)
        self.common_cards.append(self.all_cards.pop(0))
        log.info('转牌发牌完毕')
        self.all_cards.pop(0)
        self.common_cards.append(self.all_cards.pop(0))
        log.info('河牌发牌完毕')
        log.info(f'公牌为{Card.format_cards(self.common_cards)}')
        for user in self.users:
            user.common_cards = self.common_cards
            user.get_all_possible_type()

    def print_result(self):
        user_cards_list = []
        for user in self.users:
            best_compose_type = user.get_all_possible_type()[-1]
            log.info(f'用户{user.name}的手牌为: {user.format_cards()},最大牌型为{best_compose_type}')
            user_cards_list.append({"user": user, "card_type": best_compose_type})
        winner_info = sorted(user_cards_list, key=functools.cmp_to_key(users_compare))[-1]
        log.info(f'用户{winner_info["user"].name}胜！')

    def print_all_cards(self):
        log.info(Card.format_cards(self.all_cards))


if __name__ == '__main__':
    game = CardGame()
    game.add_user("张三").add_user("李四").add_user("王五").start()
    game.print_result()
