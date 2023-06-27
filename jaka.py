import jkrc
import time

ABS = 0
INCR = 1
IO_CABINET = 0
IO_TOOL = 1
IO_EXTEND = 2

def float_to_hex(f):
    import struct
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_dec(value):
    return int(value[0:6], 16)

def float_to_dec(value):
    hex = float_to_hex(value)
    return hex_to_dec(hex)

class Jaka:
    def __init__(self, ip="192.168.15.20"):
        self.result = False
        self.is_back = False
        self.jkrc_speed = 10
        self.ip = ip
        self.robot = jkrc.RC(self.ip)
        self.robot.login()
        print("Finished initializing robot")
        
    def init_robot(self):
        res = self.robot.get_robot_state()
        status = res[1]
        if status[0]:
            print("The robot was stopped immediately!")
            print("The emergency stop button was pressed!")
            return False
        if not status[1]:
            self.robot.power_on()
        if not status[2]:
            self.robot.enable_robot()
        return True

    def set_tool(self, tool_index):
        res = self.robot.set_tool_id(tool_index)
        if res[0] != 0:
            print("Failed to set robot tool!")
            print(res)
            return False
        while True:
            print("Changing tool...")
            res = self.robot.get_tool_id()
            if res[1] == tool_index:
                print(tool_index)
                break
        return True

    def stop_move(self):
        result = self.robot.motion_abort()
        if result[0] != 0:
            print("Failed to stop the robot!")
            print(result)
            return False
        print("Robot stopped")
        return True

    def is_stop_move(self):
        res = self.robot.is_in_pos()
        if res[0] != 0:
            print("Failed to check if the robot is stopped!")
            print(res)
            return False
        if res[0] == 0 and res[1]:
            return True
        else:
            return False

    def move_to_point(self, point, speed=50):
        print(point)
        result = self.robot.linear_move(end_pos=point, move_mode=ABS, is_block=False, speed=speed)
        if result[0] != 0:
            print("Failed to move to point!")
            print("JKRC.result: " + str(result))
        while True:
            print("Jaka is moving...")
            time.sleep(1)
            res = self.robot.is_in_pos()
            if res[0] != 0:
                print("Failed to check if the robot is stopped!")
                print(res)
                return res
            if res[0] == 0 and res[1]:
                break
        print("Jaka moved to point successfully")
        self.result = True
        return result

    def move_to_point_joint(self, point, speed=1):
        print(point)
        result = self.robot.joint_move(joint_pos=point, move_mode=ABS, is_block=False, speed=speed)
        while True:
            print("Jaka joint is moving...")
            time.sleep(1)
            res = self.robot.is_in_pos()
            if res[0] != 0:
                print("Failed to check if the robot is stopped!")
                print(res)
                return res
            if res[0] == 0 and res[1]:
                break
        print("Jaka joint move successful")
        return result

    def read_actual_tcp_point(self):
        ret = self.robot.get_tcp_position()
        if ret[0] == 0:
            actual_t = ret[1]
        else:
            print("Something happened. Error code: ", ret[0])
        return actual_t

    def set_digital(self, value):
        result = self.robot.set_digital_output(iotype=IO_TOOL, index=0, value=value)
        if result[0] != 0:
            print("Failed to control the I/O signal of the Jaka! -- ", value)
            print(result)

    def set_analog_output(self, index, value):
        value = float_to_dec(value)
        print(str(value))
        result = self.robot.set_analog_output(iotype=IO_EXTEND, index=index, value=value)
        if result[0] != 0:
            print("Failed to control the AO signal of the jaka! -- ", index, " -- ", value)
            print(result)

    def log_out(self):
        self.robot.logout()
