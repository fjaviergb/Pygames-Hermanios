# Pygame-Hermanios
In this project we present an arena type videogame only in python, moreover pygames.

## Running the videogame [Via python].
  - Clone the repository
  - In server.py add the desired ip for the server
  - In network.py add the server ip
  - In a terminal run:
  ```python
    python server.py
  ```
  - In a new terminal where the server is run client_enviroment.py
  ```python
    python client_enviroment.py
  ```
  - In a new terminal run client.py to initialize the client:
  ```python
    python client.py
  ```
 ## Running the videogame [Via executable].
  - First you need to have a server and client enviroment running as described above
  - To open the client either install the .exe (only for windows) or run the exe inside the exe folder
  
 ## Controls.
  - W: to go up
  - S: to go down
  - A: to go to the left
  - D: to go to the right
  - Shift: to block
  - Space: to sprint (only once every 5 seconds)
  - Ctl: to run (it is independent from sprinting)
  
## Caveats when ran in local.
If the game wanted to be ran in local we suggest to set the following variables:
  - chargecount in utils.py to 1
  - DISMAX_TIC in variables.py to 8
  - VELOCITY in variables.py to 2
That is because the variables are set to run optimal in the cloud which is slower than in local.

## Original idea and thoughts about pygames.
The original idea of this project was to build a survival game in the browser, but given the limitations of running python on the browser
and moreover pygames we were force to switch to executables.
About pygames, although it might be a good and funny tool to get started with programming videogames, we think that it lacks the depth
to produce advanced videogames. Some of those cons are: Slow and difficulty of collisions; its peak performance happens when it is ran by ticks and
it is difficult to make time dependant based functions, which makes it difficult to mock things as gravity, slashes, sprints etc.
Even though it is implementing antialiasing through a new api, called gfxdraw, it lacks drawing options existent in the original drawing tools.

## More difficulties with python/sockets:
Even though the game runs smoothly in a local network, when it is launched to the cloud the speed of the message transmission is too slow and
the game slow down to the point of making it unplayable. To overcome that we have increased the speed of the movement and sword swing and slash.

## TODO:
If someone wanted to continue the project or for our future selfs, the following can be done:
  - Improve the connection to the server
  - Try to run it on a web browser
  - Optimize slashes or in general collitions with objects.

