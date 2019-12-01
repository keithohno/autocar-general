import numpy as np

class Controller:
    """This class will represent a PID controller that will used to create instances
    of both a linear and angular PID controller for the car.
    To create instances of the controller pass the constructor initial Proportional,
    Integral, and Derivative values then set a target and a position and run the
    totalError() function to return an adjustment between -1.0 and 1.0 to send to the
    servo/motors
     """
    #Fields to hold PID values and error values
    kP = 0.0
    kI = 0.0
    kD = 0.0
    position = 0
    target = 0
    error = 0.0
    p_error = 0.0
    i_error = 0.0
    d_error = 0.0

    #

    def __init__(self, kP, kD, kI):
        self.kP = kP
        self.kI = kI
        self.kD = kD
    def setParameters(self, position, target):
        """Sets the parameters used to calculate the error. The first parameter is
        the current position of the car, and the second parameter is the target position
        for the car. """
        self.position = position
        self.target = target
    # Takes an array of kValues to set [kP, kI, KD]
    def setKValues(self, kValues):
        """This method is to adjust the kValues of the PID controller. The parameter kValues
         should be an array of 3 values for Proportional, Integral, and Derivative terms respectively"""
        self.kP = kValues[0]
        self.kI = kValues[1]
        self.kD = kValues[2]
	#TODO: I think the math here may be wrong, going to work on it. Will also need to finish documentation when I do. 
    def calculateError(self):
        """This method is to calculate the error of the car from the planned path,  """
        self.error = self.target - self.position
        self.p_error = self.error
        self.i_error += self.error
        self.d_error = self.error - self.p_error
    def totalError(self):
        self.calculateError(self.error)
        adjust = (-self.kP * self.p_error - (self.kI * self.i_error) - (self.kD * self.d_error))
        if adjust > 1.0:
            return 1.0
        elif adjust < -1.0:
            return -1.0
        else:
            return adjust
    #TODO: Decide if I want this here or as its own class 
    #      somewhere else.
    # def twiddleOptimization(self, tol = 0.2):
    #    # Initialization paramater vector
    #     p = [0,0,0]
    #    # Defines potential changes
    #     dp = [1,1,1]
    #     #Calculates the error of PID function
    #     best_error = self.totalError()
    #     threshold = 0.001
    #
    #     while sum(dp) > threshold:
    #         for i in range(len(p)):
    #             p[i] += dp[i]
    #             self.setKValues(p)
    #             new_error = self.totalError()
    #
    #             if new_error < best_error: # There was improvement
    #                 dp[i] *= 1.1
    #             else: # There was no improvement
    #                 p[i] -= 2*dp[i]
    #                 new_error = self.totalError()
    #
    #                 if new_error < best_error:# There was improvement this time
    #                     best_error = new_error
    #                     dp[i] *= 1.05
    #                 else: #There was no improvement
    #                     p[i] += dp[i]
    #                     # Due to there not being improvement in either direction,
    #                     # step size may just be too big
    #                     dp[i] *= 0.95
    #
    #     # Return optimized parameters
    #     return p











