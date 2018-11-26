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
        self.playSizeX = self.width - 150
        self.play_rect = Rect(0, 0, self.playSizeX, self.height)
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
        self.score = 0
        # TODO Boss stamina bar
        self.staminaBarMax = self.staminaBarCur = self.width * 4/5
        self.current_menu = self.startingMenu
        self.playing = False
        self.playerBulletData = {"vel": -20, "radius": 2}
        self.playerData = {"lives": 3, "velFast": 5, "velSlow": 2,
                           "bulletData": self.playerBulletData, "radius": 5}
        self.clock = pygame.time.Clock()
        self.hitboxGroup = pygame.sprite.Group()
        self.playerReprGroup = pygame.sprite.Group()
        self.playerBulletGroup = pygame.sprite.Group()
        self.monsterGroup = pygame.sprite.Group()
        self.monsterBulletGroup = pygame.sprite.Group()
        self.sidebar = pygame.sprite.RenderPlain(
            sprites.SideBar((self.width - 75, (self.height) / 2),
                            pygame.Surface((150, self.height))))

    def eventListener(self, event):
        pygame.event.pump()
        # print(pygame.key.get_mods())
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
        pygame.display.update()

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
            if monster.stamina < 1:
                # TODO fix this, delete all bullets
                # for b in self.monsterBulletGroup:
                #     b.kill()
                self.staminaBarCur = 0
                self.monsterBulletGroup.empty()

        self.playerBulletGroup.update()
        self.monsterBulletGroup.update(self.play_rect)
        self.playerHitbox.update(self.play_rect, self.monsterBulletGroup)
        self.playerRepr.update(self.play_rect, self.playerHitbox.deltaMoveX,
                               self.playerHitbox.deltaMoveY)
        hitcount = [0]
        self.monsterGroup.update(self.playerBulletGroup, hitcount)
        if hitcount[0] > 0:
            self.score += hitcount[0]
        self.sidebar.update(1, self.score, 3)
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
                pygame.draw.rect(self.screen, (150, 15, 0),
                                 [self.playSizeX // 20, self.playSizeX // 20,
                                  self.playSizeX * 0.9 * self.staminaBarCur / self.staminaBarMax,
                                  2])
            self.sidebar.draw(self.screen)



    def playerSpawn(self, pos):
        # cX, cY = pos

        # Hitbox
        radius = self.playerData["radius"]
        playerHitBoxImgOrigin = pygame.Surface((radius * 2, radius * 2),
                                               pygame.SRCALPHA)
        self.playerData["playerHitBoxImgOrigin"] = playerHitBoxImgOrigin
        playerHitBoxImg = pygame.Surface((radius * 2, radius * 2),
                                         pygame.SRCALPHA)
        # pygame.gfxdraw.filled_circle(playerHitBoxImg, radius, radius, radius, (255, 2, 2))
        # pygame.gfxdraw.filled_circle(playerHitBoxImg, radius, radius, radius-2, (255, 255, 255))
        pygame.draw.ellipse(playerHitBoxImg, (255, 0, 0),
                            [0, 0, radius * 2, radius * 2], 0)
        pygame.draw.ellipse(playerHitBoxImg, (255, 255, 255),
                            [2, 2, radius * 2 - 4, radius * 2 - 4], 0)
        pygame.gfxdraw.filled_circle(playerHitBoxImg, pos[0], pos[1], 3,
                                     (255, 2, 2))
        self.playerData["playerHitBoxImgTrans"] = playerHitBoxImg
        self.playerHitbox = sprites.PlayerHitBox(pos, self.playerData[
            "playerHitBoxImgOrigin"],
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
        # stage 1
        stage1 = levels.Stage1()
        monsterReprImg = stage1.monsterReprImg
        # pygame.draw.rect(monsterReprImg,(255,255,255),(0,0,40,40),1)
        stage1Monster = sprites.Monster((self.playSizeX / 2, 100),
                                        monsterReprImg, stage1.monsterData)
        self.monsterGroup.add(stage1Monster)
        self.staminaBarCur = self.staminaBarMax = stage1.monsterData["stamina"]



    def on_cleanup(self):
        sys.exit()

    def mainLoop(self):
        while (self._running):
            for event in pygame.event.get():
                self.eventListener(event)
            if self.inMenu:
                pygame.display.flip()
            if self.playing:
                self.inMenu = False
                self.inGameUpdate()
        self.on_cleanup()


if __name__ == "__main__":
    mainGame = Main()
    mainGame.mainLoop()
