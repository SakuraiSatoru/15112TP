import sys

import pygame
import pygame.gfxdraw
from pygame.locals import *

import ai.fileIO
import ai.helper
import ai.levels as levels
import ai.sprites as sprites


class App(object):
    def __init__(self, genomes, config):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("PyDanmaku")
        self.size = self.width, self.height = 640, 480
        self.scr_rect = Rect(0, 0, self.width, self.height)
        self.screen = pygame.display.set_mode(self.scr_rect.size,
                                              pygame.DOUBLEBUF)
        self.playSizeX = self.width - 150
        self.play_rect = Rect(0, 0, self.playSizeX, self.height)
        # self.menuInit()
        self.variableInit()
        self.playerSpawn((self.playSizeX // 2, self.height - 50), genomes,
                         config)
        self.initGame(5)

    def variableInit(self):
        print("Initializing variables...")

        self.clockTick = 60
        self.playerBulletData = {"vel": 20, "radius": 2, "fireRate": 2}
        self.playerData = {"lives": 3, "velFast": 5, "velSlow": 2,
                           "bulletData": self.playerBulletData, "radius": 2}
        self.clock = pygame.time.Clock()
        self.hitboxGroup = pygame.sprite.Group()
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
        self.currentMode = 2
        self.bestFitness = 0
        self.crashInfo = []

    def eventListener(self, event):
        pygame.event.pump()
        if event.type == pygame.QUIT:
            self._running = False
            sys.exit()

    def initGame(self, stage=0):
        print("init Game...")
        # self.inMenu = False
        self.currentStage = stage
        self.screen.fill((0, 0, 0))
        self.initSpawnQueue()
        self.currentMode = 2

    def inGameUpdate(self):
        # self.clock.tick(self.clockTick)

        self.enemySpawn()

        if hasattr(self, "monster") and self.monster is not None:
            monster = self.monster
            monster.target.x, monster.target.y = self.playSizeX // 2, self.height - 50
            if monster.shooting:
                monsterBullets = monster.shoot()
                if monsterBullets is not None:
                    for b in monsterBullets:
                        self.monsterBulletGroup.add(b)

            if self.monster.dead and self.monsterGroup.has(self.monster):
                # self.activateBossEmitter()
                self.monster.kill()
                self.monsterGroup.empty()
                self.monsterBulletGroup.empty()
                self.staminaBarGroup.empty()
                self.popUpGroup.empty()
                self.currentMode = 2
                self.currentStage = min(self.currentStage + 1,
                                        len(self.stageList) - 1)
            elif monster.stamina < 1 and not self.monster.dead:
                self.monsterBulletGroup.empty()
                self.popUpGroup.empty()
                if monster.immutable and not monster.dead:
                    monster.stamina = monster.originStamina
            if monster.newSpell[0]:
                self.popUpGroup.empty()
                self.popUpGroup.add(
                    ai.sprites.popUp((-100, 40), pygame.Surface((300, 16)),
                                     monster.newSpell[1]))
                self.monster.newSpell = [False, ""]

        self.monsterBulletGroup.update(self.play_rect)
        # self.playerHitbox.update(self.play_rect, self.monsterBulletGroup)
        if hasattr(self, "monster"):
            self.hitboxGroup.update(self.play_rect, self.monsterBulletGroup,
                                    (self.monster.rect.center))
        else:
            self.hitboxGroup.update(self.play_rect, self.monsterBulletGroup,
                                    (self.playSizeX // 2, 0))

        self.stageNameGroup.update()
        self.popUpGroup.update()
        self.monsterGroup.update(self.monsterBulletGroup,
                                 (self.playSizeX // 2, self.height - 80), )
        if hasattr(self, "monster"):
            self.staminaBarGroup.update(self.monster.stamina,
                                        max(self.monster.currentSpellIndex, 0))
        self.sidebar.update(
            self.stageList[self.currentStage].monsterData["stageName"])
        # frame counter used for fire rate
        self.frameCount += 1
        self.frameCount %= 100
        if hasattr(self, "monster"):
            self.monster.shooting = True
        for index, player in enumerate(self.players):
            if player.dead:
                self.crashInfo.append((player.fitness, player.genome))
                del self.players[index]
                if len(self.players) == 0:
                    # print("returning!")
                    return True

        self.inGameDraw()

    def inGameDraw(self):
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        self.staminaBarGroup.draw(self.screen)
        self.popUpGroup.draw(self.screen)
        self.hitboxGroup.draw(self.screen)
        self.monsterBulletGroup.draw(self.screen)
        self.monsterGroup.draw(self.screen)
        self.sidebar.draw(self.screen)
        self.stageNameGroup.draw(self.screen)

    def playerSpawn(self, pos, genomes, config):
        print("spawning player")
        # Hitbox
        radius = self.playerData["radius"]
        playerHitBoxImgOrigin = pygame.Surface((radius * 2, radius * 2),
                                               pygame.SRCALPHA)
        self.playerData["playerHitBoxImgOrigin"] = playerHitBoxImgOrigin
        self.playerData["playerHitBoxImgTrans"] = playerHitBoxImgOrigin

        # player repr
        playerReprImg = pygame.Surface((26, 26), pygame.SRCALPHA)

        self.players = []
        for genome in genomes:
            player = ai.sprites.PlayerHitBox((pos[0], pos[1] - 4),
                                             playerReprImg, self.playerData,
                                             genome, config)
            self.players.append(player)
            self.hitboxGroup.add(player)

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

        elif (self.currentMode == 2):
            if not self.monsterGroup:
                self.monster = self.monsterList[i]
                self.monsterGroup.add(self.monsterList[i])
                self.staminaBar = self.staminaBarList[i]
                self.staminaBarGroup.add(self.staminaBar)
            else:
                self.stageNameGroup.empty()
                if self.monster.dead:
                    # self.currentMode = 1
                    self.staminaBarGroup.empty()
                    self.stageNameGroup.empty()

    def on_cleanup(self):
        sys.exit()

    def mainLoop(self):
        while (True):
            for event in pygame.event.get():
                self.eventListener(event)
            # if self.inMenu:
            #     pygame.display.flip()
            result = self.inGameUpdate()
            if result:
                return
        # self.on_cleanup()
