import pygame

import fileIO


class Stage(object):
    def __init__(self, n):
        self.width = 40
        self.height = 40
        self.margin = 2
        self.n = n
        self.stageScripts = {}
        self.initImg()
        self.initFile()
        self.pathScript = r".\scripts\a.a"

        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-6, 6),
                                 "slowAngleList": (0, 0)}

    def initImg(self):
        self.monsterReprImg = pygame.Surface((self.width, self.height),
                                             pygame.SRCALPHA)
        self.monsterReprImg.fill((255, 255, 255))
        innerBox = pygame.Surface(
            (self.width - self.margin * 2, self.height - self.margin * 2),
            pygame.SRCALPHA)
        innerBox.fill((0, 0, 0))
        font = pygame.font.Font(None, 14)
        if self.n < 10:
            text = font.render("HW", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 3))
            font = pygame.font.Font(None, 35)
            text = font.render(str(self.n), True, (255, 255, 255))
            innerBox.blit(text, (
                self.width - self.margin * 9.5 - self.margin * 6 * (
                        len(str(self.n)) - 1), self.margin + 3))
            pygame.draw.line(innerBox, (255, 255, 255),
                             (self.margin + 1, self.height - 14),
                             (self.margin + 12, self.height - 14), 2)
        else:
            text = font.render("H", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 3))
            text = font.render("w", True, (255, 255, 255))
            innerBox.blit(text, (self.margin, self.margin * 2 + 10))
            font = pygame.font.Font(None, 35)
            text = font.render(str(self.n), True, (255, 255, 255))
            innerBox.blit(text, (
                self.width - self.margin * 15, self.margin + 3))
            pygame.draw.line(innerBox, (255, 255, 255),
                             (self.margin + 1, self.height - 14),
                             (self.margin + 6, self.height - 14), 2)
        self.monsterReprImg.blit(innerBox, (self.margin, self.margin))

    def initFile(self):
        dataloaded = True
        dict = {}
        try:
            dict = fileIO.read(r".\data\default.dat")
        except:
            try:
                dict = fileIO.read(r".\data\user.dat")
            except:
                dataloaded = False
        if len(dict) == 10 and dataloaded:
            pass
        else:
            raise RuntimeError;
        self.stageScripts = dict


# 1
# 	scripts
# 		['def getCubicCoeffs(k, root1, root2, root3): # Given roots e,f,g and..
# 	no
# 		1
# 	name
# 		hw1
class Stage1(Stage):
    def __init__(self):
        Stage.__init__(self, 1)
        monsterBulletScripts = ["scripts/1_1.xml", "scripts/1_2.xml",
                                "scripts/1_3.xml", "scripts/1_4.xml", ]
        pyScripts = self.stageScripts["1"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 700, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Data and Expressions, Functions, Conditionals",
                            "stageName": self.stageScripts["1"]["name"],
                            "path": "scripts/1_0.xml"}


class Stage2(Stage):
    def __init__(self):
        Stage.__init__(self, 2)
        monsterBulletScripts = ["scripts/2_1.xml", "scripts/2_2.xml",
                                "scripts/2_3.xml", "scripts/2_4.xml", ]
        pyScripts = self.stageScripts["2"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 900, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Loops, Debugging, Testing and Exceptions",
                            "stageName": self.stageScripts["2"]["name"],
                            "path": "scripts/2_0.xml"}


class Stage3(Stage):
    def __init__(self):
        Stage.__init__(self, 3)
        monsterBulletScripts = ["scripts/3_1.xml", "scripts/3_2.xml",
                                "scripts/3_3.xml", "scripts/3_4.xml", ]
        pyScripts = self.stageScripts["3"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1100, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Strings, Algorithmic Thinking, Style",
                            "stageName": self.stageScripts["3"]["name"],
                            "path": "scripts/3_0.xml"}


class Stage4(Stage):
    def __init__(self):
        Stage.__init__(self, 4)
        monsterBulletScripts = ["scripts/4_1.xml", "scripts/4_2.xml",
                                "scripts/4_3.xml", "scripts/4_4.xml", ]
        pyScripts = self.stageScripts["4"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1200, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "1D List and Tuples, Graphics",
                            "stageName": self.stageScripts["4"]["name"],
                            "path": "scripts/4_0.xml"}


class Stage5(Stage):
    def __init__(self):
        Stage.__init__(self, 5)
        monsterBulletScripts = ["scripts/5_1.xml", "scripts/5_2.xml",
                                "scripts/5_3.xml", "scripts/5_4.xml", ]
        pyScripts = self.stageScripts["5"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1300, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "2D Lists, Event-Based Animation",
                            "stageName": self.stageScripts["5"]["name"],
                            "path": "scripts/5_0.xml"}


class Stage6(Stage):
    def __init__(self):
        Stage.__init__(self, 6)
        monsterBulletScripts = ["scripts/6_1.xml", "scripts/6_2.xml",
                                "scripts/6_3.xml", "scripts/6_4.xml", ]
        pyScripts = self.stageScripts["6"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1400, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Time-Based Animation",
                            "stageName":
                                self.stageScripts["6"]["name"],
                            "path": "scripts/6_0.xml"}


class Stage7(Stage):
    def __init__(self):
        Stage.__init__(self, 8)
        monsterBulletScripts = ["scripts/7_1.xml", "scripts/7_2.xml",
                                "scripts/7_3.xml", "scripts/7_4.xml", ]
        pyScripts = self.stageScripts["8"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Sets, Dictionaties, Efficiency",
                            "stageName": self.stageScripts["8"]["name"],
                            "path": "scripts/7_0.xml"}


class Stage8(Stage):
    def __init__(self):
        Stage.__init__(self, 9)
        monsterBulletScripts = ["scripts/8_1.xml", "scripts/8_2.xml",
                                "scripts/8_3.xml", "scripts/8_4.xml", ]
        pyScripts = self.stageScripts["9"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1600, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Object-Oriented Programming, Recursion",
                            "stageName": self.stageScripts["9"]["name"],
                            "path": "scripts/8_0.xml"}


class Stage9(Stage):
    def __init__(self):
        Stage.__init__(self, 10)
        monsterBulletScripts = ["scripts/9_1.xml", "scripts/9_2.xml",
                                "scripts/9_3.xml", "scripts/9_4.xml", ]
        pyScripts = self.stageScripts["10"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1700, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Recursion",
                            "stageName": self.stageScripts["10"]["name"],
                            "path": "scripts/9_0.xml"}


class Stage10(Stage):
    def __init__(self):
        Stage.__init__(self, 11)
        monsterBulletScripts = ["scripts/10_1.xml", "scripts/10_2.xml",
                                "scripts/10_3.xml", "scripts/10_4.xml", ]
        pyScripts = self.stageScripts["11"]["scripts"]
        monsterBulletData = {"radius": 4, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 1800, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "OOPy Animation",
                            "stageName": self.stageScripts["11"]["name"],
                            "path": "scripts/10_0.xml"}
