import pygame, time, random, sys

# pygame initialization 
pygame.init()

# game configuration
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480
SNAKE_SIZE = 15
SNAKE_SPEED = 15
SCORE_FONT = pygame.font.SysFont("ubuntu", 20)
GAME_OVER_FONT = pygame.font.SysFont("ubuntu", 90)
POINT_SOUND = pygame.mixer.Sound("res/point.mp3")
GAME_OVER_SOUND = pygame.mixer.Sound("res/game_over.mp3")

# game colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# game window and clock initialization
gameWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("pySnake")
clock = pygame.time.Clock()

# draw score to top left game window (during game)
def drawScore(score):
  textSurface = SCORE_FONT.render("Score : " + str(score), True, WHITE)
  rect = textSurface.get_rect()
  rect.midtop = (WINDOW_WIDTH/10, 15)
  gameWindow.blit(textSurface, rect)

# draw game over screen (after game)
def drawGameOver(finalScore, highScore):
  pygame.mixer.Sound.play(GAME_OVER_SOUND)

  # game over text
  gameOverSurface = GAME_OVER_FONT.render("GAME OVER", True, RED)
  gameOverRect = gameOverSurface.get_rect()
  gameOverRect.midtop = (WINDOW_WIDTH / 2, WINDOW_WIDTH / 6)
  
  # score text
  scoreSurface = SCORE_FONT.render("Score : " + str(finalScore), True, RED)
  scoreRect = scoreSurface.get_rect()
  scoreRect.midtop = (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75)

  # high score text
  highScoreSurface = SCORE_FONT.render("High Score : " + str(highScore), True, RED)
  highScoreRect = highScoreSurface.get_rect()
  highScoreRect.midtop = (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 1.75)

  # play again text
  playAgainSurface = SCORE_FONT.render("Play again? [Y/n]", True, RED)
  playAgainRect = playAgainSurface.get_rect()
  playAgainRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.25)

  # drawing and updating game window
  gameWindow.fill(BLACK)
  gameWindow.blit(gameOverSurface, gameOverRect)
  gameWindow.blit(scoreSurface, scoreRect)
  gameWindow.blit(highScoreSurface, highScoreRect)
  gameWindow.blit(playAgainSurface, playAgainRect)
  pygame.display.flip()

def runGame():
  # game variables
  snake = [[WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2], [(WINDOW_WIDTH // 4) - SNAKE_SIZE, WINDOW_HEIGHT // 2], [(WINDOW_WIDTH // 4) - (SNAKE_SIZE * 2), WINDOW_HEIGHT // 2]]
  foodPosition = [(WINDOW_WIDTH / 4) * 3, WINDOW_HEIGHT / 2]

  snakeDirection = [SNAKE_SIZE, 0]
  newSnakeDirection = [SNAKE_SIZE, 0]

  running = True

  # main game logic
  while running:
    for event in pygame.event.get():
      # pygame window closed
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
      # key is pressed
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          newSnakeDirection[0] = 0
          newSnakeDirection[1] = -SNAKE_SIZE
        if event.key == pygame.K_DOWN:
          newSnakeDirection[0] = 0
          newSnakeDirection[1] = SNAKE_SIZE
        if event.key == pygame.K_LEFT:
          newSnakeDirection[0] = -SNAKE_SIZE
          newSnakeDirection[1] = 0
        if event.key == pygame.K_RIGHT:
          newSnakeDirection[0] = SNAKE_SIZE
          newSnakeDirection[1] = 0
    
    # game over conditions
    # out of bounds
    if snake[0][0] >= WINDOW_WIDTH or snake[0][0] < 0 or snake[0][1] >= WINDOW_HEIGHT or snake[0][1] < 0:
      running = False

    # snake self collision
    for pixel in snake[1:]:
      if snake[0][0] == pixel[0] and snake[0][1] == pixel[1]:
        running = False

    # snake direction verfication
    if snakeDirection != newSnakeDirection:
      # up and down
      if newSnakeDirection[1] > 0 and snakeDirection[1] >= 0 or newSnakeDirection[1] < 0 and snakeDirection[1] <= 0:
        snakeDirection[0] = 0
        snakeDirection[1] = newSnakeDirection[1]
      # left and right
      if newSnakeDirection[0] > 0 and snakeDirection[0] >= 0 or newSnakeDirection[0] < 0 and snakeDirection[0] <= 0:
        snakeDirection[0] = newSnakeDirection[0]
        snakeDirection[1] = 0

    # incrementing snake head co-ordinates and inserting in snake list
    snakeHead = [snake[0][0], snake[0][1]]
    snakeHead[0] += snakeDirection[0]
    snakeHead[1] += snakeDirection[1]
    snake.insert(0, snakeHead)

    # checking if snake has consumed food and removing tail to adjust for new head
    if snakeHead[0] == foodPosition[0] and snakeHead[1] == foodPosition[1]:
      pygame.mixer.Sound.play(POINT_SOUND)
      foodPosition = [random.randrange(0, (WINDOW_WIDTH // SNAKE_SIZE)) * SNAKE_SIZE, random.randrange(0, (WINDOW_HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
    else:
      snake.pop()

    # drawing snake and food
    gameWindow.fill(BLACK)
    pygame.draw.rect(gameWindow, WHITE, [foodPosition[0], foodPosition[1], SNAKE_SIZE, SNAKE_SIZE])
    
    for s in snake:
      pygame.draw.rect(gameWindow, GREEN, [s[0], s[1], SNAKE_SIZE, SNAKE_SIZE])

    # displaying score and updating pygame display
    drawScore(len(snake) - 3)
    pygame.display.update()
    clock.tick(SNAKE_SPEED)
  
  return len(snake) - 3

lastScore = runGame()
highScore = lastScore
drawGameOver(lastScore, highScore)

# game over screen event handling
gameEnd = False
while not gameEnd:
  for event in pygame.event.get():
    # pygame window closed
    if event.type == pygame.QUIT:
      gameEnd = True
    # key is pressed
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_y or event.key == pygame.K_RETURN:
        lastScore = runGame()
        if lastScore > highScore:
          highScore = lastScore
        drawGameOver(lastScore, highScore)
      if event.key == pygame.K_n or event.key == pygame.K_q:
        gameEnd = True
  clock.tick(SNAKE_SPEED)
  
pygame.quit()
sys.exit(0)