#!/usr/bin/python3
import socket
import pickle
import messages

result_aa = messages.result_aa


# dump and send pickle
def send_pickle(soc, obj):
    dump = pickle.dumps(obj)
    datalen = len(dump)
    totalsent = 0
    while totalsent < datalen:
        sent = soc.send(dump[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname('localhost')
    port = 9999

    soc.connect((host, port))
    print('Connected to the server.')

    TABLE = pickle.loads(soc.recv(1024))

    hands_emoji = {
        TABLE[0]: '✊',
        TABLE[1]: '✌️',
        TABLE[2]: '🖐'
    }

    name1 = input('Input your name -> ')
    send_pickle(soc, name1)

    name2 = pickle.loads(soc.recv(1024))
    print(f'Start LimitedJanken with {name2}.')

    while True:
        send_pickle(soc, 'OK')
        rounds, star, cards = pickle.loads(soc.recv(1024))

        # indicate status
        print()
        print(f'--- ROUND {rounds} ---')
        print(f'STAR: {"⭐️ " * star}')
        print()

        print('Pick your card.')
        # indicate hands
        for i in range(3):
            hand = TABLE[i]
            print(f'{i + 1}.{hand}{hands_emoji[hand]} : {"■ " * cards[i]}')

        while True:
            # select a card
            choice = input('Your choice -> ')
            # validation
            try:
                choice = int(choice) - 1
                if cards[choice] <= 0:
                    raise Exception
            except Exception:
                print('--- Invalid Choice! ---\n')
                continue
            break
        print()

        send_pickle(soc, choice)
        judge, choice1, choice2 = pickle.loads(soc.recv(1024))
        print(f'{name1}: \"{TABLE[choice1]}\"')
        print(f'{name2}: \"{TABLE[choice2]}\"')
        print()
        print(judge)

        ison = pickle.loads(soc.recv(1024))
        if not ison:
            break

    send_pickle(soc, 'OK')
    print()
    print('=========')
    print(result_aa['GAME OVER'])
    print()

    game_result, results = pickle.loads(soc.recv(1024))
    print(result_aa[game_result])
    print('Your result...')
    print(f'Win: {results[0]}, Lose: {results[1]}, Draw:{results[2]}')
    soc.close()


if __name__ == '__main__':
    main()
