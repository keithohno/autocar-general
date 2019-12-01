import pidController
import Node
kP = 1.0
kI = 0.5
kD = 0.7
target = 0

controller = pidController.Controller(kP, kI, kD)

listener = Node.Node("linearNode.json")

while(True):
    position = listener.recv("pid_control_recv",)










