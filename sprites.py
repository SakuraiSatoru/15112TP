import pygame
import pygame.gfxdraw
import random
from pygame.locals import *
import math
import string
import copy
import bulletml
import helper

class Sprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint


class PlayerRepr(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)
        self.originImg = image.copy()
        self.playerReprImg = image.copy()
        self.playerReprImgTrans = image.copy()
        self.playerReprPolyPts = [(10, 13), (10, 2), (1, 20), (7, 24),
                                  (10, 24), (10, 19)]
        self.playerReprImgLeft = pygame.Surface((13, 26), pygame.SRCALPHA)
        self.playerReprPoly1 = pygame.draw.aalines(self.playerReprImgLeft,
                                                   (255, 255, 255), False,
                                                   self.playerReprPolyPts)
        self.playerReprImgRight = pygame.transform.flip(self.playerReprImgLeft,
                                                        True,
                                                        False)
        self.playerReprImg.blit(self.playerReprImgLeft, (0, 0))
        self.playerReprImg.blit(self.playerReprImgRight, (13, 0))
        pygame.gfxdraw.circle(self.playerReprImg, 13, 16, 4, (255, 255, 255))
        self.image = self.playerReprImg

        self.playerReprImgTrans.blit(self.playerReprImgLeft, (1, 0))
        self.playerReprImgTrans.blit(self.playerReprImgRight, (12, 0))

    def update(self, scr_size, center, trans=False):
        self.rect.center = center[0], center[1] - 4
        if trans and self.image == self.playerReprImg:
            self.image = self.playerReprImgTrans
        elif (not trans) and self.image == self.playerReprImgTrans:
            self.image = self.playerReprImg


class PlayerHitBox(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, data["playerHitBoxImgOrigin"])
        self.originCenter = centerPoint
        self.spawnWaiting = self.spawnWait = 50  # count down of hit towards respawn
        self.spawnDur = 100  # count down of spawn movement
        self.lives = data["lives"]
        self.shooting = False
        self.shootable = True
        self.movable = False
        self.deltaMoveX = self.deltaMoveY = 0
        self.vel = data["velFast"]
        self.velFast = data["velFast"]
        self.velSlow = data["velSlow"]
        self.radius = image.get_rect().size[0] // 2
        self.data = data
        self.bulletData = data["bulletData"]
        self.dead = False
        self.originImg = data["playerHitBoxImgOrigin"]
        self.transformImg = data["playerHitBoxImgTrans"]
        self.transform = False
        self.keyHold = []
        self.target = self.rect.center
        self.newPath = None
        self.pathInit(self.rect.centerx, self.rect.centery)

    def pathInit(self, x=300, y=5):
        pathDoc = bulletml.BulletML.FromDocument(
            open(r".\scripts\0_1.xml", "rU"))
        self.pathActive = set()
        self.pathSource = bulletml.Bullet.FromDocument(pathDoc,
                                                       x=x, y=y,
                                                       target=self.target,
                                                       rank=1)
        # self.pathSource.vanished = True
        self.pathActive.add(self.pathSource)


    def update(self, scr_size, bullets):
        if self.spawnDur > 0:
            self.shootable = False
            self.spawnDur -= 1
            # make movement
            if len(self.pathActive) > 0:
                for path in list(self.pathActive):
                    newPath = path.step()
                    if len(newPath) > 0 and self.newPath is None:
                        self.newPath = newPath[0]
                        self.pathActive.clear()
            if self.newPath is not None:
                self.rect.center = self.newPath.x, self.newPath.y
                self.newPath.step()
        else:
            self.movable = True
            self.shootable = True

        if self.dead:
            self.shootable = False
            self.movable = False
            if self.lives > 0:
                self.spawnWaiting -= 1
            if self.spawnWaiting < 1:
                self.respawn()
            return





        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.vel = self.velFast
        self.transform = False
        if K_LSHIFT in self.keyHold:
            self.transform = True
            self.vel = self.velSlow
        if K_UP in self.keyHold:
            self.deltaMoveY -= self.vel
        if K_DOWN in self.keyHold:
            self.deltaMoveY += self.vel
        if K_LEFT in self.keyHold:
            self.deltaMoveX -= self.vel
        if K_RIGHT in self.keyHold:
            self.deltaMoveX += self.vel
        if K_z in self.keyHold:
            self.shooting = True
        else:
            self.shooting = False

        if self.transform and self.image == self.originImg:
            self.image = self.transformImg
        elif (not self.transform and self.image == self.transformImg):
            self.image = self.originImg

        if self.movable:
            self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
            self.rect.clamp_ip(scr_size)

        if self.lives < 1:
            self.movable = False
            self.shooting = False
            self.kill()

        for b in pygame.sprite.spritecollide(self, bullets, False):
            self.dead = True
            self.lives -= 1
            b.kill()
            self.kill()

    def keyDown(self, key):
        if key not in self.keyHold:
            self.keyHold.append(key)

    def keyUp(self, key):
        if key in self.keyHold:
            self.keyHold.remove(key)

    def shoot(self):
        if self.lives < 1:
            self.shooting = False
            return None
        elif self.shootable:
            x, y, width, height = self.rect
            x += (width / 2)
            ctrpt = x, y
            playerBulletImg = pygame.Surface(
                (self.bulletData["radius"] * 2, self.bulletData["radius"] * 2),
                pygame.SRCALPHA)
            pygame.draw.ellipse(playerBulletImg, (255, 255, 255),
                                [0, 0, self.bulletData["radius"] * 2,
                                 self.bulletData["radius"] * 2], 0)
            # pygame.gfxdraw.filled_circle(playerBulletImg, self.bulletData["radius"], self.bulletData["radius"], self.bulletData["radius"], (255, 255, 255))

            bulletPosLst = self.getBulletPos()
            bulletList = []
            for i in range(len(bulletPosLst)):
                bulletData = copy.deepcopy(self.bulletData)
                if self.transform:
                    bulletData["angle"] = self.bulletData["slowAngleList"][i]
                else:
                    bulletData["angle"] = self.bulletData["fastAngleList"][i]
                newBullet = PlayerBullet(bulletPosLst[i], playerBulletImg,
                                         bulletData)
                bulletList.append(newBullet)
            return bulletList
        return None

    def getBulletPos(self):
        if not self.transform:
            lst = self.bulletData["fastAngleList"]
        else:
            lst = self.bulletData["slowAngleList"]
        returnLst = []
        offset = 2
        if len(lst) % 2 > 0 and 0 in lst:
            returnLst.append(self.rect.center)
            offset = 4
        for i in reversed(range(len(lst) // 2)):
            if lst[i] == 0:
                returnLst.insert(0, (
                    self.rect.centerx - offset, self.rect.centery))
                returnLst.append(
                    (self.rect.centerx + offset, self.rect.centery))
                offset += 4
            else:
                returnLst.insert(0, self.rect.center)
                returnLst.append(self.rect.center)
        return returnLst

    def respawn(self):
        self.data["lives"] -= 1
        self.__init__(self.originCenter, self.data["playerHitBoxImgOrigin"],
                      self.data)


class PlayerBullet(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.vel = data["vel"]
        self.radius = data["radius"]
        self.angle = data["angle"]
        self.deltaMoveX = math.cos(math.radians(self.angle + 90)) * self.vel
        self.deltaMoveY = - math.sin(math.radians(self.angle + 90)) * self.vel

    def update(self):
        self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
        if self.rect.bottom < 0:
            self.kill()


class StageName(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        # self.image.fill((255,255,255))
        self.originImg = self.image.copy()
        self.target = bulletml.Bullet()
        self.dead = False
        self.data = data
        self.name = data["stageName"]
        self.descript = data["stageDescript"]
        # self.immutable = True
        self.path = r".\scripts\0_0.xml"
        self.newPath = None
        self.pathInit(self.rect.centerx, self.rect.centery)
        self.duration = 2500

    def pathInit(self, x, y):
        self.pathDoc = bulletml.BulletML.FromDocument(open(self.path, "rU"))
        self.pathActive = set()
        self.pathSource = bulletml.Bullet.FromDocument(self.pathDoc,
                                                       x=x,
                                                       y=y,
                                                       target=self.target,
                                                       rank=1)
        # self.pathSource.vanished = True
        self.pathActive.add(self.pathSource)

    def update(self):
        clr = max(min(255, self.duration), 0)
        self.image = self.originImg.copy()
        # font = pygame.font.Font("./fonts/monotxt.ttf", 20)
        font = pygame.font.Font(None, 24)
        text = font.render("Stage: " + self.name, True, (clr, clr, clr))
        self.image.blit(text, (
        self.image.get_rect().width / 2 - text.get_rect().width / 2, 0))
        font = pygame.font.Font(None, 18)
        text = font.render(self.descript, True, (clr, clr, clr))
        self.image.blit(text, (
        self.image.get_rect().width / 2 - text.get_rect().width / 2, 24))

        self.duration -= 10
        if self.duration < 0:
            self.dead = True
            self.kill()
        else:
            # make movement
            if len(self.pathActive) > 0:
                for path in list(self.pathActive):
                    newPath = path.step()
                    if len(newPath) > 0 and self.newPath is None:
                        self.newPath = newPath[0]
                        self.pathActive.clear()
            if self.newPath is not None:
                self.rect.center = self.newPath.x, self.newPath.y
                self.newPath.step()


class popUp(StageName):
    def __init__(self, centerPoint, image, text):
        Sprite.__init__(self, centerPoint, image)
        self.originImg = self.image.copy()
        self.target = bulletml.Bullet()
        self.dead = False
        self.text = text
        self.path = r".\scripts\0_3.xml"
        self.newPath = None
        self.pathInit(self.rect.centerx, self.rect.centery)
        self.duration = 8000

    def update(self):
        clr = max(min(255, self.duration), 0)
        self.image = self.originImg.copy()
        # font = pygame.font.Font("./fonts/monotxt.ttf", 20)
        font = pygame.font.Font(None, 16)
        text = font.render("Spell Func <" + self.text + ">", True,
                           (clr, clr, clr))
        self.image.blit(text, (0, 0))

        self.duration -= 20
        if self.duration < 0:
            self.dead = True
            self.kill()
        else:
            # make movement
            if len(self.pathActive) > 0:
                for path in list(self.pathActive):
                    newPath = path.step()
                    if len(newPath) > 0 and self.newPath is None:
                        self.newPath = newPath[0]
                        self.pathActive.clear()
            if self.newPath is not None:
                self.rect.center = self.newPath.x, self.newPath.y
                self.newPath.step()

class Monster(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.dead = False
        self.data = data
        self.shooting = False
        self.bulletData = data["bulletData"]
        self.originStamina = self.stamina = data["stamina"]
        self.path = data["path"]
        self.bulletCount = 0
        self.target = bulletml.Bullet()
        self.target.x, self.target.y = self.rect.centerx, self.rect.centery + 200
        self.immutable = True
        self.immutableDur = 100
        self.immutableCount = 0
        self.spellNum = data["spellNum"]
        self.currentSpellIndex = -1
        self.bulletMLInit()
        self.newPath = None
        self.pathInit(self.rect.centerx, self.rect.centery)
        self.generator = self.getBulletChar()
        # indicator of new popUp
        self.newSpell = [False, ""]

    def update(self, bullets, hitcount, monsterBulletGroup, hitBoxPos):
        # make movement
        if len(self.pathActive) > 0:
            for path in list(self.pathActive):
                newPath = path.step()
                if len(newPath) > 0 and self.newPath is None:
                    self.newPath = newPath[0]
                    self.pathActive.clear()
        if self.newPath is not None:
            self.rect.center = self.newPath.x, self.newPath.y
            self.newPath.step()

        if self.stamina < 1:
            self.shooting = False
            self.immutable = True
            self.immutableCount = 0
        else:
            if self.immutable and self.immutableCount < self.immutableDur:
                self.immutableCount += 1
                self.shooting = False
            elif self.immutable:
                self.immutableCount = 0
                if self.currentSpellIndex < 0:
                    self.currentSpellIndex = 0
                self.immutable = False
                self.shooting = True
                self.newSpell = [True, self.getSpellName()]
            # # bullet hit monster
            for b in pygame.sprite.spritecollide(self, bullets, False):
                self.damage(5)
                b.kill()
                hitcount[0] += 1

            # handle bullets
            self.target.x, self.target.y = hitBoxPos
            if not hasattr(self, "bulletMLActive"):
                return


            for obj in list(self.bulletMLActive):
                new = obj.step()
                self.bulletMLActive.update(new)
                if (obj.finished or not (-50 < obj.x < 600) or not (
                        -50 < obj.y < 600)):
                    self.bulletMLActive.remove(obj)
                    if hasattr(obj, "repr") and monsterBulletGroup.has(
                            obj.repr):
                        monsterBulletGroup.remove(obj.repr)
            for obj in self.bulletMLActive:
                if not obj.vanished:
                    if hasattr(obj, "repr"):
                        obj.repr.rect.center = (obj.x, obj.y)
                    else:
                        obj.repr = self.getBulletRepr()
                        obj.repr.rect.center = (obj.x, obj.y)
                        monsterBulletGroup.add(obj.repr)
                else:
                    if hasattr(obj, "repr") and monsterBulletGroup.has(
                            obj.repr):
                        monsterBulletGroup.remove(obj.repr)


    def pathInit(self, x=300, y=5):
        self.pathDoc = bulletml.BulletML.FromDocument(open(self.path, "rU"))
        self.pathActive = set()
        self.pathSource = bulletml.Bullet.FromDocument(self.pathDoc,
                                                       x=x,
                                                       y=y,
                                                       target=self.target,
                                                       rank=1)
        self.pathActive.add(self.pathSource)

    def bulletMLInit(self):
        self.script = self.bulletData["scripts"][
            max(self.currentSpellIndex, 0)]

    def bulletMLShoot(self):
        print(self.script)
        self.bulletMLDoc = bulletml.BulletML.FromDocument(
            open(self.script, "rU"))
        self.bulletMLSource = bulletml.Bullet.FromDocument(self.bulletMLDoc,
                                                           x=self.rect.centerx,
                                                           y=self.rect.centery,
                                                           target=self.target,
                                                           rank=0.2)
        # self.bulletMLSource.repr = self.getBulletRepr()
        # self.bulletMLActive.add([self.bulletMLSource])
        self.bulletMLActive = set([self.bulletMLSource])
        self.bulletMLSource.vanished = True
        # return self.target, self.bulletMLActive

    def getBulletRepr(self):
        x, y, width, height = self.rect
        x += width / 2
        y += height / 2
        ctrpt = x, y
        monsterBulletImg = pygame.Surface(
            (self.bulletData["radius"] * 2, self.bulletData["radius"] * 2),
            pygame.SRCALPHA)
        pygame.draw.ellipse(monsterBulletImg, (255, 255, 255),
                            [0, 0, self.bulletData["radius"] * 2,
                             self.bulletData["radius"] * 2], 1)
        # bullet text
        # font = pygame.font.Font("./fonts/monotxt.ttf",
        #                         self.bulletData["fontSize"])
        font = pygame.font.Font(None, self.bulletData["fontSize"])
        text = font.render(next(self.generator), True, (255, 255, 255))
        self.bulletData["text"] = text
        return MonsterBullet(ctrpt, monsterBulletImg, self.bulletData)

    def getBulletChar(self):
        i = 0
        prev = self.currentSpellIndex
        while True:
            if prev != self.currentSpellIndex:
                i = 0
                prev = self.currentSpellIndex
            c = self.bulletData["pyScripts"][self.currentSpellIndex][i]
            if c != " ":
                yield c
            i = (i + 1) % len(
                self.bulletData["pyScripts"][self.currentSpellIndex])

    def getSpellName(self):
        s = self.bulletData["pyScripts"][self.currentSpellIndex].split("(")[0][
            4:]
        return s

    def shoot(self):
        if not self.shooting or self.stamina < 1:
            self.shooting = False
            self.bulletMLActive.clear()
            return
        elif (not hasattr(self, "bulletMLActive")) or (
        not self.bulletMLActive):
            self.bulletMLShoot()

    def damage(self, bulletDamage):
        if not self.immutable:
            self.stamina = max(self.stamina - bulletDamage, 0)
        if self.stamina == 0 and not self.immutable:
            self.immutable = True
            if self.currentSpellIndex < self.spellNum - 1:
                self.currentSpellIndex += 1
                self.bulletMLInit()
            else:
                self.dead = True


class MonsterBullet(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.vel = data["vel"]
        self.radius = data["radius"]
        self.text = data["text"]
        self.tx = (1 - 2 ** 0.5 / 2) * self.rect.width + 1
        self.ty = (1 - 2 ** 0.5 / 2) * self.rect.height
        self.image.blit(self.text, (self.tx, self.ty))

    def pattern(self):
        pass

    def update(self, scr_rect):
        # self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
        if self.rect.bottom < 0 or self.rect.top > scr_rect.size[
            1] or self.rect.left > scr_rect.size[0] or self.rect.right < 0:
            self.kill()


class SideBar(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)
        # pygame.draw.rect(image, (255, 255, 255),
        #                  (5, 5, self.rect.width - 6, self.rect.height - 6), 1)
        # helper.filledRoundedRect(self.image, self.rect, (255,255,255), 0.2)
        helper.filledRoundedRect(self.image, (
        8, 8, self.rect.width - 16, self.rect.height - 16), (255, 255, 255),
                                 0.2)
        helper.filledRoundedRect(self.image, (
        9, 9, self.rect.width - 18, self.rect.height - 18), (0, 0, 0), 0.2)
        self.originImg = self.image.copy()
        self.stage = 1
        self.score = 0
        self.lives = 0

    def update(self, stage, score, lives):
        self.stage = stage
        self.score = score
        self.lives = lives
        self.image = self.originImg.copy()
        font = pygame.font.Font(None, 30)
        text = font.render("Stage: %s" % self.stage, True, (255, 255, 255))
        self.image.blit(text, (20, 40))
        text = font.render("Score: %s" % self.score, True, (255, 255, 255))
        self.image.blit(text, (20, 100))
        text = font.render("Lives: %s" % self.lives, True, (255, 255, 255))
        self.image.blit(text, (20, 160))


class StaminaBar(Sprite):
    # dict data:
    #     int spellCount
    #     int originStamina
    #     int width: default cell width
    #     int margin
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.img = self.image.copy()
        self.spellCount = data["spellNum"]
        self.stamina = self.originStamina = data["originStamina"]
        self.currentSpell = -1
        self.width = data["width"]
        self.margin = data["margin"]
        self.remainSpellImg = pygame.Surface((self.width, self.rect.height))
        self.remainSpellImg.fill((255, 255, 255))
        self.recovery = True
        self.recoveryProgres = 0
        self.immutable = True

    def update(self, stamina, currentSpell):
        # self.stamina = stamina
        if self.currentSpell < currentSpell or self.currentSpell == -1:
            self.recovery = True
        self.currentSpell = currentSpell
        self.image = self.img.copy()
        pos = [0, 0]
        # draw remaining rect
        for i in range(
                self.spellCount - self.currentSpell - 1):  # n of remaining spells
            self.image.blit(self.remainSpellImg, pos)
            pos[0] += self.width + self.margin
        l1 = self.rect.width - pos[0]
        # draw current bar
        if not self.recovery:
            l2 = l1 * stamina // self.originStamina
            self.recoveryProgres = 0  # reset
            currentBar = pygame.Surface((l2, self.rect.height))
        else:
            if self.recoveryProgres < l1:
                self.recoveryProgres += 10
            else:
                self.recovery = False
            currentBar = pygame.Surface(
                (self.recoveryProgres, self.rect.height))
        currentBar.fill((255, 255, 255))
        self.image.blit(currentBar, pos)

