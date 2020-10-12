import socket
import pickle


def main():
    client = socket.socket()
    addr = ('localhost', 9090)
    client.connect(addr)

    while True:
        print('1 - GetSimilarMovies')
        print('2 - Quit')

        choice = int(input('Enter your choice: '))
        request = {}
        if choice == 2:
            break

        if choice == 1:
            request['function_name'] = 'GetSimilarMovies'
            request['args'] = [855,706,862,821,218],

        request = pickle.dumps(request)
        client.send(request)
        response = client.recv(1024)
        response = pickle.loads(response)
        print('Response from server:', response)


if __name__ == '__main__':
    main()