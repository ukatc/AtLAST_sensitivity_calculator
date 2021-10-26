import numpy as np

class Efficiencies:
    '''
    All of the efficiency factors need to come in here...
    '''
    def __init__(self, eta1, eta2, eta3):
        '''
        At present, a placeholder method just to hold some efficiencies.
        :param eta1: efficiency 1
        :type eta1: float
        etc.
        '''
        self.eta1 = eta1
        self.eta2 = eta2
        self.eta3 = eta3

    def eta_a(self):
        '''
        Return the dish efficiency eta_a that needs to go into the SEFD calculation
        '''
        return self.eta1 * self.eta2 * self.eta3