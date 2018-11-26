import pygame
import pygame.gfxdraw
import random
from pygame.locals import *
import math
import string
import copy


class Sprite(pygame.sprite.Sprite):

    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint


class PlayerRepr(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)

    def update(self, scr_size, xMove=0, yMove=0):
        self.rect.move_ip(xMove, yMove)
        # TODO fix this
        self.rect.clamp_ip(
            pygame.Rect(-5, -5, scr_size.width + 10, scr_size.height + 10))


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
            return PlayerBullet(ctrpt, playerBulletImg, self.bulletData)


class PlayerBullet(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.vel = data["vel"]
        self.radius = data["radius"]

    def update(self):
        self.rect.move_ip(self.deltaMoveX, self.deltaMoveY + self.vel)
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
        # TODO integrate this into data
        self.angle = 90
        self.angleIncrement = 10

    def update(self, bullets, hitcount):
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
                self.stamina = max(0, self.stamina - 0.3)
                b.kill()
                hitcount[0] += 1

    def shoot(self):
        if self.stamina < 1:
            self.shooting = False
            return None
        else:
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
            font = pygame.font.Font("./fonts/monotxt.ttf",
                                    self.bulletData["fontSize"])
            text = font.render(random.choice(string.ascii_uppercase), True,
                               (255, 255, 255))
            self.bulletData["text"] = text
            # TODO fix this
            self.angle = (self.angle + self.angleIncrement) % 360
            self.bulletData["angle"] = self.angle
            bullets = []
            division = 4
            for i in range(division):
                self.bulletData["angle"] += 360 // division
                bullets.append(
                    MonsterBullet(ctrpt, monsterBulletImg, self.bulletData))
            self.bulletData["angle"] = self.angle
            return tuple(bullets)


class MonsterBullet(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.vel = data["vel"]
        self.radius = data["radius"]
        self.angle = data["angle"]
        self.text = data["text"]
        self.tx = (1 - 2 ** 0.5 / 2) * self.rect.width + 1
        self.ty = (1 - 2 ** 0.5 / 2) * self.rect.height
        self.image.blit(self.text, (self.tx, self.ty))
        self.deltaMoveX = round(self.vel * math.cos(math.radians(self.angle)))
        self.deltaMoveY = round(self.vel * math.sin(math.radians(self.angle)))

    def pattern(self):
        pass

    def update(self, scr_rect):
        self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
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
