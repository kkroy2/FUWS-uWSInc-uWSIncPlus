from Parameters.userDefined import UserDefined
from Parameters.Variable import Variable


class ThresholdCalculation():
    @staticmethod
    def get_minExpSup():
        return UserDefined.min_sup*Variable.size_of_dataset

    @staticmethod
    def get_semi_threshold():
        return ThresholdCalculation.get_minExpSup()*Variable.mu

    @staticmethod
    def get_local_threshold():
        return (UserDefined.min_sup*(Variable.window_size*Variable.size_of_increment + Variable.size_of_dataset)) / \
               (Variable.window_size*Variable.size_of_increment)

    @staticmethod
    def get_minExpWgtSup(self):
        return Variable.WAM * Variable.size_of_dataset * UserDefined.wgt_factor

    @staticmethod
    def update_dataset(sz):
        Variable.size_of_dataset += sz

    @staticmethod
    def get_wgt_exp_sup():
        return UserDefined.min_sup*Variable.size_of_dataset*UserDefined.wgt_factor*Variable.WAM

    @staticmethod
    def get_semi_wgt_exp_sup():
        return UserDefined.min_sup * Variable.size_of_dataset * UserDefined.wgt_factor\
               * Variable.WAM * Variable.mu
