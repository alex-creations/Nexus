import flask
import socket

# --------------------------
# --------------------------
# -x----------------------x-
# --------------------------
# --------------------------

class Game:
    def __init__(self):
        self.defaultGrid = list("--------------------------")
        self.playerOne = 2 # initial position
        self.playerTwo = 25 # initial position

    def update_grid(self, playerOne: int, playerTwo: int):
        playerOne = self.playerOne
        playerTwo = self.playerTwo
        self.defaultGrid = list("--------------------------")
        for i in range(len(self.defaultGrid)):
            if i+1 == playerOne:
                self.defaultGrid[i] = "x"
            if i+1 == playerTwo:
                self.defaultGrid[i] = "y"
        return self.defaultGrid

    def handle_move(self, direction: str, player: int):
        """
        Handles player movement across the game grid.\n
        Requires `player` (int) and `direction` (str)\n
        Returns: `400` (moved), `401` (something in the way), `402` (out of bounds)
        """
        playerOne = self.playerOne
        playerTwo = self.playerTwo
        match direction: # undertale vibes
            case "left":
                match player:
                    case 1:
                        self.playerOne += 1
                        return self.update_grid(playerOne+1,playerTwo)

a = Game()
print(a.handle_move("left", 1))
print(a.handle_move("left", 1))

def server_program():
    host = socket.gethostname() # user's host name
    port = 2700  # game:client port (nexus will run on 2700)

    server_socket = socket.socket() # fetch socket
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2) # 2 max connections at once
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True: # receive data stream
        game = Game()
        data = conn.recv(1024).decode() # no data packet > 1024 bytes
        if not data:
            # if other end terminates, terminate
            break
        print("from connected user: " + str(data))
        if str(data) == "1 right":
            game.handle_move("right", 1)
        if str(data) == "1 left":
            game.handle_move("left", 1)
        x = game.update_grid()
        returnGrid = ""
        for grid in x:
            returnGrid += f"\n{grid}"
        conn.send(returnGrid.encode())
        # data = input('respond -> ')
        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

#if __name__ == '__main__': # if not imported, start server
#    server_program()