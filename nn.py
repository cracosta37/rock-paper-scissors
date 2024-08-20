import numpy as np
import pandas as pd
import tensorflow as tf

import constants as c

data_from_record122 = pd.read_csv('Data/rps-record122.csv')
data_from_record_dtclf = pd.read_csv('Data/rps-record_dtclf')

num_rounds = 0

lables = np.empty((num_rounds, c.NUMBER_OF_INPUTS ))


