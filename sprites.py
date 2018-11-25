import pygame
import pygame.gfxdraw
import random
from pygame.locals import *
import math
import string

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
        self.rect.clamp_ip(pygame.Rect(-5, -5, 650, 490))


class PlayerHitBox(Sprite):
    def __init__(self, centerPoint, image, data):
        Sprite.__init__(self, centerPoint, image)
        self.lives = data["lives"]
        self.shooting = False
        self.movable = False
        self.deltaMoveX = self.deltaMoveY = 0
        self.vel = data["vel"]
        self.radius = image.get_rect().size[0] // 2
        self.data = data
        self.bulletData = data["bulletData"]
        self.dead = False

    def update(self, scr_size, bullets):
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
        if key == K_UP:
            self.deltaMoveY -= self.vel
        if key == K_DOWN:
            self.deltaMoveY += self.vel
        if key == K_RIGHT:
            self.deltaMoveX += self.vel
        if key == K_LEFT:
            self.deltaMoveX -= self.vel
        if key == K_z:
            self.shooting = True

    def keyUp(self, key):
        if key == K_UP:
            self.deltaMoveY += self.vel
        if key == K_DOWN:
            self.deltaMoveY -= self.vel
        if key == K_RIGHT:
            self.deltaMoveX -= self.vel
        if key == K_LEFT:
            self.deltaMoveX += self.vel
        if key == K_z:
            self.shooting = False

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
        self.shootCoolDown = self.shootCoolDownCur = self.bulletData["fireRate"]
        # TODO integrate this into data
        self.angle = 90
        self.angleIncrement = 10


    def update(self, bullets):
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
                self.stamina = max(0, self.stamina - 1)
                b.kill()
                # if self.health < 1:
                #     self.dying = True

    def shoot(self):
        if self.stamina < 1:
            self.shooting = False
            return None
        else:
            x, y, width, height = self.rect
            x += width / 2
            y += height/2
            ctrpt = x, y
            monsterBulletImg = pygame.Surface(
                (self.bulletData["radius"] * 2, self.bulletData["radius"] * 2),
                pygame.SRCALPHA)
            pygame.draw.ellipse(monsterBulletImg, (255, 255, 255),
                                [0, 0, self.bulletData["radius"] * 2,
                                 self.bulletData["radius"] * 2], 1)
            # bullet text
            font = pygame.font.Font(None, 3)
            text = font.render(random.choice(string.ascii_letters), True, color)
            self.bulletData["text"] = text
            # TODO fix this
            self.angle = (self.angle + self.angleIncrement) % 360
            self.bulletData["angle"] = self.angle
            bullets = []
            division =7
            for i in range(division):
                self.bulletData["angle"] += 360 // division
                bullets.append(MonsterBullet(ctrpt, monsterBulletImg, self.bulletData))
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

    def pattern(self):
        pass

    def update(self, scr_rect):
        self.deltaMoveX = self.vel * math.cos(math.radians(self.angle))
        self.deltaMoveY = self.vel * math.sin(math.radians(self.angle))
        self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
        if self.rect.bottom < 0 or self.rect.top > scr_rect.size[1] or self.rect.left  > scr_rect.size[0] or self.rect.right < 0:
            self.kill()

    def draw(self):
        pass