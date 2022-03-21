

#Imports
import random, socket, sys , pickle, time


#Player class

class Player():
    def __init__(self):

        #Define the 10x10 grid of dots.
        self.grid = [['O' for x in range(10)]for y in range(10)]

        #Initialize the X and y coordinates of the grid to be selected at random.
        self.x = random.randint(0,9)
        self.y = random.randint(0,9)
        self.grid[self.x][self.y] = "X"

        #Define the ports for IPC
        self.port = None
        self.rightport = None
        self.leftport = None

        #Define the elements of the game- players, hits.
        self.players = None 
        self.leftsideplayer = None
        self.rightsideplayer = None
        self.bombattempts = []
        self.hits = 0


        #Get the local IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Allow both TCP and UDP connections.
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

        #Socket Connection Establishment

def listen(player):

    #Assign host variable to the local ip address.
    host = get_ip_address()

    while True:
        if player.rightsideplayer:

            print("Awaiting...")

            #Create a socket to listen.
            listensocket = socket.socket()

            #Set the socket reusablity option- in order to reduce 'socket address in use' errors.
            listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #Bind the listening socket to the IP address and Port.
            listensocket.bind((host, 8080))

            #Listen for messages with the backlog argument of 5, which is the max number of queued connections.
            listensocket.listen(5)

            #Accept the incoming connections. The return values are, c-a new socket object to send and receive data on the connection
            #and addr-the address bound to the socket on the other end of the connection.
            c, addr = listensocket.accept()

            #Receiving the message
            msg = c.recv(1024)

            #Converting the object into byte stream.
            msg_array = pickle.loads(msg)

            time.sleep(0.2)
            print("Received " + str(msg_array))

        else:

            print("Awaiting...")
            listensocket = socket.socket()
            listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     
            listensocket.bind((host,int(player.port)))      
            listensocket.listen(5)     
            c ,addr = listensocket.accept()     
            msg = c.recv(1024)     
            msg_array = pickle.loads(msg)
            time.sleep(0.2)
            print("Received " + str(msg_array))


        #Working of the game going clockwise.
        if "bomb" in msg_array:

            if player.rightsideplayer:

                #Gather the hits and parse the message according to rules for the next player.
                player.hits = player.hits + int(msg_array.partition("/")[2])
                player.rightsideplayer = msg_array.partition("bomb")[0]

                #Reset the bombattempts for the next player in turn.
                player.bombattempts = []

                #Check if there are any players left or all bombed.
                if int(player.hits) == int(player.players):
                    print("YOU WON! :)")
                    break

                else:
                    #Attack the nect player in turn and continue the game.
                    #Create a new socket for the round.
                    sockettwo = socket.socket()

                    #Connect it to the player on the right to start listening.
                    sockettwo.connect((player.rightsideplayer, 8080))

                    #attack with random coordinate values.
                    bombx = random.randint(0, 9)
                    bomby = random.randint(0, 9)

                    #Convert them into a byte stream.
                    data_string = pickle.dumps((bombx, bomby))
                    sockettwo.send(data_string)

                    #Save the attempted attack coordinates.
                    player.bombattempts.append((bombx, bomby))

                    #Close all the sockets
                    print("Bombed IP " + player.rightsideplayer + "(" + str(bombx) + "," + str(bomby) + ")")
                    sockettwo.close()
                    listensocket.close()

            else:
                player.hits = player.hits + int(msg_array.partition("/")[2])
                player.rightport = msg_array.partition("bomb")[0]
                player.bombattempts = []
                if int(player.hits) == int(player.players):
                    print("Winner!")
                    break
                else:
                    sockettwo = socket.socket()
                    time.sleep(2)
                    sockettwo.connect((host,int(player.righstport)))
                    bombx = random.randint(0, 9)
                    bomby = random.randint(0, 9)
                    data_string = pickle.dumps((bombx, bomby))
                    sockettwo.send(data_string)
                    player.bombattempts.append((bombx, bomby))
                    print("Bombed port" + player.rightport + "(" + str(bombx) + "," + str(bomby) + ")")
                    sockettwo.close()
                    listensocket.close()
                    print("updated")

        #We reassign the next player's left side player.
        elif "def" in msg_array:

            if player.leftsideplayer:
                if int(player.hits) == int(player.players):
                    print("Winner!")
                    break

                player.leftsideplayer = "".join(msg_array.split("def"))
                print("updated")
                listensocket.close()
            else:
                if int(player.hits) == int(player.players):
                    print("Winner!")
                    break
                player.leftport = "".join(msg_array.split("def"))
                print("updated")
                listensocket.close()

        else:

            #Check if the received coordinates for attack bombed our ship.
            if player.grid[msg_array[0]][msg_array[1]] == "X":
                print("BOMBED! PLAYER LOSES :(")

                if player.rightsideplayer:
                    socketright = socket.socket()
                    socketright.connect((player.rightsideplayer, 8080))
                    #Send the IP address of the left side player to the right side player for connection.
                    data_string = pickle.dumps(player.leftsideplayer + "def")
                    socketright.send(data_string)
                    socketright.close()
                    time.sleep(1) 

                    socketleft = socket.socket()
                    socketleft.connect((player.leftsideplayer, 8080))
                    data_string = pickle.dumps(player.rightsideplayer + "bomb" + "/" + str(player.hits + 1))
                    socketleft.send(data_string)
                    socketleft.close()
                    listensocket.close()
                    break
                else:
                    socketleft = socket.socket()
                    socketleft.connect((host, int(player.leftport)))
                    data_string = pickle.dumps(player.rightport + "bomb" + "/" + str(player.hits + 1))
                    socketleft.send(data_string)
                    socketleft.close()

                    socketright = socket.socket()
                    socketright.connect((host, int(player.rightport)))
                    data_string = pickle.dumps(player.leftport + "def")
                    socketright.send(data_string)
                    socketright.close()
                    listensocket.close()
                    break

            else:
                #if there is no hit, the game will continue and "loc" is the location that takes hit next.
                player.grid[msg_array[0]][msg_array[1]] = "loc"

                if player.rightsideplayer:
                    sockettwo = socket.socket()
                    sockettwo.connect((player.rightsideplayer, 8080))
                    while True:
                        #attack using random coordinates.
                        bombx = random.randint(0, 9)
                        bomby = random.randint(0, 9)

                        #Cross check with the list of bomb attempts to see if the coordinates have already been used and move forward only if unused.
                        if (bombx,bomby) not in player.bombattempts:
                            data_string = pickle.dumps((bombx, bomby))
                            sockettwo.send(data_string)

                            #Save the new attack coordinates pair to the list
                            player.bombattempts.append((bombx,bomby))
                            print("Sent Attack to IP" + player.rightsideplayer + "(" + str(bombx) + "," + str(bomby) + ")")
                            sockettwo.close()
                            listensocket.close()
                            break
                else:
                    sockettwo = socket.socket()
                    sockettwo.connect((host,int(player.rightport)))

                    while True:
                        bombx = random.randint(0, 9)
                        bomby = random.randint(0, 9)
                        if (bombx, bomby) not in player.bombattempts:
                            data_string = pickle.dumps((bombx, bomby))
                            sockettwo.send(data_string)
                            player.bombattempts.append((bombx, bomby))
                            print("Sent Attack to port " + player.rightport + "(" + str(bombx) + "," + str(bomby) + ")")
                            sockettwo.close()
                            listensocket.close()
                            break

#code for defining the command line arguments in each case.

def samemachine(player):
    player.leftport = sys.argv[3]
    player.rightport = sys.argv[4]
    player.players = sys.argv[5]
    player.port = sys.argv[6]
    listen(player)

def differentmachine(player):
    player.leftsideplayer = sys.argv[1]
    player.rightsideplayer = sys.argv[2]
    player.players = sys.argv[5]
    player.port = sys.argv[6]
    listen(player)


def game():
    #Check if they are less than 3 arguements
    if len(sys.argv) < 3:
        print("Specify a Left and Right Node/Address")

    #The player who will intiate the bomb attempts
    elif len(sys.argv) == 8: #first bomb attempt
        try:
            if sys.argv[7] == "first":
                #checking if the value of number of players is valid
                if int(sys.argv[5]):
                    if sys.argv[1] == sys.argv[2] == "N/A":
                        #Initialize new player
                        newplayer = Player()
                        #Bind the values of player nodes that was used in the 'player' class.
                        newplayer.leftport = sys.argv[3]
                        newplayer.rightport = sys.argv[4]
                        newplayer.players = sys.argv[5]
                        newplayer.port = sys.argv[6]

                        #Repeat the same process of creating a new socket and connecting it to the next player in question.
                        sockettwo = socket.socket()
                        host = get_ip_address()
                        sockettwo.connect((host, int(newplayer.rightport)))

                    
                        bombx = random.randint(0,9)
                        bomby = random.randint(0,9)
                        data_string = pickle.dumps((bombx,bomby))
                        sockettwo.send(data_string)
                        print("Bombed the port" + newplayer.rightport + "(" + str(bombx) + "," + str(bomby) + ")")
                        sockettwo.close()
                        listen(newplayer)

                    else:
    
                        newplayer = Player()
                        newplayer.leftsideplayer = sys.argv[1]
                        newplayer.rightsideplayer = sys.argv[2]
                        newplayer.players = sys.argv[5]
                        newplayer.port = sys.argv[6]
                        sockettwo = socket.socket()
                        host = get_ip_address()
                        sockettwo.connect((newplayer.rightsideplayer, 8080))
                        bombx = random.randint(0, 9)
                        bomby = random.randint(0, 9)
                        data_string = pickle.dumps((bombx, bomby))
                        sockettwo.send(data_string)
                        print("Sent Attack to IP " + newplayer.rightsideplayer + "(" + str(bombx) + "," + str(bomby) + ")")
                        sockettwo.close()
                        listen(newplayer)

        except TypeError:
            print("Enter number of players in the game")

    elif len(sys.argv) == 7:

        try:
            #Validity check
            if int(sys.argv[5]):
                if sys.argv[1] == sys.argv[2] == "N/A":
                    player = Player()
                    samemachine(player)
                else:
                    player = Player()
                    differentmachine(player)


        except TypeError:
            print("Enter number of players in the game")
    return

if __name__ == '__main__':

    game()