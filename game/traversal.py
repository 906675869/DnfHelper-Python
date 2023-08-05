import _thread
import random
import time

# import keyboard
from pynput.keyboard import Key

from common import config, helper
from common import logger
from game import call, init, address
from game import skill


# from pynput import Key


class Screen:

    def __init__(self, mem):
        self.thread = None
        self._switch = False
        self.mem = mem
        self.hook_harm_switch = False
        self.hook_harm_origin_bytes = None

    def screen_switch(self):
        self._switch = not self._switch
        if self._switch:
            self.thread = _thread.start_new_thread(self.screen_thread, ())
            logger.info("技能全屏 [ √ ]", 1)
        else:
            self._switch = False
            logger.info("技能全屏 [ x ]", 1)

    def screen_thread(self):
        while self._switch:
            try:
                code_config = list(map(int, config().get("自动配置", "全屏配置").split(",")))
                if len(code_config) != 5:
                    logger.info("全屏配置错误", 2)
                    break
                rate = code_config[0]
                time.sleep(rate / 1000)
                self.full_screen(code_config)
            except Exception as e:
                print(e)

    @classmethod
    def screen_kill(cls):
        """秒杀完毕"""
        call.skill_call(0, 54141, 0, 0, 0, 0, 1.0)
        logger.info("秒杀完毕 [ √ ]", 1)

    def full_screen(self, code_config):
        """全屏遍历"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        num = 0
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            if obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_code > 0 and obj_blood > 0 and obj_ptr != rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        code = int(code_config[1])
                        harm = int(code_config[2])
                        size = float(code_config[3])
                        call.skill_call(rw_addr, code, harm, monster.x, monster.y, 0, size)
                        num = num + 1
                        if num >= code_config[4]:
                            break

    def follow_monster(self):
        """跟随怪物"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            if obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                    obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_ptr != rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        if obj_blood > 0:
                            rw_coordinate = map_obj.read_coordinate(rw_addr)
                            if abs(rw_coordinate.x - monster.x) > 60:
                                # call.drift_call(rw_addr, monster.x, monster.y, 0, 2)
                                self.go_dest(monster.x, monster.y)
                            # time.sleep(0.2)
                            if config().getint("自动配置", "跟随打怪") == 2:
                                title = helper.get_process_name()
                                if title == "地下城与勇士：创新世纪":
                                    keys = skill.pick_key()
                                    helper.key_press(keys, 0.03)
                                    # call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)
                            if config().getint("自动配置", "跟随打怪") == 3:
                                call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)
                            break

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)

    def hook_harm(self):
        self.hook_harm_switch = not self.hook_harm_switch
        if self.hook_harm_switch:
            random_harm = random.randint(2000000, 3999999)
            self.hook_harm_origin_bytes = self.mem.read_bytes(address.QjAddr, 10)
            self.mem.write_bytes(address.QjAddr, helper.add_list([72, 190], helper.int_to_bytes(random_harm, 8)))
            logger.info("hook伤害 [ √ ]", 1)
        else:
            if len(self.hook_harm_origin_bytes) > 0:
                self.mem.write_bytes(address.QjAddr, self.hook_harm_origin_bytes)
            logger.info("hook伤害 [ x ]", 1)

    def float_harm(self, x: int):
        if x == 0:
            x = 20
        rd_addr = call.person_ptr()
        self.mem.write_int(rd_addr + address.FdbgAddr, x)
        logger.info("浮点伤害 [ x ]", 1)

    def go_dest(self, x: int, y: int):
        # mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return
        rd_addr = call.person_ptr()
        left = False
        right = False
        up = False
        down = False
        cnt = 0
        while True:
            cnt = cnt + 1
            if cnt > 100:  ## 6s
                helper.release(Key.left)
                helper.release(Key.right)
                helper.release(Key.up)
                helper.release(Key.down)
                break
            rw_coordinate = map_obj.read_coordinate(rd_addr)
            if x - 30 < rw_coordinate.x < x + 30 and y - 30 < rw_coordinate.y < y + 30:
                helper.release(Key.left)
                helper.release(Key.right)
                helper.release(Key.up)
                helper.release(Key.down)
                break
            if x - 30 < rw_coordinate.x < x + 30:
                helper.release(Key.left)
                helper.release(Key.right)
                left = False
                right = False
            if y - 30 < rw_coordinate.y < y + 30:
                helper.release(Key.up)
                helper.release(Key.down)
                up = False
                down = False
            if rw_coordinate.x > x + 30:
                if right:
                    helper.release(Key.right)
                    right = False
                helper.key_press_release(Key.left)
                time.sleep(0.01)
                helper.key_press_release(Key.left)
                time.sleep(0.02)
                helper.press(Key.left)
                time.sleep((rw_coordinate.x - x) / 1163)
                left = True
            if rw_coordinate.x < x - 30:
                if left:
                    helper.release(Key.left)
                    left = False
                helper.key_press_release(Key.right)
                time.sleep(0.01)
                helper.key_press_release(Key.right)
                time.sleep(0.01)
                helper.press(Key.right)
                time.sleep((x - rw_coordinate.x) / 1163)
                right = True
            if rw_coordinate.y > y + 30:
                if down:
                    helper.release(Key.down)
                    down = False
                helper.press(Key.up)
                up = True
            if rw_coordinate.y < y - 30:
                if up:
                    helper.release(Key.up)
                    up = False
                helper.press(Key.down)
            time.sleep(0.03)
