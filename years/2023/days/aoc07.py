from collections import Counter
from enum import IntEnum
from util import lmap


class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

class CamelHand:
    def __init__(self, cards, bid):
        self.__cards = cards
        self.__bid = bid

    @classmethod
    def from_string(cls, s):
        cards, bid = s.split()
        bid = int(bid)
        return cls(cards, bid)

    @property
    def bid(self):
        return self.__bid

    def __get_card_value(self, card, joker_wildcard):
        if card.isnumeric():
            return int(card)
        return {
            "T": 10,
            "J": 0 if joker_wildcard else 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }[card]

    def __get_hand_type(self, joker_wildcard):
        card_counter = Counter(self.__cards)
        jokers = 0
        if joker_wildcard:
            jokers = card_counter["J"]
            card_counter["J"] = 0
        most = card_counter.most_common(2)
        first = most[0][1]
        second = most[1][1] if len(most) > 1 else 0

        if first + jokers == 5:
            return HandType.FIVE_OF_A_KIND
        if first + jokers == 4:
            return HandType.FOUR_OF_A_KIND
        if first + jokers == 3:
            return HandType.FULL_HOUSE if second == 2 else HandType.THREE_OF_A_KIND
        if first == 2 and second == 2:
            return HandType.TWO_PAIR
        if first + jokers == 2:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def sort_key(self, joker_wildcard=False):
        return (self.__get_hand_type(joker_wildcard), *(self.__get_card_value(card, joker_wildcard) for card in self.__cards))


def solve(data):
    hands = lmap(CamelHand.from_string, data)
    hands.sort(key=lambda h: h.sort_key())
    ans1 = sum((i + 1) * hand.bid for i, hand in enumerate(hands))
    hands.sort(key=lambda h: h.sort_key(joker_wildcard=True))
    ans2 = sum((i + 1) * hand.bid for i, hand in enumerate(hands))
    return ans1, ans2
