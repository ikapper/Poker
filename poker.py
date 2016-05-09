#!/usr/bin/env python3

import random

def main():
    """Terminal上でポーカーを再現。ダブルアップはなし。
    """
    poker = Poker()
    # test()
    """
    標準入出力を利用して、ゲームを行う
    ループで回せばいい
    終了の文字も指定する
    ゲームの流れは、
    スタート->dealされた札が5枚表示される->holdする札を選択する->
    ->再びdealする->役を判定->ゲームの結果処理->スタートに戻る
    ユーザーができることは、
    holdする札を選ぶ。結果表示後続けるか選ぶ。
    の2つ
    """
    print('How to hold card? --> Please input "134".')
    print('Input "n" to exit.')
    coins = 1000
    print('conis:', coins)
    while True:
        bet = 50
        coins -= bet
        print('bet:', bet)
        deals = poker.gen_display_str()
        print('Cards dealt:', deals)
        # listとして受け取って数字だけを格納する
        inp = list(input('Which cards do you hold? -> '))
        holds = []
        flag_exit = False
        for s in inp:
            if s == 'n':
                flag_exit = True
            if s.isdigit():
                num = int(s)
                if num > 0 and num < 6:
                    holds.append(num - 1) # 実際のインデックスは-1する
        if flag_exit == True:
            print('Exit.')
            break;
        holds = list(set(holds))
        poker.change_cards(holds)
        hand = poker.judge_deals()
        print('Cards dealt:', poker.gen_display_str(), '---->', hand)
        gain = poker.gain(bet, hand)
        coins += gain
        print('You gained', gain, 'coins.')
        print('coins:',coins)
        poker.shuffle()

def test():
    poker = Poker()
    print('-----Non-Joker TEST-----')
    # non-Joker
    poker.deals = ['S1','S10','S11','S13','S12']
    print('RoyalTest:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H12','C12','S12','D12','Joker1']
    print('5 card:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S3','S4','S5','S6','S7']
    print('Straigth Flush:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D10','S10','H10','C10','S12']
    print('4 card:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S1','D1','S11','C11','H11']
    print('FullHouse:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S4','S2','S6','S1','S12']
    print('Flush:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D9','C10','C11','H13','S12']
    print('Straight:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D10','S10','C13','C10','S12']
    print('Three of a Kind:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H10','S10','H5','D11','C5']
    print('2 pair:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H10','S10','H5','D11','C7']
    print('1 pair:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H6','S10','H13','D11','C5']
    print('No pair:', poker.judge_deals(), '-->', poker.deals)
    print('-----   END   -----')

    
    print('-----Contains Joker TEST-----')
    # contains Joker
    poker.deals = ['S1','S10','S11','Joker1','S12']
    print('RoyalTest:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H12','C12','S12','D12','Joker1']
    print('5 card:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S3','Joker1','S5','S6','S7']
    print('Straigth Flush:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D10','Joker1','H10','C10','S12']
    print('4 card:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S1','D1','S11','Joker1','H11']
    print('FullHouse:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['S4','S2','Joker1','S1','S12']
    print('Flush:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D9','Joker1','C11','H13','S12']
    print('Straight:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['D10','Joker1','C13','C10','S12']
    print('Three of a Kind:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H10','Joker1','H5','D11','C5']
    print('2 pair:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['Joker1','S10','H5','D11','C7']
    print('1 pair:', poker.judge_deals(), '-->', poker.deals)
    poker.deals = ['H6','S10','Joker1','D11','C5']
    print('Must not be No pair:', poker.judge_deals(), '-->', poker.deals)
    print('-----   END   -----')

    
class Poker:
    """1ゲーム分のポーカーの状態を管理する
    なお、1人分しか扱っていないのであしからず
    Jokerは4枚まで対応する（デフォルトは1枚）
    """
    # 上から上位
    CONST_ROYAL_STRAIGHT_FLUSH = 'ROYAL STRAIGHT FLUSH'
    CONST_5_CARDS = 'FIVE CARD'
    CONST_STRAIGHT_FLUSH = 'STRAIGHT FLUSH'
    CONST_4_CARDS = 'FOUR CARD'
    CONST_FULL_HOUSE = 'FULL HOUSE'
    CONST_FLUSH = 'FLUSH'
    CONST_STRAIGHT = 'STRAIGHT'
    CONST_3_CARDS = 'THREE OF A KIND'
    CONST_2_PAIR = 'TWO PAIR'
    CONST_1_PAIR = 'ONE PAIR'    
    CONST_NO_PAIR = 'NO PAIR'
    
    PAIR = {CONST_ROYAL_STRAIGHT_FLUSH  : 50000,
            CONST_5_CARDS               : 1000,
            CONST_STRAIGHT_FLUSH        : 500,
            CONST_4_CARDS               : 50,
            CONST_FULL_HOUSE            : 30,
            CONST_FLUSH                 : 20,
            CONST_STRAIGHT              : 15,
            CONST_3_CARDS               : 2,
            CONST_2_PAIR                : 1,
            CONST_1_PAIR                : 0,
            CONST_NO_PAIR               : 0,
            }
    
    def __init__(self, jokers=1):
        """山札cardsを生成して、配る分dealsを用意する
        cardsとdealsを足すと全カードになる
        Jokerは4枚まで想定している
        """
        self.num_joker = jokers
        # カード群を生成
        bundle = [suit + str(i) for suit in ('S', 'C', 'H', 'D') for i in range(1, 14)]
        bundle.extend('Joker{0}'.format(i + 1) for i in range(self.num_joker))
        random.shuffle(bundle)
        self.cards = bundle
        self.deals = self.pickTop(5)
                
    def shuffle(self):
        """配った分と山札を合わせてシャッフルしたあと、配り直す
        """
        self.cards.extend(self.deals)
        random.shuffle(self.cards)
        self.deals = self.pickTop(5)
    
    def gain(self, bet, hand):
        multiply = self.PAIR[hand]
        return bet * multiply
    
    
    def pickTop(self, n):
        """先頭からn個popする --> list
        """
        if n > len(self.cards) - 1:
            n = len(self.cards) - 1
        elif n < 0:
            n = 0
        result = [self.cards.pop(0) for i in range(n)]
        return result
    
    def change_cards(self, holds=[0,1,2,3,4]):
        """dealsの左から数えた時のholdするindexのリスト。最左を1として、5まで考えられる
        デフォルトは全ホールド。dealsが変化する。抜いたカードは山札に戻す
        """
        # holdしないインデックスはpopしてすぐに新しいのをinsertする
        nonhold = [i for i in range(5)]
        for idx in holds:
            nonhold.remove(idx)
        for idx in nonhold:
            pop = self.deals.pop(idx)
            self.deals.insert(idx, self.cards.pop(0))
            self.cards.append(pop) # 山札の下に持っていく
            
    def judge_deals(self):
        """呼ばれた時点でのdealsで役判定する
        return a corresponding hand
        """
        # まずはスートとランクに分ける
        suits = []
        ranks = []
        jokers = 0
        for deal in self.deals:
            if deal.startswith('Joker'):
                jokers += 1
                continue
            suits.append(deal[:1]) # str
            ranks.append(int(deal[1:])) # int
        result = self.judge(suits, ranks, jokers)
        return result
    
    def judge(self, suits, ranks, jokers=0):
        """jokers: number of jokers
        テストにも使う
        return a corresponding hand
        """

        # ここから判定を開始するが、ロイヤルストレートフラッシュは後回しにしてストレートとフラッシュを判定する
        # 高い役から順に評価していけばいい
        isRoyal = self._isRoyal(suits, ranks, jokers)
        if isRoyal: return self.CONST_ROYAL_STRAIGHT_FLUSH
        
        isFive = self._is5Cards(ranks, jokers)
        if isFive: return self.CONST_5_CARDS
        
        isStraight = self._isStraight(ranks, jokers)
        isFlush = self._isFlush(suits, jokers)
        if isStraight and isFlush: return self.CONST_STRAIGHT_FLUSH
        
        isFour = self._is4Cards(ranks, jokers)
        if isFour: return self.CONST_4_CARDS
        
        isFullHouse = self._isFullHouse(ranks, jokers)
        if isFullHouse: return self.CONST_FULL_HOUSE
        
        if isFlush: return self.CONST_FLUSH
        
        if isStraight: return self.CONST_STRAIGHT
        
        isThree = self._is3Cards(ranks, jokers)
        if isThree: return self.CONST_3_CARDS
        
        is2Pair = self._is2Pair(ranks, jokers)
        if is2Pair: return self.CONST_2_PAIR
        
        is1Pair = self._is1Pair(ranks, jokers)
        if is1Pair: return self.CONST_1_PAIR
        
        return self.CONST_NO_PAIR
        
    
    def _isRoyal(self, suits, ranks, num_jokers=0):
        """ロイヤルストレートフラッシュかどうか
        """
        sset = set(suits)
        if not ('S' in sset and self._isFlush(suits, num_jokers)):
            return False
        # print('isRoyal. Suit OK')
        sorted_ranks = sorted(ranks)
        rset = set(ranks)
        for r in rset:
            if not r in (1,10,11,12,13):
                return False
        # print('isRoyal. Rank range OK')
        # 上をくぐり抜けてくれば、10~13と1かJokerのランクで構成されるといえる
        # これでストレートになればOK
        return self._isStraight(sorted_ranks, num_jokers)
        
    
    def _isStraight(self, ranks, num_jokers=0):
        sorted_ranks = sorted(ranks)
        if not 1 in sorted_ranks:
            return self.__checkStraight(sorted_ranks, num_jokers)
        else:
            # 1が含まれる時は先頭に1がある時と末尾に14をおいた時にストレートになるか調べる
            result = self.__checkStraight(sorted_ranks, num_jokers)
            # これで終わればそれはそれでいい
            if result == True:
                return True
            # 1の代わりに14を加えて確かめる
            fixed = sorted_ranks[1:]
            fixed.append(14)
            return self.__checkStraight(fixed, num_jokers)
        
    def __checkStraight(self, sorted_ranks, num_jokers=0):
        prev = -1
        straight_count = 0
        for r in sorted_ranks:
            if prev == -1:
                # first process
                prev = r
                straight_count += 1
                continue
            if r - prev != 1:
                if num_jokers > 0:
                    prev += 1
                    num_jokers -= 1
                    straight_count += 1
                    continue
            else :
                prev = r
                straight_count += 1
        if num_jokers > 0:
            straight_count += num_jokers
        return straight_count == 5
    
    def _isFlush(self, suits, num_jokers=0):
        sset = set(suits)
        # suitが1種類ならJokerの数は関係なしにFLUSH
        return len(sset) == 1
    
    def _is5Cards(self, ranks, num_jokers):
        return self.__isNCards(5, ranks, num_jokers)
    
    def _is4Cards(self, ranks, num_jokers):
        return self.__isNCards(4, ranks, num_jokers)
    
    def _is3Cards(self, ranks, num_jokers):
        return self.__isNCards(3, ranks, num_jokers)
    
    def __isNCards(self, n, ranks, num_jokers):
        ranks = sorted(ranks)
        rset = set(ranks)
        candidates = [ranks.count(r) for r in rset]
        cmax = max(candidates) + num_jokers
        return cmax == n
    
    def _isFullHouse(self, ranks, num_jokers):
        ranks = sorted(ranks)
        rset = set(ranks)
        count_list = [ranks.count(r) for r in rset]
        # [2,3]ならすぐにFULLHOUSE
        count_list = sorted(count_list)
        if count_list == [2, 3]:
            return True
        # ここまで来てFULLHOUSEになるのはJokerがないといけない
        # あまり賢くない
        try:
            first = count_list[len(count_list) - 1]
        except IndexError:
            first = 0
        try:
            second = count_list[len(count_list) - 2]
        except IndexError:
            second = 0
        # firstが3,secondが2になるまでJokerを分配する
        while first < 3:
            if num_jokers > 0:
                first += 1
                num_jokers -= 1
            else:
                break
        while second < 2:
            if num_jokers > 0:
                second += 1
                num_jokers -= 1
            else:
                break
        # second < first
        return [second, first] == [2, 3]
    
    def _is2Pair(self, ranks, num_jokers):
        ranks = sorted(ranks)
        rset = set(ranks)
        count_list = [ranks.count(r) for r in rset]
        count_list = sorted(count_list)
        if count_list == [1,2,2]:
            return True
        # FULLHOUSEと同じようにJokerを分配する
        fixed_list = []
        for c in reversed(count_list):
            while c < 2:
                if num_jokers > 0:
                    c += 1
                    num_jokers -= 1
                else:
                    break
            fixed_list.append(c)
        fixed_list = sorted(fixed_list)
        return fixed_list == [1,2,2]
    
    def _is1Pair(self, ranks, num_jokers):
        ranks = sorted(ranks)
        rset = set(ranks)
        count_list = [ranks.count(r) for r in rset]
        count_list = sorted(count_list)
        if count_list[len(count_list) - 1] > 1:
            # 重なる要素が1つでもあればTrue
            return True
        # Joker分配
        fixed = []
        for c in count_list:
            if num_jokers > 0:
                num_jokers -= 1
                c += 1
            fixed.append(c)
        return sorted(fixed).pop() > 1
    
    def hello(self):
        print('cards: {0}'.format(self.cards))
        print('deals: {0}'.format(self.gen_display_str()))
    
    def gen_display_str(self):
        """dealsを見やすい？形の文字列を返す。1,11,12,13を文字に置き換えて文字列を生成する
        """
        result = ''
        for item in self.deals:
            if item.startswith('Joker'):
                result += ', Joker'
                continue
            suit = item[:1]
            rank = item[1:]
            rank = int(rank)
            result += ', ' + suit
            if rank == 1:
                result += '-A'
            elif rank == 11:
                result += '-J'
            elif rank == 12:
                result += '-Q'
            elif rank == 13:
                result += '-K'
            else:
                result += '-' + str(rank)
        return result[2:]
    
    
if __name__ == '__main__':
    main()
    