import pygame, sys, time


velocityXright = 0
velocityXleft = 0
velocityY = 0
x1 = 0
x2 = 0
pause = False
BG = pygame.image.load("assets/MenuBG.png")
p1score, p2score = 0, 0

class Player:
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.speed = 0
        
        self.img = pygame.image.load("assets/p1.gif").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 0.6)

    def update(self):
        self.posY -= self.speed
        if self.posY > 645:
            self.posY = 645
        self.speed -= 1.5

    def render(self, screen):
        w, h = self.img.get_rect().size
        screen.blit(self.img, (self.posX-w/2,self.posY-h/2))

class Player2(Player):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.img = pygame.image.load("assets/p2.gif").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 0.6)


class Ball:
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.velocity = 0.1
        self.acceleration = 0.3

        self.img = pygame.image.load("assets/SoccerBall.png").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 0.4)

    def update(self):
        self.velocity += self.acceleration
        self.posY += self.velocity
        if self.posY >= 660:
            self.velocity = -self.velocity

    def render(self, screen):
        w, h = self.img.get_rect().size
        screen.blit(self.img, (self.posX-w/2,self.posY-h/2))


class Button:
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


class Menu:
    pygame.init()
    pygame.display.set_caption("Head Ball")
    screen = pygame.display.set_mode((1280, 720))

    def get_font(self, size):
        return pygame.font.Font("assets/font.ttf", size)
        
    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(BG, (0, 0))

            OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 550), 
                                text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main()
            pygame.display.update()

    def PlayButton(self):
        global pause
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(BG, (0, 0))

            BACK = Button(image=None, pos=(640, 560), 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            MULT = Button(image=None, pos=(640, 360), 
                                text_input="Play Online", font=self.get_font(50), base_color="Black", hovering_color="Green")
            AI = Button(image=None, pos=(640, 160), 
                                text_input="Play with an AI", font=self.get_font(50), base_color="Black", hovering_color="Green")
            FRIEND = Button(image=None, pos=(640, 260), 
                                text_input="Play with a friend", font=self.get_font(50), base_color="Black", hovering_color="Green")

            for button in [BACK, MULT, AI, FRIEND]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK.checkForInput(MOUSE_POS):
                        self.main()
                    if AI.checkForInput(MOUSE_POS):
                        Ai.run(Ai())
                        pause = False
                    if FRIEND.checkForInput(MOUSE_POS):
                        Friend.run(Friend())
                        pause = False
                    if MULT.checkForInput(MOUSE_POS):
                        Game.run(Game())
                        pause = False
            pygame.display.update()

    def main(self):
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("Head Ball", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.PlayButton()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()


class Game:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.player = None
        self.ball = None
        self.menu = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()

    def init(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Head Ball")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(150, 645)
        self.ball = Ball(640, 400)
        self.menu = Menu()

    def update(self):
        self.events()
        self.player.update()
        self.ball.update()
        self.collisions()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if not pause:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                if self.player.posY >= 640:
                    self.player.speed = 18
            if keys[pygame.K_a]:
                self.player.posX -= 5
            if keys[pygame.K_d]:
                self.player.posX += 5

    def render(self):
        self.screen.fill((50,150,0))
        self.player.render(self.screen)
        self.ball.render(self.screen)
        self.display_score()
        self.drawStadium()
        self.clock.tick(60)

    def drawStadium(self):
        pygame.draw.line(self.screen,(255,255,255),[0, 680],[1280, 680], 5)

        pygame.draw.line(self.screen,(255,255,255),[90, 680],[90, 450], 5)
        pygame.draw.line(self.screen,(255,255,255),[0, 680],[0, 450], 5)
        pygame.draw.line(self.screen,(255,255,255),[90, 450],[0, 450], 10)

        pygame.draw.line(self.screen,(255,255,255),[1190, 680],[1190, 450], 5)
        pygame.draw.line(self.screen,(255,255,255),[1280, 680],[1280, 450], 5)
        pygame.draw.line(self.screen,(255,255,255),[1280, 450],[1190, 450], 10)

        pygame.draw.line(self.screen,(255,255,255),[90, 0],[90, 450], 5)
        pygame.draw.line(self.screen,(255,255,255),[1190, 0],[1190, 450], 5)

        pygame.draw.line(self.screen,(255,255,255),[90, 0],[1190, 0], 5)

        pygame.draw.circle(self.screen, (255,255,255), [640, 680], 10)

    def display_score(self):
        global p1score, p2score
        font = pygame.font.SysFont("assets/font.ttf", 80)
        message = font.render(f"{p1score} - {p2score}", True, (255, 255, 255))
        self.screen.blit(message, (600, 5))

    def reset_ball(self):
        global velocityXright, velocityXleft, velocityY, x1, x2, pause
        velocityXleft, velocityXright, velocityY, x1, x2 = 0, 0, 0, 0, 0

    def reset_game_after_goal(self):
        global pause
        self.player = Player(150, 645)
        self.player2 = Player2(1130, 645)
        self.ball = Ball(640, 400)
        self.reset_ball()
        pause = False

    def collisionsWithBall(self, plyr):
        global velocityXright, velocityXleft, velocityY, x1, x2, pause
        if plyr.posX >= 1255:
            plyr.posX = 1255
        if plyr.posX <= 25:
            plyr.posX = 25
        #Collisin with ball
        if plyr.posX - 25 <= self.ball.posX <= plyr.posX and (self.ball.posY-50 <= plyr.posY <= self.ball.posY+70):
            velocityY = 0.3
            x2 = 0
            x1 = 0
            velocityXleft = 0
            velocityXright = 13
        if plyr.posX <= self.ball.posX <= plyr.posX + 25 and (self.ball.posY-50 <= plyr.posY <= self.ball.posY+70):
            velocityY = 0.3
            x2 = 0
            x1 = 0
            velocityXright = 0
            velocityXleft = 13

    def collisions(self):
        global velocityXright, velocityXleft, velocityY, x1, x2, pause, p1score, p2score
        self.ball.posX -= velocityXright
        self.ball.posX += velocityXleft
        self.ball.posY -= velocityY

        self.ball.posX -= x1
        self.ball.posX += x2

        self.collisionsWithBall(self.player)
        #collision with walls
        if self.ball.posX >= 1170 and self.ball.posY <= 452:
            x1 = 7
            x2 = 0
            velocityXright = 0
            velocityXleft = 0
            velocityY = 0
        if self.ball.posX <= 120 and self.ball.posY <= 452:
            x2 = 7
            x1 = 0
            velocityXright = 0
            velocityXleft = 0
            velocityY = 0
        if self.ball.posX <= 52 and self.ball.posY >= 452:
            self.ball.posX = 25
            self.ball.posY = 660
            pause = True
            p2score += 1
            time.sleep(1)
            self.reset_game_after_goal()
        if self.ball.posX >= 1220 and self.ball.posY >= 452:
            self.ball.posX = 1255
            self.ball.posY = 660
            pause = True
            p1score += 1
            time.sleep(1)
            self.reset_game_after_goal()
        if self.ball.posY <= 25:
            self.ball.posY = 25
        if self.ball.posY >= 665:
            self.ball.posY = 660


class Friend(Game):
    def __init__(self):
        super().__init__()
        self.player2 = None

    def init(self):
        super().init()
        self.player2 = Player2(1130, 645)
    
    def update(self):
        super().update()
        self.player2.update()

    def render(self):
        super().render()
        self.player2.render(self.screen)
        pygame.display.flip()

    def events(self):
        super().events()
        keys = pygame.key.get_pressed()
        if not pause:
            if keys[pygame.K_UP]:
                if self.player2.posY >= 640:
                    self.player2.speed = 18
            if keys[pygame.K_LEFT]:
                self.player2.posX -= 5
            if keys[pygame.K_RIGHT]:
                self.player2.posX += 5

    def collisions(self):
        super().collisions()
        self.collisionsWithBall(self.player2)


class Ai(Game):
    def __init__(self):
        super().__init__()
        self.ai = None

    def init(self):
        super().init()
        self.ai = Player2(1130, 645)
    
    def update(self):
        super().update()
        self.ai.update()
        self.jump()

    def render(self):
        super().render()
        self.ai.render(self.screen)
        pygame.display.flip()

    def collisions(self):
        super().collisions()
        self.collisionsWithBall(self.ai)

        if not pause:
            #Movement
            if self.ball.posX < 640 and self.ai.posX <= 1150:
                self.ai.posX += 4.5
            if self.ball.posX >= 640:
                if self.ai.posX >= self.ball.posX + 20:
                    self.ai.posX -= 4.5
                if self.ai.posX <= self.ball.posX + 20:
                    self.ai.posX += 4.5

    def jump(self):
        if self.ball.posX - 10 <= self.ai.posX <= self.ball.posX + 10 and self.ball.posY < self.ai.posY:
            pass


if __name__ == "__main__":
    app = Menu()
    app.main()
