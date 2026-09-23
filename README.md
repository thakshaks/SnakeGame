This is my multigame_project repo.

Multigame Platform allows users to login to the gaming platform and play classic games such as snake game, tetris, etc. Each game runs in a separate container. Redis caches user inputs and game status containing details about coordinates of various game pieces, score, game-over call, etc. Various aspects of the game was created through the use of AI platforms such as Gemini, Claude and Anthropic. Was bugs with respect to configurations and settings was resolved to make the game smoother.

config: Contains settings required to run the program.

main: 
   |-templates: Contains html templates for games, dashboard and login pages. 
   |-consumers.py: This is for asynchronous communication between browser and games/main engines. Also initializes Redis to publish game                       inputs from browser and game state from each game container.
   |-routing.py: Listens to socket connections from browser and calls GameConsumer class in consumers.py
   |- views.py: Contains various functions related to login, logouts, and dashboard calls from urls.py
   |-urls.py: Routes requests to views.py

snake-engine:
  |-main.py: Listens to game inputs on Redis channels and publishes game state to Redis (Will be used by consumers.py). Calls various                   game functions in snakegame.py. 
  |-snakegame.py: Contains main game logic such as suspension on game upon hitting the edges, increase in score on consuming apple,                           increase in length of snake to name a few.
  |-Dockerfile.game: Dockerfile to create snake_game image.

tetris-engine:
  |-main.py: Listens to game inputs on Redis channels and publishes game state to Redis (Will be used by consumers.py). Calls various                   game functions in tetris.py. 
  |-tetris.py: Contains main game logic such as generating different blocks, placing blocks on top of each other, clearing full rows and                suspension of game upon block tower hitting the top.
  |-Dockerfile.game: Dockerfile to create tetris image.

Dockerfile.web: Creates a web-server image.

docker-compose.yaml: Docker compose file for orchestrating web server and game conatiners.

In work: 
      |-Adding a PostgreSQL to store scores of all players.
      |- Addition of other games.
      |- Using Kubernetes to orchestrate all services. 
      |- Host on AWS or GCP Platform

  
  
