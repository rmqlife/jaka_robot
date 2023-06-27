from HanglokLogger import HagLogger
from PyQt5.QtCore import *
import HanglokJKRC as jkrc
import os
start_point = [-243.02299499511716, -172.26100158691406, 516.3909912109374, -1.5707963000000003,
                                   0.78539815, 1.5707962999999998]


log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log")
logger = HagLogger(os.path.join(log_path, "Nucleic_Acid_Service.log"))
jkrc_object = jkrc.HagJkrc(logger, "192.168.15.200")
point = jkrc_object.read_actual_tcp_point_all()
print(point)
point[0] = point[0] + 1
print(point)
jkrc_object.move_to_point(start_point, 50)
point = jkrc_object.read_actual_tcp_point_all()
print(point)
