import socket
import select

port = 60003
sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockL.bind(("", port))
sockL.listen(1)

listOfSockets = []

print(f"Listening on port {port}")


def broadcast(message, sender):
    try:
        message = f"[{sender.getpeername()}]: {message}"
    except:
        message = f"server: {message}"

    for soc in listOfSockets:
        soc.send(message.encode())


while True:
    tup = select.select(listOfSockets, [], [])
    sock = tup[0][0]

    if sock == sockL:
        sockClient, addr = sockL.accept()
        broadcast(f"{addr} connected")
        listOfSockets.append(sockClient)
    else:
        data = sock.recv(2048)
        if not data:
            listOfSockets.remove(sock)
            broadcast("Disconnected", sock)
            sock.close()
        else:
            broadcast(data.decode(), sock)
