import random, sys, pygame
from pygame.locals import *
FPS, SCREENWIDTH, SCREENHEIGHT, GAME_SPRITES = 32, 289, 511, {}
SCREEN, GROUNDY = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)), SCREENHEIGHT * 0.8
PLAYER, BACKGROUND, PIPE = 'assets/bird.png', 'assets/grey.jpg', 'assets/pipe.png'
def welcomeScreen():
    basex, playerx, playery = 0, int(SCREENWIDTH / 5), int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score, playerx, playery, basex = 0, int(SCREENWIDTH / 5), int(SCREENWIDTH / 2), 0
    newPipe1, newPipe2 = getRandomPipe(), getRandomPipe()
    upperPipes = [ {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']}, {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}, ]
    lowerPipes = [ {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']}, {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}, ]
    pipeVelX, playerVelY, playerMaxVelY, playerMinVelY, playerAccY, playerFlapAccv, playerFlapped= -4, -9, 10, -8, 1, -8, False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: playerVelY, playerFlapped = playerFlapAccv, True
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4: score += 1
        if playerVelY < playerMaxVelY and not playerFlapped: playerVelY += playerAccY
        if playerFlapped: playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0]), lowerPipes.append(newpipe[1])
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits, width = [int(x) for x in list(str(score))], 0
        for digit in myDigits: width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2
        for digit in myDigits:
            SCREEN.blit(pygame.font.SysFont('comicsansms', 20).render("Press Space to Start", True, (0, 0, 0)), [55, 5])
            SCREEN.blit(pygame.font.SysFont('comicsansms', 20).render("Score", True, (0, 0, 0)), [115, 30])
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0: return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            return True
    return False
def getRandomPipe():
    pipeHeight, offset = GAME_SPRITES['pipe'][0].get_height(), SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX, y1 = SCREENWIDTH + 10, pipeHeight - y2 + offset
    pipe = [ {'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]
    return pipe
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flap Bird')
    GAME_SPRITES['numbers'] = (pygame.image.load('assets/0.png').convert_alpha(),
                               pygame.image.load('assets/1.png').convert_alpha(), pygame.image.load(
        'assets/2.png').convert_alpha(),
                               pygame.image.load('assets/3.png').convert_alpha(), pygame.image.load(
        'assets/4.png').convert_alpha(),
                               pygame.image.load('assets/5.png').convert_alpha(), pygame.image.load(
        'assets/6.png').convert_alpha(),
                               pygame.image.load('assets/7.png').convert_alpha(), pygame.image.load(
        'assets/8.png').convert_alpha(),
                               pygame.image.load('assets/9.png').convert_alpha(),)
    GAME_SPRITES['base'] = pygame.image.load('assets/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), pygame.image.load(PIPE).convert_alpha() )
    GAME_SPRITES['background'], GAME_SPRITES['player'] = pygame.image.load(BACKGROUND).convert(), pygame.image.load(PLAYER).convert_alpha()
    while True: mainGame()