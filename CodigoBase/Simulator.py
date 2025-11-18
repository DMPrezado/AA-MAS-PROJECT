import random
import time


# key class
class Key:
    def __init__(self, name, x, y, treasure=None):
        self.name = name
        self.treasure = treasure
        self.x = x
        self.y = y

# treasure class
class Treasure:
    opened = False
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
# ground class
class Ground:
    def __init__(self, x, y):
        self.name = "Ground"
        self.x = x
        self.y = y

#map class
class Map:

    def __init__(self):
        self.size = 5
        self.agentx = 0
        self.agenty = 0
        self.stop = False
        # define treasures and keys
        t1 = Treasure("T1", 3, 2)
        t2 = Treasure("T2", 2, 1)
        k1 = Key("K1", 0, 2)
        k2 = Key("K2", 4, 1)
        self.treasures = [t1, t2]
        self.keys = [k1, k2]


    def get_action(self):
        actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        (a,b) = random.choice(actions)
        newx = self.agentx + a
        newy = self.agenty + b
        while newx < 0 or newx >= self.size or newy >= self.size or newy < 0:
            (a,b) = random.choice(actions)
            newx = self.agentx + a
            newy = self.agenty + b

        return newx, newy

    def get_object_here(self, x, y):
        for treasure in self.treasures:
            treasure_pos = (treasure.x, treasure.y)
            if treasure_pos == (x,y):
                print("Found treasure")
                return treasure

        for key in self.keys:
            key_pos = (key.x, key.y)
            if key_pos == (x,y):
                print("Found key")
                return key

        return Ground(x, y)


    def render(self):
        for i in range(self.size):
            row = ""
            for j in range(self.size):

                keys_here = [w.name for w in self.keys if w.x == j and w.y == i]
                treasures_here = [w.name for w in self.treasures if w.x == j and w.y == i and w.opened == False]

                if self.agentx == j and self.agenty == i:
                    row += " AA "
                elif keys_here:
                    row += f" {keys_here[0]} "
                elif treasures_here:
                    row += f" {treasures_here[0]} "
                else:
                    row += " .. "
            print(row)

        print("\n")

        treasures_opened = [t for t in self.treasures if t.opened]
        if len(treasures_opened) == len(self.treasures):
            print("All treasures open! :D")
            self.stop = True


if __name__ == "__main__":

    map = Map()
    found_keys =[]

    while not map.stop:
        map.render()

        print("My keys: ")
        for key in found_keys:
            print(f" {key.name} opens: {key.treasure}")

        x, y = map.get_action()
        obj = map.get_object_here(x, y)
        if isinstance(obj,Ground):
            map.agentx = x
            map.agenty = y
        elif isinstance(obj,Key):

            # From here:
            if obj.name == "K1":
                obj.treasure = "T1"
            elif obj.name == "K2":
                obj.treasure = "T2"
            # to here, in the explorer agent main
            # you must change this code

            map.keys.remove(obj)
            found_keys.append(obj)
            map.agentx = x
            map.agenty = y

        elif isinstance(obj,Treasure):
            for key in found_keys:
                if key.treasure == obj.name:
                    obj.opened = True
                    map.treasures.remove(obj)
                    map.agentx = x
                    map.agenty = y

        time.sleep(0.5)

