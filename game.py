import random

TABLE = ['GU', 'CHOKI', 'PA']


class Player():

    def __init__(self, name):
        self.name = name
        self.cards = [2, 2, 2]  # GU, CHOKI, PA
        self.star = 3
        self.results = [0, 0, 0]  # win, lose, draw

    def win(self):
        self.results[0] += 1
        self.star += 1

    def lose(self):
        self.star -= 1
        self.results[1] += 1

    def draw(self):
        self.results[2] += 1


def init_game(name1, name2):
    p1 = Player(name1)
    p2 = Player(name2)
    return p1, p2


def is_on(player1, player2):
    return (player1.star > 0 and player2.star > 0 and
            sum(player1.cards) > 0 and sum(player2.cards) > 0)


def judge_janken(player1, choice1, player2, choice2):
    n = (choice1 - choice2 + 3) % 3
    if n == 2:    # win
        player1.win()
        ret1 = 'WIN'
        player2.lose()
        ret2 = 'LOSE'
    elif n == 1:  # lose
        player1.lose()
        player2.win()
        ret1 = 'LOSE'
        ret2 = 'WIN'
    else:         # draw
        player1.draw()
        player2.draw()
        ret1 = 'DRAW'
        ret2 = 'DRAW'
    return ret1, ret2


# ゲーム本体
def main():

    name1 = 'YOU'
    name2 = 'CPU'
    you, cpu = init_game(name1, name2)

    rounds = 1

    while is_on(you, cpu):

        print(f'--- ROUND {rounds} ---')
        print(f'STAR: {"★ " * you.star}')
        print()

        # プレイヤーの選択
        print('Please choice.')
        for i in range(3):  # 手持ち表示
            print(f'{i + 1}.{TABLE[i]}: {"■ " * you.cards[i]}')
        choice = input('Your choice -> ')
        print()

        # 入力値判定
        try:
            choice = int(choice) - 1
            if you.cards[choice] <= 0:
                raise Exception
            else:
                you.cards[choice] -= 1
        except Exception:
            print('--- Invalid Choice! ---\n')
            continue

        # CPUの選択
        cpuchoice = random.randint(0, 2)
        while cpu.cards[cpuchoice] == 0:
            cpuchoice = random.randint(0, 2)
        cpu.cards[cpuchoice] -= 1

        # 選択カード表示
        print(f'{you.name}: \"{TABLE[choice]}\"')
        print(f'{cpu.name}: \"{TABLE[cpuchoice]}\"')

        # 勝敗判定
        print(judge_janken(you, choice, cpu, cpuchoice)[0])

        rounds += 1
        print()

    # 結果表示
    print('=========')
    print('GAME OVER')

    if you.star == cpu.star:  # draw
        print('DRAW')
    else:    # win, lose
        winner = you if you.star > cpu.star else cpu
        print('WINNER: {}'.format(winner.name))

    results = you.results
    print('your result')
    print(f'win: {results[0]}, lose: {results[1]}, draw:{results[2]}')


if __name__ == '__main__':
    main()
