import random
import time

# import game.map_data

skill_keys = ['z', 'x', 'x', 'v', 'a', 's', 'd', 'f', 'g', 'h', 'q', 'w', 'e', 'r']


class Skill:
    def __init__(self, map_data=None):
        self.map_data = map_data

    def pick_strings(self, keys: [], num_picks: int):
        picks = []
        while True:
            key = keys[random.randint(0, len(keys) - 1)]
            if key not in picks:
                picks.append(key)
            if len(picks) >= num_picks:
                break
        return picks

    def pick_key(self, num_picks: int = 5):
        keys = []
        for i in range(len(skill_keys)):
            keys.append(skill_keys[i])

        if self.map_data.is_boss_room():
            keys.append("t")
            keys.append("y")
        return self.pick_strings(keys, num_picks)


if __name__ == '__main__':
    while True:
        picks = Skill().pick_key()
        print(picks)
        time.sleep(1)