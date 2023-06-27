import jkrc
import struct
import time
import threading

#start_tcp = [-171.67300415039062, -603.9699707031249, 557.3790283203125, -1.5707963000000007, 0.7853981499999996, 3.1415926]
start_tcp = [-616.3250874654573, 20.105799276982772, 437.6865918435906, -1.5707968426730587, 0.7853980389479363, 1.5707960494302746]

# 绝对运动
ABS = 0
# 增量运动
INCR = 1
#控制柜面板IO
IO_CABINET =0
# 工具IO
IO_TOOL = 1
#扩展 IO
IO_EXTEND = 2

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_dec(value):
    return int(value[0:6], 16)

def float_to_dec(value):
    hex = float_to_hex(value)
    return hex_to_dec(hex)

class HagJkrc:
    def __init__(self, logger, ip="192.168.15.20"):
        self.log = logger
        self.start_tcp = start_tcp
        self.result = False
        self.is_back = False
        self.jkrc_speed = 10
        self.ip = ip
        self.robot = jkrc.RC(self.ip)
        self.robot.login()
        print("finish ini robot")
        # if self.init_robot():
        #     print("init jaka")
            # self.robot.set_tool_id(2) #NucleicAcid
            # time.sleep(2)
            # self.robot.set_tool_id(1) #RootCanal
            # t1 = threading.Thread(daemon=True, target=self.move_to_origin)
            # t1.start()
        return

    def init_robot(self):
        res = self.robot.get_robot_state()
        status = res[1]
        if status[0]:
            print("The robot was stopped immediately!")
            self.log.error("The emergency stop button was pressed!")
            return False
        if not status[1]:
            self.robot.power_on()
        if not status[2]:
            self.robot.enable_robot()
        return True

    def get_res(self):
        return self.result

    def set_res(self, res):
        self.result = res

    def get_is_back(self):
        return self.is_back

    def set_is_back(self, is_back):
        self.is_back = is_back

    def set_tool(self, tool_index):
        res = self.robot.set_tool_id(tool_index)
        if res[0] != 0:
            self.log.error("set robot tool failed!")
            print(res)
            return False
        while True:
            print("change tool...")
            res = self.robot.get_tool_id()
            if res[1] == tool_index:
                print(tool_index)
                break
        return True

    def stop_move(self):
        # 直接使用会导致视频卡顿，并且不能复位
        result = self.robot.motion_abort()
        if result[0] != 0:
            self.log.error("Stop the robot failed!")
            print(result)
            return False
        print("stop robot")
        return True

        # if self.stop_move_on == False:
        #     print("stop_move_on")
        #     self.stop_move_on = True
        #     result = self.robot.program_pause()
        #     if result[0] != 0:
        #         self.log.error("Stop the robot failed!")
        #         print(result)
        #         return False
        #     print("stop robot program")
        #     return True
        # else:
        #     result = self.robot.program_resume()
        #     print("move_on")
        #     self.stop_move_on = False
        #     if result[0] != 0:
        #         self.log.error("Stop the robot failed!")
        #         print(result)
        #         return False
        #     print("continue robot program")
        #     return True



    def is_stop_move(self):
        res = self.robot.is_in_pos()
        if res[0] != 0:
            self.log.error("search robot is stop failed!")
            print(res)
            return False
        if res[0] == 0 and res[1]:
            print(res)
            return True
        else:
            print(res)
            return False

    def move_to_point(self, point, speed=50):
        print(point)
        result = self.robot.linear_move(end_pos=point, move_mode=ABS, is_block=False, speed=speed)
        if result[0] != 0:
            self.log.error("move to point failed!")
            print("JKRC.result : " + str(result))
        #完成动作再跳出函数，即每个动作都等它完成
        while True:
            print("jaka is moving")
            time.sleep(1)
            res = self.robot.is_in_pos()
            if res[0] != 0:
                self.log.error("search robot is stop failed!")
                print(res)
                return res
            if res[0] == 0 and res[1]:
                break
        print("jaka move to point successfully")
        self.result = True
        return result

    def move_to_origin(self, speed=50):
        result = self.robot.linear_move(end_pos=self.start_tcp, move_mode=ABS, is_block=False, speed=speed)
        if result[0] != 0:
            self.log.error("move to origin failed!")
            print(result)
        time.sleep(2)
        print("jaka move to origin successful")
        # self.is_back = True
        return result

    def move_to_point_joint(self, point, speed=1):
        print(point)
        result = self.robot.joint_move(joint_pos=point, move_mode=ABS, is_block=False, speed=speed)#可以尝试改为阻塞
        # if result[0] != 0:
        #     self.log.error("move to point failed!")
        #     print(result)
        #完成动作再跳出函数，即每个动作都等它完成
        while True:
            print("jaka joint is moving")
            time.sleep(1)
            res = self.robot.is_in_pos()
            if res[0] != 0:
                self.log.error("search robot is stop failed!")
                print(res)
                return res
            if res[0] == 0 and res[1]:
                break
        print("jaka joint move successful")
        return result

    def read_actual_tcp_point(self):
        ret = self.robot.get_tcp_position()
        if ret[0] == 0:
            actual_t = ret[1]
        else:
            print("some things happend,the errcode is: ", ret[0])
        point = (actual_t[0], actual_t[1], actual_t[2])
        return point

    def read_actual_tcp_point_all(self):
        ret = self.robot.get_tcp_position()
        if ret[0] == 0:
            actual_t = ret[1]
        else:
            print("some things happend,the errcode is: ", ret[0])
        return actual_t

    def read_actual_joint_point(self):
        ret = self.robot.get_joint_position()
        if ret[0] == 0:
            joint = ret[1]
        else:
            print("some things happend,the errcode is: ", ret[0])
        return joint

    def set_digital(self, value):   #用于控制电信号输出（爪子等）
        result = self.robot.set_digital_output(iotype=IO_TOOL, index=0, value=value)
        if result[0] != 0:
            self.log.error("Failed to control the I/O signal of the jaka! -- ", value)
            print(result)

    def set_set_analog_output(self, index, value):
        value = float_to_dec(value)
        print(str(value))
        result = self.robot.set_analog_output(iotype=IO_EXTEND, index=index, value=value)
        if result[0] != 0:
            self.log.error("Failed to control the AO signal of the jaka! -- ", index, " -- ", value)
            print(result)

    def log_out(self):
        self.robot.logout()

    def get_roobot_digital_status(self):
        ret = self.robot.get_robot_status()
        if ret[0] == 0:
            return ret[1][14]

