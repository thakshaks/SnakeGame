This is a repository for my multi-game platform.

My multi-game platform uses a Django web-server that listens to user requests and redirects users to the game. Each user input is then sent to the respective game-engines, where the position of game elements such as snake, apple (in snake_game), block positions (in tetris) is updated and status is sent to the web browser for rendering.

My architecture uses Redis for caching the inputs from browser and game element positions, scores, game-over status, etc. from game engines. This reduces the latency between user outputs and game rendering on browser.

Here is a brief description of each folder in my rep:
 Config-> i) Settings.py: Contains

