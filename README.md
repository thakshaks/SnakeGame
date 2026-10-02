This is a repository for my multi-game platform.

My multi-game platform uses a Django web-server that listens to user requests and redirects users to the game. Each user input is then sent to the respective game-engines, where the position of game elements such as snake, apple (in snake_game), block positions (in tetris) is updated and status is sent to the web browser for rendering.

My architecture uses Redis for caching the inputs from browser and game element positions, scores, game-over status, etc. from game engines. This reduces the latency between user outputs and game rendering on browser.

Here is a brief description of each folder in my rep:
 a) Config-> i) Settings.py: Contains required configurations to run my application.
 ii) asgi.py: The main entry point into the server.

 b) k8s: Contains Kubernetes manifest files

 c) main: i) templates: Contains templates for dashboard, snake_game, tetris, login and register pages.
 ii) consumers.py: It is responsible for establishing a web socket connection with the browser, receive user inputs from browser and forward those inputs to engine through redis, subscribe to status from redis and forward status to web-browser.
 iii) model.py: Defines database schema to store score of users/game.
 iv) routing.py: Calls methods from consumer.py upon browser requesting a web socket coonection.
 v) urls.py: Calls various methods in views.py to render dashboard, login, register and game templates.
 vi) views.py: Has methods that link url requests from browser and templates for specific urls.

 d) snake-engine: i) Dockerfile: Helps build image for the snake_game.
 ii) main.py: Subscribes to redis to get inputs from users and forwards these to the snakegame.py methods.
 iii) snakegame.py: Brain of the game. Responsible for logic and positioning of game elements 

 e) tetris-engine:  i) Dockerfile: Helps build image for the tetris.
 ii) main.py: Subscribes to redis to get inputs from users and forwards these to the tetris.py methods.
 iii) tetris.py: Brain of the game. Responsible for logic and positioning of game elements 

f) db.sqlite3: SQL database containing player and score info.

g) Dockerfile.web: Helps build image for django web-server
