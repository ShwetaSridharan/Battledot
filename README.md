# Battledot
Battledot is a spinoff of the popular battleship game. The game has been implemented in python and was done for a take home assessment.
Game description:

Rather than having two players oppose each other directly, any player will be attacked by one opponent and in turn will attack a different opponent.   
Players are connected in a ring: A is bombing B who is bombing C, ... who is bombing Z who is bombing A.   
Each player has a 10x10 grid of "dots" where one "single-dot ship" is positioned randomly. A player loses if this ship is bombed.   
Players cannot see each other's grids directly. Each player randomly selects a dot location on the enemy grid to bomb, and sends the bomb to the enemy. If the bomb lands in the enemy's dot-ship, the enemy dies; otherwise, it lives. When a player dies, relevant neighbors are matched up so that their unfinished games can continue.   
For example: A is bombing B is bombing C is bombing D is bombing A. If B hits C's ship, B wins, C loses/dies. B is now bombing D. 

Follow the steps below to run the code:
README FILE:

This program is a BattleDot SpinOff where Players will enter into the arena and await the game to start.
Players will then take turns attacking at random the oppenent in front of them. When their ship is taken down by an opponent,
they will send the port/IP of the oppenents adjacent to it so they can be connected. The game ends when only one user remains

The program features 2 ways to play. P2P with different IP's under the same network or different Ports using the same machine!

Written in Python 3.7.3


HOW TO USE:

IF ON THE SAME MACHINE:

We initialize all the players by: (Assuming they will form a perfect ring and no user has multiple people attacking it)

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser

eg. (Python BattleDot.py N/A N/A 8079 8081 2 8080)

    (Python BattleDot.py N/A N/A 8080 8079 2 8081)

Initialize the final player with the last arguement being "first"

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser first

eg. (Python BattleDot.py N/A N/A 8081 8080 2 8079 first)


Wait until the users done battling !!



IF ON SEPERATE MACHINES:

We initialize all the players by: (Assuming they will form a perfect ring and no user has multiple people attacking it)

Here the ports do not really matter.

Run Python BattleDot IP_A IP_B PortA PortB #OfOtherplayers PortUser

eg. (Python BattleDot.py 129.128.41.11 129.128.41.13 8080 8089 2 8080)

    (Python BattleDot.py 129.128.41.12 129.128.41.11 8080 8089 2 8080)

Initialize the final player with the last arguement being "first"

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser first

eg. (Python BattleDot.py 129.128.41.13 129.128.41.12 8080 8089 2 8080)



Wait until the users are done battling !



RESULTS:

Throughout the entire program for each process there will be "Sent attack to ___" and Received from "____"

these help indicate which node its being attacked by or who it is attacking. Upon getting knocked out, it will say

"Hit! Player Lose" and will then update the neighbors with its each other's IP/POrt so they can continue battling.

Upon being the last player remaining, There is a notification saying the user has won!
