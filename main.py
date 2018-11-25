import pygame
from pygame.locals import *
import sys
import sprites
import pygame.gfxdraw
import levels
# code reference: https://www.pygame.org/project/937/1620

class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Term Project")
        self.size = self.width, self.height = 640, 480
        self.scr_rect = Rect(0, 0, self.width, self.height)
        self.screen = pygame.display.set_mode(self.scr_rect.size,
                                              pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.menuInit()
        self.variableInit()
        self.menu(self.startingMenu)

    def menuInit(self):
        print("Initializing menus...")
        titleMenuDict = {"choice": "Press z to start and shoot",
                         "defaultClr": (200, 200, 200), "pos": (40, 150)}
        startGameMenuDict = {"choice": "StartGame", "func": self.initGame,
                             "defaultClr": (200, 200, 200),
                             "focusClr": (255, 255, 255), "pos": (60, 250)}
        tutorialMenuDict = {"choice": "Tutorial", "func": self.initGame,
                             "defaultClr": (200, 200, 200),
                             "focusClr": (255, 255, 255), "pos": (60, 280)}
        quitMenuDict = {"choice": "Quit", "func": sys.exit,
                        "defaultClr": (200, 200, 200),
                        "focusClr": (255, 255, 255), "pos": (60, 310)}
        self.startingMenu = (titleMenuDict, startGameMenuDict, tutorialMenuDict,quitMenuDict)

    def menu(self, choices):
        self.screen.fill((0, 0, 0))
        self.inMenu = True
        self.num_choices = len(choices)
        # self.current_selection = 1
        self.current_menu = choices
        i = 0
        while i < self.num_choices:
            if pygame.font:
                font = pygame.font.Font(None, 28)
                if self.current_selection == i:
                    text = font.render(choices[i]["choice"], 1,
                                       (choices[i]["focusClr"]))
                else:
                    text = font.render(choices[i]["choice"], 1,
                                       (choices[i]["defaultClr"]))
                textpos = choices[i]["pos"]
                self.screen.blit(text, textpos)
            i += 1

    def variableInit(self):
        print("Initializing variables...")
        self._running = True
        self.inMenu = True
        self.current_selection = 1
        self.num_choices = 0
        # TODO Boss stamina bar
        self.staminaBarMax = self.staminaBarCur = self.width * 4/5
        self.current_menu = self.startingMenu
        self.playing = False
        self.playerBulletData = {"vel": -20, "radius": 2}
        self.playerData = {"lives": 3, "vel": 5,"bulletData":self.playerBulletData}
        self.clock = pygame.time.Clock()
        self.hitboxGroup = pygame.sprite.Group()
        self.playerReprGroup = pygame.sprite.Group()
        self.playerBulletGroup = pygame.sprite.Group()
        self.monsterGroup = pygame.sprite.Group()
        self.monsterBulletGroup = pygame.sprite.Group()

    def eventListener(self, event):
        pygame.event.pump()
        if event.type == pygame.QUIT:
            self._running = False
        elif self.inMenu and event.type == KEYDOWN:
            if event.key == K_UP:
                self.current_selection = max(1, self.current_selection - 1)
                self.menu(self.current_menu)
            elif event.key == K_DOWN:
                self.current_selection = min(self.current_selection + 1,
                                             self.num_choices - 1)
                self.menu(self.current_menu)
            elif event.key == K_z:
                self.inMenu = False
                self.screen.fill((0, 0, 0))
                selection = self.current_menu[self.current_selection]
                if "param" in selection:
                    selection["func"](selection["param"])
                elif "func" in selection:
                    selection["func"]()
        elif self.playing and event.type == KEYDOWN and self.playerHitbox.movable:
            self.playerHitbox.keyDown(event.key)
        elif self.playing and event.type == KEYUP and self.playerHitbox.movable:
            self.playerHitbox.keyUp(event.key)

    def initGame(self):
        print("init Game...")
        self.inMenu = False
        self.screen.fill((0, 0, 0))
        # self.playerData = {"lives":3}
        self.playerSpawn((self.width // 2, self.height - 20))
        self.startGame()

    def startGame(self):
        self.playing = True
        self.enemySpawn()


    def inGameUpdate(self):
        self.clock.tick(60)
        if self.playerHitbox.shooting:
            playerBullet = self.playerHitbox.shoot()
            if playerBullet is not None:
                self.playerBulletGroup.add(playerBullet)
        for monster in self.monsterGroup:
            self.staminaBarCur = monster.stamina
            if monster.shooting:
                monsterBullets = monster.shoot()
                if monsterBullets is not None:
                    for b in monsterBullets:
                        self.monsterBulletGroup.add(b)
                print(self.monsterBulletGroup)
            if monster.stamina < 1:
                # TODO fix this, delete all bullets
                # for b in self.monsterBulletGroup:
                #     b.kill()
                self.staminaBarCur = 0
                self.monsterBulletGroup.empty()

        self.playerBulletGroup.update()
        self.monsterBulletGroup.update(self.scr_rect)
        self.playerHitbox.update(self.scr_rect,self.monsterBulletGroup)
        self.playerRepr.update(self.scr_rect, self.playerHitbox.deltaMoveX,
                               self.playerHitbox.deltaMoveY)
        self.monsterGroup.update(self.playerBulletGroup)
        self.inGameDraw()
        if self.playerHitbox.dead:
            self.__init__()

    def inGameDraw(self):
        if not self.inMenu:
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            self.playerReprGroup.draw(self.screen)
            self.hitboxGroup.draw(self.screen)
            self.playerBulletGroup.draw(self.screen)
            self.monsterBulletGroup.draw(self.screen)
            self.monsterGroup.draw(self.screen)
            # stamina bar
            if self.staminaBarCur >0:
                pygame.draw.rect(self.screen,(150,15,0),[self.width//20,self.width//20,self.width*0.9*self.staminaBarCur/self.staminaBarMax,2])



    def playerSpawn(self, pos):
        # cX, cY = pos

        # Hitbox
        playerHitBoxImg = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(playerHitBoxImg, (255, 255, 255), [0, 0, 10, 10],
                            0)
        pygame.draw.ellipse(playerHitBoxImg, (255, 0, 0), [0, 0, 10, 10], 2)
        # pygame.gfxdraw.aacircle(playerHitBoxImg, pos[0], pos[1], 3, (255, 2, 2))
        # pygame.gfxdraw.filled_circle(playerHitBoxImg, pos[0], pos[1], 3, (255, 2, 2))
        self.playerHitbox = sprites.PlayerHitBox(pos, playerHitBoxImg,
                                                 self.playerData)

        # player repr
        playerReprImg = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(playerReprImg, (55, 55, 55), [0, 0, 20, 20], 0)
        # playerReprImg.fill((50, 55, 55))
        self.playerRepr = sprites.PlayerRepr(pos, playerReprImg)

        self.hitboxGroup = pygame.sprite.Group(self.playerHitbox)
        self.playerReprGroup = pygame.sprite.Group(self.playerRepr)
        self.playerHitbox.movable = True

    def enemySpawn(self):
        stage1 = levels.Stage1()
        monsterReprImg = pygame.Surface((40, 40), pygame.SRCALPHA)
        monsterReprImg.fill((0,0,0))
        pygame.draw.rect(monsterReprImg,(255,255,255),(0,0,40,40),1)
        stage1Monster = sprites.Monster((self.width/2,100),monsterReprImg,stage1.monsterData)
        self.monsterGroup.add(stage1Monster)
        self.staminaBarCur = self.staminaBarMax = stage1.monsterData["stamina"]


    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        sys.exit()

    def mainLoop(self):
        while (self._running):
            for event in pygame.event.get():
                self.eventListener(event)
            # self.on_loop()
            # self.on_render()
            if self.inMenu:
                pygame.display.flip()
            if self.playing:
                self.inMenu = False
                self.inGameUpdate()
        self.on_cleanup()


if __name__ == "__main__":
    mainGame = Main()
    mainGame.mainLoop()
