from controller import Robot

class myUR5(Robot):
    def __init__(self):
        super().__init__()
        # Get the robot's motors
        self.motors = [
            self.getDevice("shoulder_pan_joint"),
            self.getDevice("shoulder_lift_joint"),
            self.getDevice("elbow_joint"),
            self.getDevice("wrist_1_joint"),
            self.getDevice("wrist_2_joint"),
            self.getDevice("wrist_3_joint")
        ]

        # Get the position sensors for each joint
        self.position_sensors = [
            self.getDevice("shoulder_pan_joint_sensor"),
            self.getDevice("shoulder_lift_joint_sensor"),
            self.getDevice("elbow_joint_sensor"),
            self.getDevice("wrist_1_joint_sensor"),
            self.getDevice("wrist_2_joint_sensor"),
            self.getDevice("wrist_3_joint_sensor")
        ]

        # Enable the position sensors
        timestep = int(self.getBasicTimeStep())
        for sensor in self.position_sensors:
            sensor.enable(timestep)

    def set_pos(self, positions):
        # Set the position of each joint to the target position
        for i, pos in enumerate(positions):
            self.motors[i].setPosition(pos)
        # Step the simulation to apply the new positions
        self.step(int(self.getBasicTimeStep()))

    def get_pos(self):
        # Get the current position of each joint
        current_positions = [sensor.getValue() for sensor in self.position_sensors]
        return current_positions

if __name__ == "__main__":
    arm = myUR5()

    # Example usage with vector inputs
    a = 0
    direction = 1  # 1 for increasing, -1 for decreasing

    while True:
        a += 0.03 * direction
        if a >= 6.28:
            direction = -1
        elif a <= 0:
            direction = 1

        p = [0, -1.57, 1.57, 0.0, a, 0]
        arm.set_pos(p)
        print(a)

        # Get and print current joint positions inside the loop
        current_positions = arm.get_pos()
        print("Current Joint Positions:", current_positions)