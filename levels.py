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
            print("successfully loaded python scripts")
        else:
            raise RuntimeError;
        self.stageScripts = dict


# TODO implement spell names in the dict
# 1
# 	scripts
# 		['def getCubicCoeffs(k, root1, root2, root3): # Given roots e,f,g and vertical scale k, we can find # the coefficients a,b,c,d as such: # k(x-e)(x-f)(x-g) = # k(x-e)(x^2 - (f+g)x + fg) # kx^3 - k(e+f+g)x^2 + k(ef+fg+eg)x - kefg e,f,g = root1, root2, root3 return k, -k*(e+f+g), k*(e*f+f*g+e*g), -k*e*f*g', 'def playGuessingGame(): print("Let\'s play a guessing game! Think of a type of pet.") if input("Does it have fur?") == "Yes": if input("Can you teach it to play fetch?") == "Yes": print("It\'s a dog!") else: print("It\'s a cat!") else: if input("Can it swim?") == "Yes": print("It\'s a fish!") else: print("It\'s a bird!") return #### the following four functions go together ####', 'def threeLinesArea(m1, b1, m2, b2, m3, b3): if(m1-m2)*(m2-m3)*(m3-m1)==0: return 0 else: x1 = lineIntersection(m1,b1,m2,b2) y1 = m1*x1+b1 x2 = lineIntersection(m3,b3,m2,b2) y2 = m2*x2+b2 x3 = lineIntersection(m1,b1,m3,b3) y3 = m3*x3+b3 d1 = distance(x1,y1,x2,y2) d2 = distance(x2,y2,x3,y3) d3 = distance(x1,y1,x3,y3) return triangleArea(d1,d2,d3) #### the following two functions go together ####', 'def bonusFindIntRootsOfCubic(a, b, c, d): p = -b/(3*a) q = p**3 + (b*c-3*a*d)/(6*a**2) r = c/(3*a) x = (q+(q*q+(r-p*p)**3)**0.5)**(1/3)+(q-(q*q+(r-p*p)**3)**0.5)**(1/3)+p x = round(complex(x).real) p1 = (-b-x*a)/(2*a) p2 = complex((b*b-4*a*c-2*a*b*x-3*a*a*x*x)**0.5/(2*a)).real y = round(p1+p2) z = round(p1-p2) x1 = min(x,y,z) x3 = max(x,y,z) x2 = x+y+z-x1-x3 return x1,x2,x3 ################################################# # Hw1 Test Functions # ignore_rest #################################################', 'def colorBlender(rgb1, rgb2, midpoints, n): if n==0: return rgb1 if n == midpoints + 1: return rgb2 if n < 0 or n > midpoints+1: return None r1 = rgb1//1000000 g1 = rgb1//1000%1000 b1 = rgb1%1000 r2 = rgb2//1000000 g2 = rgb2//1000%1000 b2 = rgb2%1000 p1 = (r2-r1)/(midpoints+1)*n+r1 p2 = (g2-g1)/(midpoints+1)*n+g1 p3 = (b2-b1)/(midpoints+1)*n+b1 if p1*10%10 == 5: p1 = int(p1) + 1 else: p1 = round(p1) if p2*10%10 == 5: p2 = int(p2) + 1 else: p2 = round(p2) if p3*10%10 == 5: p3 = int(p3) + 1 else: p3 = round(p3) return p1*1000000+p2*1000+p3 #### bonusFindIntRootsOfCubic is a bonus problem, and therefore optional ####']
# 	no
# 		1
# 	name
# 		hw1
class Stage1(Stage):
    def __init__(self):
        Stage.__init__(self, 1)
        monsterBulletScripts = ["scripts/1_1.xml", "scripts/1_2.xml",
                                "scripts/1_3.xml", "scripts/1_4.xml",]
        pyScripts = self.stageScripts["1"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 300, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Data and Expressions, Functions, Conditionals",
                            "stageName": self.stageScripts["1"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-6, 6),
                                 "slowAngleList": (0, 0)}


class Stage2(Stage):
    def __init__(self):
        Stage.__init__(self, 2)
        monsterBulletScripts = ["scripts/2_1.xml", "scripts/2_2.xml",
                                "scripts/2_3.xml", "scripts/2_4.xml",]
        pyScripts = self.stageScripts["2"]["scripts"]
        print(self.stageScripts)
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 400, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Loops, Debugging, Testing and Exceptions",
                            "stageName": self.stageScripts["2"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-6, 0, 6),
                                 "slowAngleList": (0, 0)}


class Stage3(Stage):
    def __init__(self):
        Stage.__init__(self, 3)
        monsterBulletScripts = ["scripts/3_1.xml", "scripts/3_2.xml",
                                "scripts/3_3.xml", "scripts/3_4.xml",]
        pyScripts = self.stageScripts["3"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Strings, Algorithmic Thinking, Style",
                            "stageName": self.stageScripts["3"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage4(Stage):
    def __init__(self):
        Stage.__init__(self, 4)
        monsterBulletScripts = ["scripts/4_1.xml", "scripts/4_2.xml",
                                "scripts/4_3.xml", "scripts/4_4.xml", ]
        pyScripts = self.stageScripts["4"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "1D List and Tuples, Graphics",
                            "stageName": self.stageScripts["4"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage5(Stage):
    def __init__(self):
        Stage.__init__(self, 5)
        monsterBulletScripts = ["scripts/5_1.xml", "scripts/5_2.xml",
                                "scripts/5_3.xml", "scripts/5_4.xml",]
        pyScripts = self.stageScripts["5"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "2D Lists, Event-Based Animation",
                            "stageName": self.stageScripts["5"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage6(Stage):
    def __init__(self):
        Stage.__init__(self, 6)
        monsterBulletScripts = ["scripts/6_1.xml", "scripts/6_2.xml",
                                "scripts/6_3.xml", "scripts/6_4.xml",]
        pyScripts = self.stageScripts["6"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Time-Based Animation",
                            "stageName":
                                self.stageScripts["6"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage7(Stage):
    def __init__(self):
        Stage.__init__(self, 8)
        monsterBulletScripts = ["scripts/7_1.xml", "scripts/7_2.xml",
                                "scripts/7_3.xml", "scripts/7_4.xml",]
        pyScripts = self.stageScripts["8"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Sets, Dictionaties, Efficiency",
                            "stageName": self.stageScripts["8"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage8(Stage):
    def __init__(self):
        Stage.__init__(self, 9)
        monsterBulletScripts = ["scripts/8_1.xml", "scripts/8_2.xml",
                                "scripts/8_3.xml", "scripts/8_4.xml",]
        pyScripts = self.stageScripts["9"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Object-Oriented Programming, Recursion",
                            "stageName": self.stageScripts["9"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage9(Stage):
    def __init__(self):
        Stage.__init__(self, 10)
        monsterBulletScripts = ["scripts/9_1.xml", "scripts/9_2.xml",
                                "scripts/9_3.xml", "scripts/9_4.xml",]
        pyScripts = self.stageScripts["10"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "Recursion",
                            "stageName": self.stageScripts["10"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}


class Stage10(Stage):
    def __init__(self):
        Stage.__init__(self, 11)
        monsterBulletScripts = ["scripts/10_1.xml", "scripts/10_2.xml",
                                "scripts/10_3.xml", "scripts/10_4.xml",]
        pyScripts = self.stageScripts["11"]["scripts"]
        monsterBulletData = {"radius": 8, "color": (255, 255, 255), "vel": 5,
                             "fireRate": 50, "fontSize": 16,
                             "scripts": monsterBulletScripts,
                             "pyScripts": pyScripts}
        self.monsterData = {"stamina": 500, "spellNum": 4,
                            "bulletData": monsterBulletData,
                            "stageDescript": "OOPy Animation",
                            "stageName": self.stageScripts["11"]["name"],
                            "path": "scripts/1_0.xml"}
        self.playerBulletData = {"fireRate": 1, "fastAngleList": (-10, 0, 10),
                                 "slowAngleList": (0, 0, 0)}
