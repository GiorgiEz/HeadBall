import pygame, sys, time


BGPLAYBUTTON  = pygame.image.load("assets/MenuBG.png")
BG = pygame.image.load("assets/MenuBGPB.png")
shootVelocityXright = 0
shootVelocityXleft = 0
shootVelocityY = 0
x1Walls, x2Walls = 0, 0
pause = False
p1score, p2score = 0, 0


def useAssets(name, size):
    img = pygame.image.load(f"assets/{name}").convert_alpha()
    return pygame.transform.rotozoom(img, 0, size)

def renderAssets(screen, img, posX, posY):
    w, h = img.get_rect().size
    screen.blit(img, (posX-w/2,posY-h/2))


class Player:
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.speed = 0
        self.img = useAssets("p1.gif", 0.6)

    def update(self):
        #Jumping
        self.posY -= self.speed
        if self.posY > 645:
            self.posY = 645
        self.speed -= 1.5

    def render(self, screen):
        renderAssets(screen, self.img, self.posX, self.posY)

class Player2(Player):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.img = useAssets("p2.gif", 0.6)


class Goal1:
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.img = useAssets("goal_1.png", 1)

    def render(self, screen):
        renderAssets(screen, self.img, self.posX, self.posY)

class Goal2(Goal1):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.img = useAssets("goal_2.png", 1)


class BackGround:
    def __init__(self):
        self.img = useAssets("stadium.jpg", 4)

    def render(self, screen):
        screen.blit(self.img, (0,0))


class Ball:
    global pause
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.velocity = 0.1
        self.acceleration = 0.3
        self.img = useAssets("SoccerBall.png", 0.4)

    def update(self):
        if not pause:
            self.velocity += self.acceleration
            self.posY += self.velocity
            if self.posY >= 660:
                self.velocity = -self.velocity

    def render(self, screen):
        renderAssets(screen, self.img, self.posX, self.posY)


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
        
    def PlayButton(self):
        global pause
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(BGPLAYBUTTON, (0, 0))
            BACK = Button(image=None, pos=(640, 560), 
                                text_input="BACK", font=self.get_font(50), base_color="orange", hovering_color="Green")
            AI = Button(image=None, pos=(640, 200), 
                                text_input="Play with an AI", font=self.get_font(50), base_color="orange", hovering_color="Green")
            FRIEND = Button(image=None, pos=(640, 350), 
                                text_input="Play with a friend", font=self.get_font(50), base_color="orange", hovering_color="Green")
            for button in [BACK, AI, FRIEND]:
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
            pygame.display.update()

    def main(self):
        while True:
            self.screen.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(90).render("HeadBall", True, "orange")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                                text_input="PLAY", font=self.get_font(115), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                                text_input="QUIT", font=self.get_font(85), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.PlayButton()
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
        self.goal1 = None
        self.goal2 = None
        self.background = None

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
        self.goal1 = Goal1(64, 563)
        self.goal2 = Goal2(1215, 563)
        self.background = BackGround()

    def update(self):
        self.events()
        self.player.update()
        self.ball.update()
        self.collisions()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.reset_game()
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
        self.background.render(self.screen)
        self.player.render(self.screen)
        self.ball.render(self.screen)
        self.goal1.render(self.screen)
        self.goal2.render(self.screen)
        self.display_score()
        self.drawLines()
        self.back_button()
        self.display_names("Player 1", 10, 690)
        self.display_names("Player 2", 1185, 690)
        self.clock.tick(60)

    def get_font(self, size):
        return pygame.font.Font("assets/font.ttf", size)

    def drawLines(self):
        pygame.draw.line(self.screen,(255,255,255),[0, 680],[1280, 680], 5)
        pygame.draw.line(self.screen,"grey",[0, 0],[1280, 0], 5)
        pygame.draw.circle(self.screen, (255,255,255), [640, 680], 10)
        pygame.draw.line(self.screen,"grey",[1153, 0],[1152, 444], 7)
        pygame.draw.line(self.screen,"grey",[126, 0],[126, 444], 7)

    def back_button(self):
        self.img = useAssets("Quit Rect.png", 0.34)
        MOUSE_POS = pygame.mouse.get_pos()
        BACK = Button(image=self.img, pos=(62, 22), 
        text_input="BACK", font=self.get_font(28), base_color="grey", hovering_color="Green")
        BACK.changeColor(MOUSE_POS)
        BACK.update(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    self.reset_game()
                    self.menu.PlayButton()

    def text_on_screen(self, fontName, text, posX, posY, color, size):
        font = pygame.font.SysFont(fontName, size)
        message = font.render(text, True, color)
        self.screen.blit(message, (posX, posY))

    def display_names(self, name, posX, posY):
        self.text_on_screen("assets/font.ttf", name, posX, posY, "orange", 30)

    def display_score(self):
        global p1score, p2score
        self.text_on_screen("assets/font.ttf", f"{p1score} - {p2score}", 580, 5, "orange", 80)
        if p1score == 7:
            self.game_over(1)
        if p2score == 7:
            self.game_over(2)

    def game_over(self, plyr):
        global p1score, p2score, pause
        self.text_on_screen("assets/font.ttf", f"Player {plyr} won", 360, 200, "orange", 130)
        pause = True

    def reset_ball_velocity(self, xLeft, xRight, y, x1w, x2w):
        global shootVelocityXright, shootVelocityXleft, shootVelocityY, x1Walls, x2Walls, pause
        shootVelocityXleft, shootVelocityXright, shootVelocityY, x1Walls, x2Walls = xLeft, xRight, y, x1w, x2w

    def reset_game_after_goal(self):
        global pause
        self.player = Player(150, 645)
        self.player2 = Player2(1130, 645)
        self.ai = Player2(1130, 645)
        self.ball = Ball(640, 400)
        self.reset_ball_velocity(0,0,0,0,0)
        self.speed = 0
        pause = False

    def reset_game(self):
        global p1score, p2score
        self.reset_game_after_goal()
        p1score, p2score = 0, 0

    def collisionsWithBall(self, plyr):
        global shootVelocityXright, shootVelocityXleft, shootVelocityY, x1Walls, x2Walls, pause
        if plyr.posX >= 1255:
            plyr.posX = 1255
        if plyr.posX <= 25:
            plyr.posX = 25

        #Collisin with ball
        if plyr.posX - 30 <= self.ball.posX <= plyr.posX and (self.ball.posY-50 <= plyr.posY <= self.ball.posY+50):
            if plyr.posY >= 645:
                self.reset_ball_velocity(0, 8, 0.00001, 0, 0)
            else: self.reset_ball_velocity(0, 14, 0.0001, 0, 0)

        if plyr.posX <= self.ball.posX <= plyr.posX + 30 and (self.ball.posY-50 <= plyr.posY <= self.ball.posY+50):
            if plyr.posY >= 645:
                self.reset_ball_velocity(8, 0, 0.2, 0, 0)
            else: self.reset_ball_velocity(14, 0, 0.1, 0, 0)

    def scoring_goal(self):
        global pause
        pause = True
        time.sleep(1)
        self.reset_game_after_goal()

    def collisions(self):
        global shootVelocityXright, shootVelocityXleft, shootVelocityY, x1Walls, x2Walls, p1score, p2score
        self.ball.posX -= shootVelocityXright
        self.ball.posX += shootVelocityXleft
        self.ball.posY -= shootVelocityY

        self.ball.posX -= x1Walls
        self.ball.posX += x2Walls

        self.collisionsWithBall(self.player)
        #collision with walls
        if self.ball.posX >= 1125 and self.ball.posY <= 452:
            self.reset_ball_velocity(0, 0, 0, 7, 0)

        if self.ball.posX <= 145 and self.ball.posY <= 452:
            self.reset_ball_velocity(0, 0, 0, 0, 7)

        if self.ball.posX <= 90 and self.ball.posY >= 452:
            self.scoring_goal()
            p2score += 1

        if self.ball.posX >= 1190 and self.ball.posY >= 452:
            self.scoring_goal()
            p1score += 1

        if (1180 <= self.ball.posX and 444 <= self.ball.posY <= 460) \
            or (self.ball.posX <= 100 and 444 <= self.ball.posY <= 460):
            self.ball.posY += 30

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
        self.velocity = 140
        self.acceleration = 0.1
        self.speed = 0

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
            
        if self.ai.posY >= 640:
            self.ai.posY == 640

    def jump(self):
        self.ai.posY -= self.speed
        if self.ai.posY > 645:
            self.ai.posY = 645
            delayOnJump = False
        else: delayOnJump = True
        self.speed -= 4.5

        if self.ball.posX - 40 <= self.ai.posX <= self.ball.posX + 40 and self.ai.posY >= self.ball.posY \
        and not delayOnJump and self.ai.posX >= self.ball.posX:
            if self.ball.posY >= 515:
                self.speed = 645 - self.ball.posY
            else: self.speed = 150



if __name__ == "__main__":
    app = Menu()
    app.main()
