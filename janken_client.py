#!/usr/bin/python3
import socket
import pickle


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
    print('connected to the server')

    TABLE = pickle.loads(soc.recv(1024))
    print(TABLE)

    name1 = input('input your name -> ')
    send_pickle(soc, name1)

    name2 = pickle.loads(soc.recv(1024))
    print(f'start LimitedJanken with {name2}')

    while True:
        send_pickle(soc, 'OK')
        rounds, star, cards = pickle.loads(soc.recv(1024))

        # indicate status
        print(f'--- ROUND {rounds} ---')
        print(f'STAR: {"★ " * star}')
        print()

        print('Please choice.')
        # indicate hands
        for i in range(3):
            print(f'{i + 1}.{TABLE[i]}: {"■ " * cards[i]}')

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
        print(judge)

        ison = pickle.loads(soc.recv(1024))
        if not ison:
            break

    print('=========')
    print('GAME OVER')

    game_result, results = pickle.loads(soc.recv(1024))
    print(game_result)
    print('your result')
    print(f'win: {results[0]}, lose: {results[1]}, draw:{results[2]}')
    s.close()


if __name__ == '__main__':
    main()
