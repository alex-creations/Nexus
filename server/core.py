import flask
import socket

# --------------------------
# --------------------------
# -x----------------------x-
# --------------------------
# --------------------------

class Game:
    def __init__(self):
        self.defaultGrid = ["--------------------------",
                    "--------------------------",
                    "--------------------------",
                    "--------------------------",
                    "--------------------------"]
        self.playerOne = [2,2] # initial position
        self.playerTwo = [25,2] # initial position

    def update_grid(self, playerOne: list = [2,2], playerTwo: list = [25,2]):
        playerOne = self.playerOne
        playerTwo = self.playerTwo
        updateGrid = self.defaultGrid[playerOne[1]]
        updatedGrid = ""
        x = 0
        for pos in updateGrid:
            if x == playerOne[0] or x == playerTwo[0]:
                updatedGrid += "x"
            else:
                updatedGrid += "-"
            x += 1
        self.defaultGrid[playerOne[1]] = updatedGrid
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
            case "up":
                if player == 1:
                    if playerTwo == [playerOne[0], (playerOne[1]+1)]:
                        return 401 # something is already there
                    if playerOne[1]+1 > 4:
                        return 402 # out of bounds
                    playerOne = [playerOne[0], (playerOne[1]+1)]
                if player == 2:
                    if playerOne == [playerTwo[0], (playerTwo[1]+1)]:
                        return 401 # something is already there
                    if playerTwo[1]+1 > 4:
                        return 402 # out of bounds
                    playerTwo = [playerOne[0], (playerOne[1]+1)]
            case "down":
                if player == 1:
                    if playerTwo == [playerOne[0], (playerOne[1]-1)]:
                        return 401
                    if playerOne[1]-1 < 0:
                        return 402
                    playerOne = [playerOne[0], (playerOne[1]-1)]
                if player == 2:
                    if playerOne == [playerTwo[0], (playerTwo[1]-1)]:
                        return 401
                    if playerTwo[1]-1 < 0:
                        return 402
                    playerTwo = [playerTwo[0], (playerTwo[1]-1)]
            case "left":
                if player == 1:
                    if playerTwo == [(playerOne[0]-1), playerOne[1]]:
                        return 401
                    if playerOne[0]-1 < 0:
                        return 402
                    playerOne = [(playerOne[0]-1), playerOne[1]]
                if player == 2:
                    if playerOne == [(playerTwo[0]-1), playerTwo[1]]:
                        return 401
                    if playerTwo[0]-1 < 0:
                        return 402
                    playerTwo = [(playerTwo[0]-1), playerTwo[1]]
            case "right":
                if player == 1:
                    if playerTwo == [(playerOne[0]+1), playerOne[1]]:
                        return 401
                    if playerOne[0]-1 > 25:
                        return 402
                    playerOne = [(playerOne[0]+1), playerOne[1]]
                if player == 2:
                    if playerOne == [(playerTwo[0]+1), playerTwo[1]]:
                        return 401
                    if playerTwo[0]-1 > 25:
                        return 402
                    playerTwo = [(playerTwo[0]+1), playerTwo[1]]

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

if __name__ == '__main__': # if not imported, start server
    server_program()