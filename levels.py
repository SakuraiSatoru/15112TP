import pygame


class Stage(object):
    def __init__(self, n):
        self.width = 40
        self.height = 40
        self.margin = 2
        self.monsterReprImg = pygame.Surface((self.width, self.height),
                                             pygame.SRCALPHA)
        self.monsterReprImg.fill((255, 255, 255))
        innerBox = pygame.Surface(
            (self.width - self.margin * 2, self.height - self.margin * 2),
            pygame.SRCALPHA)
        innerBox.fill((0, 0, 0))
        font = pygame.font.Font(None, 14)
        if n < 10:
            text = font.render("HW", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 3))
            font = pygame.font.Font(None, 35)
            text = font.render(str(n), True, (255, 255, 255))
            innerBox.blit(text, (
                self.width - self.margin * 9.5 - self.margin * 6 * (
                        len(str(n)) - 1), self.margin + 3))
            pygame.draw.line(innerBox, (255, 255, 255),
                             (self.margin + 1, self.height - 14),
                             (self.margin + 12, self.height - 14), 2)
        else:
            text = font.render("H", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 3))
            text = font.render("w", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 10))
            font = pygame.font.Font(None, 35)
            text = font.render(str(n), True, (255, 255, 255))
            innerBox.blit(text, (
                self.width - self.margin * 15, self.margin + 3))
            pygame.draw.line(innerBox, (255, 255, 255),
                             (self.margin + 1, self.height - 14),
                             (self.margin + 6, self.height - 14), 2)
        self.monsterReprImg.blit(innerBox, (self.margin, self.margin))


class Stage1(Stage):
    def __init__(self):
        Stage.__init__(self, 1)
        # self.monsterSpawns = 2
        monsterSpellScripts = ["scripts/1_1.xml"]
        monsterBulletData = {"radius": 10, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 15,
                             "scripts": monsterSpellScripts}
        self.monsterData = {"stamina": 300, "moveFunc": None,
                            "bulletData": monsterBulletData, "name": "I",
                            "stageName": "Data and Expressions\nFunctions\nConditionals"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 10),
                                 "slowAngleList": (0, 0)}
