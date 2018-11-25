class Stage1(object):
    def __init__(self):
        # self.monsterSpawns = 2
        monsterBulletData = {"radius": 10, "color": (255, 255, 255),"vel": 8,"fireRate": 5}
        self.monsterData = {"stamina": 100, "moveFunc": None,
                            "bulletData": monsterBulletData}
