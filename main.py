# CMU 15112 Term Project
# @author Zhihao Fang
# code reference: https://www.pygame.org/project/937/1620
import pygame
from pygame.locals import *
import sys
import sprites
import pygame.gfxdraw
import levels
import bulletml
import libs.PAdLib.particles as particles
import helper
import fileIO
import random


class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("PyDanmaku")
        self.size = self.width, self.height = 640, 480
        self.scr_rect = Rect(0, 0, self.width, self.height)
        self.screen = pygame.display.set_mode(self.scr_rect.size,
                                              pygame.DOUBLEBUF)
        self.playSizeX = self.width - 150
        self.play_rect = Rect(0, 0, self.playSizeX, self.height)
        self.menuInit()
        self.variableInit()
        self.particleInit()
        self.menu(self.startingMenu)

    def menuInit(self):
        print("Initializing menus...")
        titleMenuDict = {"choice": "PyDanmaku     (Press z)",
                         "defaultClr": (200, 200, 200), "pos": (40, 150)}
        startGameMenuDict = {"choice": "StartGame", "func": self.initGame,
                             "defaultClr": (200, 200, 200),
                             "focusClr": (255, 255, 255), "pos": (60, 250)}
        tutorialMenuDict = {"choice": "Tutorial", "func": self.menu,
                            "param": None, "defaultClr": (200, 200, 200),
                            "focusClr": (255, 255, 255), "pos": (60, 280)}
        dataMenuDict = {"choice": "User Data", "func": self.menu,
                        "param": None, "defaultClr": (200, 200, 200),
                        "focusClr": (255, 255, 255), "pos": (60, 310)}
        scoreBoardMenuDict = {"choice": "High Score", "func": self.menu,
                              "param": None, "defaultClr": (200, 200, 200),
                              "focusClr": (255, 255, 255), "pos": (60, 340)}
        quitMenuDict = {"choice": "Quit", "func": sys.exit,
                        "defaultClr": (200, 200, 200),
                        "focusClr": (255, 255, 255), "pos": (60, 370)}
        self.startingMenu = (
            titleMenuDict, startGameMenuDict, tutorialMenuDict, dataMenuDict,
            scoreBoardMenuDict, quitMenuDict)
        tutorialTitleMenuDict = {
            "choice": "z - shoot    lshift - transform    arrow key - movement",
            "defaultClr": (200, 200, 200),
            "pos": (40, 150)}
        tutorialBackMenuDict = {"choice": "Back", "func": self.menu,
                                "param": self.startingMenu,
                                "defaultClr": (200, 200, 200),
                                "focusClr": (255, 255, 255), "pos": (60, 280)}
        self.tutorialMenu = (
            tutorialTitleMenuDict, startGameMenuDict, tutorialBackMenuDict)
        dataTitleMenuDict = {
            "choice": r"Copy folders containg all hwX.py into .\data folder",
            "defaultClr": (200, 200, 200),
            "pos": (40, 150)}
        loadDataMenuDict = {"choice": "Load Data", "func": self.loadUserData,
                            "defaultClr": (200, 200, 200),
                            "focusClr": (255, 255, 255), "pos": (60, 250)}
        deleteDataMenuDict = {"choice": "Delete User Data",
                              "func": self.deleteData,
                              "defaultClr": (200, 200, 200),
                              "focusClr": (255, 255, 255), "pos": (60, 280)}
        dataBackMenuDict = {"choice": "Back", "func": self.menu,
                            "param": self.startingMenu,
                            "defaultClr": (200, 200, 200),
                            "focusClr": (255, 255, 255), "pos": (60, 310)}
        self.dataMenu = (
            dataTitleMenuDict, loadDataMenuDict, deleteDataMenuDict,
            dataBackMenuDict)
        tutorialMenuDict["param"] = self.tutorialMenu
        dataMenuDict["param"] = self.dataMenu
        continueTitleMenuDict = {
            "choices": ["Python is boring...", "Gaming is meaningless...",
                        "STG is outdated...", "You are wasting time...",
                        "Gamers are Baka...", "TP is tedious...",
                        "Are you giving up...", "Do you accept the defeat..."],
            "choice": "Are you giving up...",
            "defaultClr": (200, 200, 200),
            "pos": (40, 150)}
        continueNoMenuDict = {"choice": "No", "func": self.continueGame,
                              "param": 0,
                              "defaultClr": (200, 200, 200),
                              "focusClr": (255, 255, 255), "pos": (60, 250)}
        continueYesMenuDict = {"choice": "Yes", "func": self.__init__,
                               "defaultClr": (200, 200, 200),
                               "focusClr": (255, 255, 255), "pos": (60, 280)}
        self.continueMenu = (
            continueTitleMenuDict, continueNoMenuDict, continueYesMenuDict)
        scoreBoardTitleMenuDict = {"choice": "High Score",
                                   "defaultClr": (200, 200, 200),
                                   "pos": (40, 150)}
        self.highScoreMenu = [scoreBoardTitleMenuDict]
        for i in range(5):
            highscoreMenuDict = {"choice": "%d: 0" % (i + 1),
                                 "defaultClr": (200, 200, 200),
                                 "focusClr": (255, 255, 255),
                                 "pos": (60, 250 + i * 30)}
            self.highScoreMenu.append(highscoreMenuDict)
        highscoreBackMenuDict = {"choice": "Back", "func": self.menu,
                                 "param": self.startingMenu,
                                 "defaultClr": (200, 200, 200),
                                 "focusClr": (255, 255, 255), "pos": (60, 400)}
        self.highScoreMenu.append(highscoreBackMenuDict)
        self.initHighScore()
        scoreBoardMenuDict["param"] = self.highScoreMenu
        clearTitleMenuDict = {
            "choice": "Congrats! You are a master of STG and 112! Check high score.",
            "defaultClr": (200, 200, 200),
            "pos": (40, 150)}
        clearBackMenuDict = {"choice": "back to menu", "func": self.menu,
                             "param": self.startingMenu,
                             "defaultClr": (200, 200, 200),
                             "focusClr": (255, 255, 255), "pos": (60, 250)}
        self.clearMenu = (clearTitleMenuDict, clearBackMenuDict)

    def initHighScore(self):
        d = fileIO.read(r".\data\score.dat")
        if d is not None:
            for i in range(5):
                self.highScoreMenu[i + 1]["choice"] = "%d: %d" % (
                    i + 1, d.get(str(i + 1), 0))

    def continueGame(self, stage):
        self.variableInit()
        self.initGame(stage)

    def loadUserData(self):
        fileIO.write(fileIO.extractScripts(fileIO.walker()))
        self.menu(self.startingMenu)

    def deleteData(self):
        fileIO.delete()
        self.menu(self.startingMenu)

    def menu(self, choices):
        self.screen.fill((0, 0, 0))
        self.inMenu = True
        self.num_choices = len(choices)
        # self.current_selection = 1
        self.current_menu = choices
        self.currentMode = 0
        i = 0
        while i < self.num_choices:
            if pygame.font:
                # font = pygame.font.Font(r".\fonts\CASTWO_ALT.ttf", 15)
                font = pygame.font.Font(None, 28)
                choice = choices[i]["choice"]
                if isinstance(choice, list):
                    choice = random.choice(choice)
                if self.current_selection == i:
                    text = font.render(choice, 1, (choices[i]["focusClr"]))
                else:
                    text = font.render(choice, 1, (choices[i]["defaultClr"]))
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
        self.clockTick = 60
        self.current_menu = self.startingMenu
        self.playing = False
        self.playerBulletData = {"vel": 20, "radius": 2, "fireRate": 2}
        self.playerData = {"lives": 3, "velFast": 5, "velSlow": 2,
                           "bulletData": self.playerBulletData, "radius": 3}
        self.clock = pygame.time.Clock()
        self.hitboxGroup = pygame.sprite.Group()
        self.playerReprGroup = pygame.sprite.Group()
        self.playerBulletGroup = pygame.sprite.Group()
        self.monsterGroup = pygame.sprite.Group()
        self.monsterBulletGroup = pygame.sprite.Group()
        self.stageNameGroup = pygame.sprite.Group()
        self.staminaBarGroup = pygame.sprite.Group()
        self.popUpGroup = pygame.sprite.Group()
        self.sidebar = pygame.sprite.RenderPlain(
            sprites.SideBar((self.width - 75, (self.height) / 2),
                            pygame.Surface((150, self.height))))
        self.frameCount = 0
        self.currentStage = 0
        # 0:menu 1: stagename 2:monster
        self.currentMode = 0
        self.endingCountDown = 100

    def particleInit(self):
        # particle
        self.particleSystem = particles.ParticleSystem()
        self.particleSystem.set_particle_acceleration([0.0, 20.0])

        self.playerDieEmitter = particles.Emitter()
        self.playerDieEmitter.set_density(0)
        self.playerDieEmitter.set_angle(0.0, 360.0)
        self.playerDieEmitter.set_speed([10.0, 200.0])
        self.playerDieEmitter.set_life([0.5, 1])
        self.playerDieEmitter.set_colors([(255, 255, 255)])

        self.bossDieEmitter = particles.Emitter()
        self.bossDieEmitter.set_density(0)
        self.bossDieEmitter.set_angle(0.0, 360.0)
        self.bossDieEmitter.set_speed([10.0, 200.0])
        self.bossDieEmitter.set_life([0.5, 0.8])
        self.bossDieEmitter.set_colors([(255, 255, 255)])

        self.particleSystem.add_emitter(self.playerDieEmitter,
                                        "playerDieEmitter")
        self.particleSystem.add_emitter(self.bossDieEmitter, "bossDieEmitter")

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
                selection = self.current_menu[self.current_selection]
                if "param" in selection:
                    self.screen.fill((0, 0, 0))
                    self.inMenu = False
                    selection["func"](selection["param"])
                elif "func" in selection:
                    self.screen.fill((0, 0, 0))
                    self.inMenu = False
                    selection["func"]()
        elif self.playing and event.type == KEYDOWN and self.playerHitbox.movable:
            self.playerHitbox.keyDown(event.key)
        elif self.playing and event.type == KEYUP and self.playerHitbox.movable:
            self.playerHitbox.keyUp(event.key)
        pygame.display.update()

    def initGame(self, stage=0):
        print("init Game...")
        self.inMenu = False
        self.currentStage = stage
        self.screen.fill((0, 0, 0))
        # self.playerData = {"lives":3}
        self.initSpawnQueue()
        self.playerSpawn((self.playSizeX // 2, self.height + 80))
        self.playerHitbox.lives = 3
        self.playing = True
        self.currentMode = 1
        # self.enemySpawn()

    def inGameUpdate(self):
        self.clock.tick(self.clockTick)

        self.enemySpawn()

        # TODO integrate into plyer and monster class update()
        if self.playerHitbox.shooting:
            playerBullets = self.playerHitbox.shoot()
            if playerBullets is not None:
                for b in playerBullets:
                    if b is not None:
                        self.playerBulletGroup.add(b)
        if hasattr(self, "monster") and self.monster is not None:
            monster = self.monster
            monster.target.x, monster.target.y = self.playerHitbox.rect.center
            if monster.shooting:
                monsterBullets = monster.shoot()
                if monsterBullets is not None:
                    for b in monsterBullets:
                        self.monsterBulletGroup.add(b)

            if self.monster.dead and self.monsterGroup.has(self.monster):
                self.activateBossEmitter()
                self.monster.kill()
                self.monsterGroup.empty()
                self.monsterBulletGroup.empty()
                self.staminaBarGroup.empty()
                self.popUpGroup.empty()
                self.currentMode = 1
                self.currentStage = min(self.currentStage + 1,
                                        len(self.stageList) - 1)
            elif monster.stamina < 1 and not self.monster.dead:
                self.monsterBulletGroup.empty()
                self.popUpGroup.empty()
                if monster.immutable and not monster.dead:
                    monster.stamina = monster.originStamina
                if monster.immutable and monster.immutableCount == 0:
                    self.activateBossEmitter()
            elif self.monster.dead and hasattr(self,
                                               "playerHitbox") and self.playerHitbox.lives > 0 and self.currentStage == len(
                    self.stageList) - 1:
                self.playing = False
                self.inMenu = True
                self.menu(self.clearMenu)
            if monster.newSpell[0]:
                self.popUpGroup.empty()
                self.popUpGroup.add(
                    sprites.popUp((-100, 40), pygame.Surface((300, 16)),
                                  monster.newSpell[1]))
                self.monster.newSpell = [False, ""]

        self.playerBulletGroup.update()
        self.monsterBulletGroup.update(self.play_rect)
        self.playerHitbox.update(self.play_rect, self.monsterBulletGroup)
        self.playerRepr.update(self.play_rect, self.playerHitbox.rect.center,
                               self.playerHitbox.transform)

        self.stageNameGroup.update()
        self.popUpGroup.update()
        hitcount = [0]
        self.monsterGroup.update(self.playerBulletGroup, hitcount,
                                 self.monsterBulletGroup,
                                 self.playerHitbox.rect.center)
        if hitcount[0] > 0:
            self.score += hitcount[0]
        if hasattr(self, "monster"):
            self.staminaBarGroup.update(self.monster.stamina,
                                        max(self.monster.currentSpellIndex, 0))
        self.sidebar.update(
            self.stageList[self.currentStage].monsterData["stageName"],
            self.score, self.playerHitbox.lives)
        # frame counter used for fire rate
        self.frameCount += 1
        self.frameCount %= 100
        self.particleSystem.update(1 / self.clockTick)
        if hasattr(self, "monster") and self.playerHitbox.spawnDur == 2:
            self.monster.shooting = True
        elif hasattr(self, "monster") and self.playerHitbox.spawnDur > 2:
            self.monsterBulletGroup.empty()
        if self.playerHitbox.dead:
            if self.playerHitbox.lives == 0:
                if self.endingCountDown == 100:
                    self.activePlayerEmitter()
                    self.monster.shooting = False
                    self.endingCountDown -= 1
                elif self.endingCountDown > 0:
                    self.endingCountDown -= 1
                else:
                    try:
                        fileIO.writeScore(self.score)
                    except:
                        print("failed to save score")
                    self.inMenu = True
                    self.playing = False
                    self.continueMenu[1]["param"] = self.currentStage
                    self.continueMenu[0]["choice"] = random.choice(
                        self.continueMenu[0]["choices"])
                    self.menu(self.continueMenu)
            elif self.playerHitbox.spawnWaiting == self.playerHitbox.spawnWait:
                self.monster.shooting = False
                self.activePlayerEmitter()
            elif self.playerHitbox.spawnWaiting <= 10:
                self.monsterBulletGroup.empty()
        self.inGameDraw()

    def activateBossEmitter(self):
        self.particleSystem.emitters["bossDieEmitter"].set_position(
            self.monster.rect.center)
        self.particleSystem.emitters["bossDieEmitter"].set_density(500)
        self.particleSystem.emitters["bossDieEmitter"]._padlib_update(
            self.particleSystem, 0.2)
        self.particleSystem.emitters["bossDieEmitter"].set_density(0)

    def activePlayerEmitter(self):
        self.particleSystem.emitters["playerDieEmitter"].set_position(
            self.playerHitbox.rect.center)
        self.particleSystem.emitters["playerDieEmitter"].set_density(500)
        self.particleSystem.emitters["playerDieEmitter"]._padlib_update(
            self.particleSystem, 0.2)
        self.particleSystem.emitters["playerDieEmitter"].set_density(0)

    def inGameDraw(self):
        if not self.inMenu:
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            self.staminaBarGroup.draw(self.screen)
            self.popUpGroup.draw(self.screen)
            if not self.playerHitbox.dead:
                self.playerReprGroup.draw(self.screen)
                self.hitboxGroup.draw(self.screen)
            self.playerBulletGroup.draw(self.screen)
            self.particleSystem.draw(self.screen)
            self.monsterBulletGroup.draw(self.screen)
            self.monsterGroup.draw(self.screen)
            self.sidebar.draw(self.screen)
            self.stageNameGroup.draw(self.screen)

    def playerSpawn(self, pos):
        # Hitbox
        radius = self.playerData["radius"]
        playerHitBoxImgOrigin = pygame.Surface((radius * 2, radius * 2),
                                               pygame.SRCALPHA)
        self.playerData["playerHitBoxImgOrigin"] = playerHitBoxImgOrigin
        self.playerData["playerHitBoxImgTrans"] = playerHitBoxImgOrigin
        self.playerHitbox = sprites.PlayerHitBox(pos, self.playerData[
            "playerHitBoxImgOrigin"], self.playerData)

        # player repr
        playerReprImg = pygame.Surface((26, 26), pygame.SRCALPHA)
        self.playerRepr = sprites.PlayerRepr((pos[0], pos[1] - 4),
                                             playerReprImg)

        self.hitboxGroup = pygame.sprite.Group(self.playerHitbox)
        self.playerReprGroup = pygame.sprite.Group(self.playerRepr)
        # self.playerHitbox.movable = True

    def initSpawnQueue(self):
        print("initializing spawn queue...")
        self.stageList = [levels.Stage1(), levels.Stage2(), levels.Stage3(),
                          levels.Stage4(), levels.Stage5(), levels.Stage6(),
                          levels.Stage7(), levels.Stage8(), levels.Stage9(),
                          levels.Stage10()]
        self.stageNameList = []
        self.monsterList = []
        self.staminaBarList = []
        for stage in self.stageList:
            stagename = sprites.StageName((self.playSizeX / 2, -50),
                                          pygame.Surface((300, 60)),
                                          stage.monsterData)
            self.stageNameList.append(stagename)
            monster = sprites.Monster((self.playSizeX / 2, -50),
                                      stage.monsterReprImg, stage.monsterData)
            self.monsterList.append(monster)
            staminaBarData = {"spellNum": stage.monsterData["spellNum"],
                              "width": 4, "margin": 4,
                              "originStamina": stage.monsterData["stamina"]}
            staminaBar = sprites.StaminaBar((self.playSizeX / 2, 20),
                                            pygame.Surface(
                                                (self.playSizeX - 30, 1)),
                                            staminaBarData)
            self.staminaBarList.append(staminaBar)

    def enemySpawn(self):
        i = self.currentStage
        if (self.currentMode == 1):
            self.monsterGroup.empty()
            self.staminaBarGroup.empty()
            if self.stageNameGroup:
                for s in self.stageNameGroup:
                    if s.duration <= 0:
                        self.stageNameGroup.empty()
                        self.currentMode = 2
                        break
            else:
                self.stageNameGroup.add(self.stageNameList[i])
                if hasattr(self, "playerHitbox"):
                    self.playerHitbox.bulletData.update(
                        self.stageList[i].playerBulletData)
                    self.playerHitbox.shootable = False

        elif (self.currentMode == 2):
            if not self.monsterGroup:
                if hasattr(self, "playerHitbox"):
                    self.playerHitbox.shootable = True
                self.monster = self.monsterList[i]
                self.monsterGroup.add(self.monsterList[i])
                self.staminaBar = self.staminaBarList[i]
                self.staminaBarGroup.add(self.staminaBar)
            else:
                self.stageNameGroup.empty()
                if self.monster.dead:
                    self.currentMode = 1
                    self.staminaBarGroup.empty()
                    self.stageNameGroup.empty()

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
