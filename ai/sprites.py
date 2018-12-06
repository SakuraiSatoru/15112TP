import bulletml
import neat
import pygame
import pygame.gfxdraw

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

        self.playerReprImgTrans.blit(self.playerReprImgLeft, (1, 0))
        self.playerReprImgTrans.blit(self.playerReprImgRight, (12, 0))
        self.image = self.playerReprImgTrans
        pygame.gfxdraw.filled_circle(self.playerReprImgTrans, 13, 16, 4,
                                     (255, 255, 255))

    def update(self, scr_size, center, trans=False):
        self.rect.center = center[0], center[1] - 4


class PlayerHitBox(Sprite):
    def __init__(self, centerPoint, image, data, genome,
                 config):
        print("init player!")
        Sprite.__init__(self, centerPoint, image)

        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.index = 0

        self.fitness = 0

        self.originCenter = centerPoint
        self.shooting = True
        self.shootable = True
        self.movable = True
        self.deltaMoveX = self.deltaMoveY = 0
        self.vel = data["velSlow"]
        self.radius = image.get_rect().size[0] // 2
        self.data = data
        self.bulletData = data["bulletData"]
        self.dead = False
        self.image = data["playerHitBoxImgTrans"]
        self.image.fill((255, 255, 255))
        self.transform = True
        self.target = self.rect.center

    # check 8 directions
    def checkDist(self, b):
        sqDist = (b.rect.x - self.rect.x) ** 2 + (b.rect.y - self.rect.y) ** 2
        if sqDist < 25:
            raise Exception
        if b.rect.y < self.rect.y and abs(b.rect.x - self.rect.x) < 8:
            return (0, sqDist)
        if self.rect.y > b.rect.y and self.rect.x > b.rect.x and abs(
                self.rect.y - b.rect.y - self.rect.x + b.rect.x) < 8:
            return (1, sqDist)
        if self.rect.x > b.rect.x and abs(self.rect.y - b.rect.y) < 8:
            return (2, sqDist)
        if self.rect.x > b.rect.x and self.rect.y < b.rect.y and abs(
                self.rect.x - b.rect.x - b.rect.y + self.rect.x) < 8:
            return (3, sqDist)
        if self.rect.y < b.rect.y and abs(self.rect.x - b.rect.x) < 8:
            return (4, sqDist)
        if self.rect.y < b.rect.y and self.rect.x < b.rect.x and abs(
                b.rect.y - self.rect.y - b.rect.x + self.rect.x) < 8:
            return (5, sqDist)
        if self.rect.x < b.rect.x and abs(self.rect.y - b.rect.y) < 8:
            return (6, sqDist)
        if self.rect.x < b.rect.x and self.rect.y > b.rect.y and abs(
                b.rect.x - self.rect.x - self.rect.y + b.rect.y) < 8:
            return (7, sqDist)
        return None

    # check kNN
    def checkKNN(self, bullets, k=5):
        print("checking...")
        dLst = [None] * k
        rLst = []
        for b in bullets:
            sqDist = (b.rect.x - self.rect.x) ** 2 + (
                    b.rect.y - self.rect.y) ** 2
            if sqDist < 25:
                raise Exception
            i = 0
            while i < k:
                if dLst[i] is not None and sqDist > self.sqDistCal(dLst[i][0],
                                                                   dLst[i][0],
                                                                   self.rect.x,
                                                                   self.rect.y):
                    i += 1
                else:
                    dLst.insert(i, (
                        b.rect.x - self.rect.x, b.rect.y - self.rect.y))
                    dLst.pop()
                    break
        for d in dLst:
            if d is not None:
                rLst.append(d[0] * 10000 // 480)
                rLst.append(d[1] * 10000 // 480)
        while len(rLst) < k * 2:
            rLst.append(0)
        print(rLst)
        return rLst

    def sqDistCal(self, x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def moveDecision(self, bullets, bossPos):
        # algorithm 1, set .\ai\config input to 9
        input = [10000] * 9
        for b in bullets:
            try:
                d = self.checkDist(b)
                if d is not None and input[d[0]] > d[1]:
                    input[d[0]] = d[1]
            except:
                self.dead = True
                self.kill()
        input[8] = (self.rect.y - bossPos[1]) * 10000 // 480
        # algorithm 1, set .\ai\config input to 9

        # algorithm 2, set .\ai\config input to 12
        # input = [10000] * 12
        # try:
        #     input = self.checkKNN(bullets)
        # except:
        #     print("dead")
        #     self.dead = True
        #     self.kill()
        #
        # if len(input) > 10:
        #     input = input[:10]
        # input.append((self.rect.x - bossPos[0]) * 10000 // 480)
        # input.append(abs(self.rect.x - 240) * 10000 // 480)
        # algorithm 2, set .\ai\config input to 12

        # Setup the input layer
        input = tuple(input)
        print(input)

        # Feed the neural network information
        output = self.neural_network.activate(input)
        # print("input:", input, "output:",output)

        # Obtain Prediction
        # output = (up,left,down.right)
        if output[0] > 0.5:
            self.deltaMoveY -= self.vel
        if output[1] > 0.5:
            self.deltaMoveX -= self.vel
        if output[2] > 0.5:
            self.deltaMoveY += self.vel
        if output[3] > 0.5:
            self.deltaMoveX += self.vel

    def update(self, scr_size, bullets, bossPos):
        if self.dead:
            return
        self.deltaMoveX = 0
        self.deltaMoveY = 0
        self.moveDecision(bullets, bossPos)
        self.fitness += len(bullets)
        if abs(self.rect.x - bossPos[0]) < 25:
            self.fitness += 5000

        self.movable = True

        if self.movable:
            self.rect.move_ip(self.deltaMoveX, self.deltaMoveY)
            self.rect.clamp_ip(scr_size)


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

        self.duration -= 50
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
        self.immutableDur = 2
        self.immutableCount = 0
        self.spellNum = data["spellNum"]
        self.currentSpellIndex = 0
        self.bulletMLInit()
        self.newPath = None
        self.pathInit(self.rect.centerx, self.rect.centery)
        # self.generator = self.getBulletChar()
        # indicator of new popUp
        self.newSpell = [False, ""]

    def update(self, monsterBulletGroup, hitBoxPos):
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
            if self.currentSpellIndex < 0:
                self.currentSpellIndex = 0
            self.immutable = False
            self.shooting = True
            self.newSpell = [True, self.getSpellName()]
            self.damage(0.4)

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
        self.bulletMLDoc = bulletml.BulletML.FromDocument(
            open(self.script, "rU"))
        self.bulletMLSource = bulletml.Bullet.FromDocument(self.bulletMLDoc,
                                                           x=self.rect.centerx,
                                                           y=self.rect.centery,
                                                           target=self.target,
                                                           rank=0.2)
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
        return MonsterBullet(ctrpt, monsterBulletImg, self.bulletData)

    def getSpellName(self):
        s = self.bulletData["pyScripts"][self.currentSpellIndex].split("(")[0][
            3:]
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

    def pattern(self):
        pass

    def update(self, scr_rect):
        if self.rect.bottom < 0 or self.rect.top > scr_rect.size[
            1] or self.rect.left > scr_rect.size[0] or self.rect.right < 0:
            self.kill()


class SideBar(Sprite):
    def __init__(self, centerPoint, image):
        Sprite.__init__(self, centerPoint, image)
        helper.filledRoundedRect(self.image, (
            8, 8, self.rect.width - 16, self.rect.height - 16),
                                 (255, 255, 255),
                                 0.2)
        helper.filledRoundedRect(self.image, (
            9, 9, self.rect.width - 18, self.rect.height - 18), (0, 0, 0), 0.2)
        self.originImg = self.image.copy()
        self.stage = 1

    def update(self, stage):
        self.stage = stage
        self.image = self.originImg.copy()
        font = pygame.font.Font(None, 25)
        text = font.render("Stage: %s" % self.stage, True, (255, 255, 255))
        self.image.blit(text, (25, 80))


class StaminaBar(Sprite):
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
