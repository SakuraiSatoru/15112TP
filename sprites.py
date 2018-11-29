import pygame
import pygame.gfxdraw
import random
from pygame.locals import *
import math
import string
import copy
import bulletml

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

    def update(self, scr_size, xMove=0, yMove=0, trans=False):
        if trans and self.image == self.playerReprImg:
            self.image = self.playerReprImgTrans
        elif (not trans) and self.image == self.playerReprImgTrans:
            self.image = self.playerReprImg
        self.rect.move_ip(xMove, yMove)
        # TODO fix this
        self.rect.clamp_ip(
            pygame.Rect(-8, -11, scr_size.width + 16, scr_size.height + 16))


class PlayerHitBox(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, data["playerHitBoxImgOrigin"])
        self.lives = data["lives"]
        self.shooting = False
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

    def update(self, scr_size, bullets):

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
        else:
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


class Monster(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.data = data
        self.bulletData = data["bulletData"]
        self.stamina = data["stamina"]
        self.movePattern = data["moveFunc"]
        self.shooting = False
        self.bulletCount = 0
        self.shootCoolDown = self.shootCoolDownCur = self.bulletData[
            "fireRate"]
        self.target = bulletml.Bullet()
        self.target.x, self.target.y = self.rect.centerx, self.rect.centery + 200
        self.bulletMLInit()

    def update(self, bullets, hitcount, monsterBulletGroup, hitBoxPos):
        if self.stamina < 1:
            self.shooting = False
            self.kill()
        else:
            # shoot cool down
            if self.shootCoolDownCur < 1:
                self.shooting = True
                self.shootCoolDownCur = self.shootCoolDown
            else:
                self.shootCoolDownCur -= 1
                self.shooting = False
            # bullet hit monster
            for b in pygame.sprite.spritecollide(self, bullets, False):
                self.stamina = max(0, self.stamina - 0.5)
                b.kill()
                hitcount[0] += 1

            self.target.x, self.target.y = hitBoxPos
            for obj in list(self.bulletMLActive):
                new = obj.step()
                # TODO where to put this:
                # self.bulletMLActive.update(new)
                if new:
                    for n in new:
                        if not n.vanished:
                            n.repr = self.getBulletRepr()
                            n.repr.rect.center = (n.x, n.y)
                    if not monsterBulletGroup.has(n.repr):  # can be deleted?
                        monsterBulletGroup.add(n.repr)

                self.bulletMLActive.update(new)
                if (obj.finished or not (-50 < obj.x < 600) or not (
                        -50 < obj.y < 600)):
                    self.bulletMLActive.remove(obj)
                    try:
                        monsterBulletGroup.remove(obj.repr)
                    except:
                        print("remove failure!")
                else:
                    # if obj.repr is None:
                    #     obj.repr = self.getBulletRepr()
                    if not obj.vanished:
                        obj.repr.rect.center = (obj.x, obj.y)

    def bulletMLInit(self):
        cx, cy, width, height = self.rect
        cx += width / 2
        cy += height / 2
        ctrpt = cx, cy
        script = self.bulletData["scripts"][0]
        self.bulletMLDoc = bulletml.BulletML.FromDocument(open(script, "rU"))
        self.bulletMLActive = set()

    def bulletMLShoot(self):
        self.bulletMLSource = bulletml.Bullet.FromDocument(self.bulletMLDoc,
                                                           x=self.rect.centerx,
                                                           y=self.rect.centery,
                                                           target=self.target,
                                                           rank=0.2)
        # self.bulletMLSource.repr = self.getBulletRepr()
        self.bulletMLSource.vanished = True
        self.bulletMLActive.add(self.bulletMLSource)
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
        text = font.render(random.choice(string.ascii_uppercase), True,
                           (255, 255, 255))
        self.bulletData["text"] = text
        return MonsterBullet(ctrpt, monsterBulletImg, self.bulletData)

    def shoot(self):
        if self.stamina < 1:
            self.shooting = False
            return None
        elif not self.bulletMLActive:
            self.bulletMLShoot()
            # bullets = []
            # for obj in self.bulletMLActive:
            #     if obj.repr is None:
            #         obj.repr = self.getBulletRepr()
            #         obj.repr.rect.center = (obj.x, obj.y)
            #     bullets.append(obj)

            # x, y, width, height = self.rect
            # x += width / 2
            # y += height / 2
            # ctrpt = x, y
            # monsterBulletImg = pygame.Surface(
            #     (self.bulletData["radius"] * 2, self.bulletData["radius"] * 2),
            #     pygame.SRCALPHA)
            # pygame.draw.ellipse(monsterBulletImg, (255, 255, 255),
            #                     [0, 0, self.bulletData["radius"] * 2,
            #                      self.bulletData["radius"] * 2], 1)
            # # bullet text
            # font = pygame.font.Font("./fonts/monotxt.ttf",
            #                         self.bulletData["fontSize"])
            # text = font.render(random.choice(string.ascii_uppercase), True,
            #                    (255, 255, 255))
            # self.bulletData["text"] = text
            # # TODO fix this
            # self.angle = (self.angle + self.angleIncrement) % 360
            # self.bulletData["angle"] = self.angle
            # bullets = []
            # division = 4
            # for i in range(division):
            #     self.bulletData["angle"] += 360 // division
            #     bullets.append(
            #         MonsterBullet(ctrpt, monsterBulletImg, self.bulletData))
            # self.bulletData["angle"] = self.angle
            # return tuple(bullets)


class MonsterBullet(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.vel = data["vel"]
        self.radius = data["radius"]
        # self.angle = data["angle"]
        self.text = data["text"]
        self.tx = (1 - 2 ** 0.5 / 2) * self.rect.width + 1
        self.ty = (1 - 2 ** 0.5 / 2) * self.rect.height
        self.image.blit(self.text, (self.tx, self.ty))
        # self.deltaMoveX = round(self.vel * math.cos(math.radians(self.angle)))
        # self.deltaMoveY = round(self.vel * math.sin(math.radians(self.angle)))

    def pattern(self):
        pass

    def update(self, scr_rect):
        # self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
        if self.rect.bottom < 0 or self.rect.top > scr_rect.size[
            1] or self.rect.left > scr_rect.size[0] or self.rect.right < 0:
            self.kill()

    def draw(self):
        pass


class SideBar(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)
        pygame.draw.rect(image, (255, 255, 255),
                         (5, 5, self.rect.width - 6, self.rect.height - 6), 1)
        self.image = image
        self.originImg = image.copy()
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


class StaminaBar(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)
