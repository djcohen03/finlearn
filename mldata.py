import time
import random
import numpy as np
from fincore.format import FeatureData
from sklearn.model_selection import train_test_split
from joblib import dump, load

class MLData(object):
    ''' A Class for Loading, Caching, Formatting, and Managing the Feature data
        used in the Machine Learning Algorithms

        # Example:
        spydata = MLData('SPY')
        model.fit(spydata.x_train, spydata.y_train)
        model.score(spydata.x_test, spydata.y_test)

    '''

    def __init__(self, symbol, getvix=False, simsize=1440):
        ''' Initialize and immediately load the feature data into memory
        '''
        self.symbol = symbol
        self.getvix = getvix
        self.simsize = simsize
        self.refresh()

    def reshape(self, cutoff=0.5):
        ''' Rejoin the training and simulation data, and reshape the distribution
            of training/dimulating data based on the given cutoff proportion
        '''
        # Compute new simsize based on cutoff value:
        count, _ = self.allinputs.shape
        self.simsize = int(count * cutoff)
        # Reshape the data based on the new self.simsize value:
        self._shape()

    def shuffle(self, test_size=0.25):
        ''' Shuffle and split training/testing data
        '''
        state = random.randint(1, 10000)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.inputs, self.outputs, random_state=state)

        print 'Shuffled: %s Train Vectors, %s Test Vectors' % (self.x_train.shape[0], self.x_test.shape[0])

    def refresh(self):
        ''' Reload the Feature data for the given symbol directly from the database
        '''
        self.featuredata = FeatureData(self.symbol, getvix=self.getvix)
        self.allinputs, self.alloutputs, self.features = self.featuredata.format()
        self._shape()

    def _shape(self):
        ''' Shape the data into four parts:
                - Train/Test Inputs
                - Train/Test Outputs
                - Simulation Inputs
                - Simulation Outputs
            Simulation outputs are meant to be used exclusively in the class
            method Simulate.run (see simulate.py).  This method takes a trained
            ML model with attribute 'mldata' (which is an instance of this MLData
            class), and uses the mldata.siminputs and mldata.simoutputs values to
            run a model simluation.

        '''
        # Resplit the data based on the value of self.simsize:
        self.siminputs = self.allinputs[-self.simsize:]
        self.simoutputs = self.alloutputs[-self.simsize:]
        self.inputs = self.allinputs[:-self.simsize]
        self.outputs = self.alloutputs[:-self.simsize]
        print 'Shaped ML Data (Train: %s; Simulation: %s)' % (self.inputs.shape[0], self.siminputs.shape[0])

        # Reshuffle the data to make sure training/testing vectors are only
        # drawing from the proper input/output train/test vectors
        self.shuffle()



if __name__ == '__main__':
    pass
