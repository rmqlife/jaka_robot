import json
import logging
from HanglokJKRC import HagJkrc

class Arm:
    def __init__(self, config_file):
        self.logger = logging.getLogger("my_logger")
        self.logger.setLevel(logging.DEBUG)

        with open(config_file, 'r') as file:
            config = json.load(file)

        self.arm = HagJkrc(self.logger, config['ip'])
        self.arm.init_robot()

        self.pointset = config['pointset']

    def set_gripper(self, val):
        self.arm.set_set_analog_output(0, val)

    def grab_pen(self):
        pt = self.pointset['pen']
        print(pt)
        self.arm.move_to_point(pt, 50)
        self.set_gripper(20)
        pt[2] -= 40
        self.arm.move_to_point(pt, 30)
        self.set_gripper(5)

        pt[2] += 100
        self.arm.move_to_point(pt, 30)

    def move_to_point(self, point_name):
        pt = self.pointset.get(point_name)
        if pt:
            self.move_to_joint(pt)
        else:
            print(f"Point '{point_name}' not found in the pointset.")

    def set_coord(self, point_name, coordinates):
        self.pointset[point_name] = coordinates

    def move_to_coord(self, coord):
        current_pos = self.tcp_pos()
        new_pos = [coord[0], coord[1], coord[2], current_pos[3], current_pos[4], current_pos[5]]
        self.arm.move_to_point(new_pos, 50)

    def tcp_pos(self):
        return self.arm.read_actual_tcp_point_all()
    
    def joint_pos(self):
        return self.arm.read_actual_joint_point()
    
    def move_to_joint(self, joint):
        return self.arm.move_to_point_joint(joint, speed=0.2)
    
# Read the config file path
config_file = 'config-deputy.json'

# Create an instance of the Arm class
arm = Arm(config_file)

j = arm.joint_pos()
print(j)

arm.move_to_point('left')
# # arm.move_to_point('left')
arm.move_to_point('right')
arm.move_to_point('left_up')
arm.move_to_point('right_up')
