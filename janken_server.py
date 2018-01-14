#!/usr/bin/python3
import socket
import threading
import game
import pickle


# dump and send pickle
def send_pickle(conn, obj):
    dump = pickle.dumps(obj)
    datalen = len(dump)
    totalsent = 0
    while totalsent < datalen:
        sent = conn.send(dump[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def gamethread(accept1, accept2):
    # establish a connection
    p1_conn, p1_addr = accept1
    p2_conn, p2_addr = accept2

    print(f'start {p1_addr} vs {p2_addr}')

    TABLE = game.TABLE
    send_pickle(p1_conn, TABLE)
    send_pickle(p2_conn, TABLE)

    name1 = pickle.loads(p1_conn.recv(1024))
    name2 = pickle.loads(p2_conn.recv(1024))
    p1, p2 = game.init_game(name1, name2)

    print(f'{p1_addr}: {p1.name}')
    print(f'{p2_addr}: {p2.name}')

    send_pickle(p1_conn, p2.name)
    send_pickle(p2_conn, p1.name)

    rounds = 1

    while True:
        p1_conn.recv(1024)
        send_pickle(p1_conn, [rounds, p1.star, p1.cards])
        p2_conn.recv(1024)
        send_pickle(p2_conn, [rounds, p2.star, p2.cards])

        # select a card
        p1_choice = pickle.loads(p1_conn.recv(1024))
        p2_choice = pickle.loads(p2_conn.recv(1024))
        p1.cards[p1_choice] -= 1
        p2.cards[p2_choice] -= 1

        # judge win or lose
        p1, p1_judge, p2, p2_judge = game.judge_janken(
            p1, p1_choice, p2, p2_choice)
        send_pickle(p1_conn, [p1_judge, p1_choice, p2_choice])
        send_pickle(p2_conn, [p2_judge, p2_choice, p1_choice])

        # game over or not
        ison = game.is_on(p1, p2)
        send_pickle(p1_conn, ison)
        send_pickle(p2_conn, ison)
        if not ison:
            break

        rounds += 1

    winner = game.winner(p1, p2)
    if not winner:
        game_result = 'DRAW'
    else:
        game_result = f'WINNER: {winner.name}'

    p1_conn.recv(1024)
    send_pickle(p1_conn, [game_result, p1.results])
    p2_conn.recv(1024)
    send_pickle(p2_conn, [game_result, p2.results])

    p1_conn.close()
    print(f'closed: {p2_addr}')
    p2_conn.close()
    print(f'closed: {p2_addr}')


def main():
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostbyname('localhost')
    port = 9999

    serversocket.bind((host, port))

    serversocket.listen(6)
    accept = serversocket.accept
    while True:
        accept1 = accept()
        print(f'connected: {accept1[1]}')
        accept2 = accept()
        print(f'connected: {accept2[1]}')

        threading.Thread(target=gamethread, args=(
            accept1, accept2)).start()


if __name__ == '__main__':
    main()
