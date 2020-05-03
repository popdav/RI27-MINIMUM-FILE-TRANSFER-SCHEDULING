from MockNetwork import Network


def main():
    n = Network()
    n.init_network()

    for server in n:
        print(server)


if __name__ == '__main__':
    main()
