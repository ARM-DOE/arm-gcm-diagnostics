import unittest
import os
import cdms2
from arm_diags.src import seasonal_mean

def get_abs_file_path(relative_path):
    return os.path.dirname(os.path.abspath(__file__)) + '/' + relative_path

class TestARMDerivations(unittest.TestCase):

    def test_var_seasons_passes(self):
        test_file = cdms2.open(get_abs_file_path('test_vars.nc'))
        var = test_file('pr')
        test_file.close()
        seasons= ['ANN']
        seasonal_mean.var_seasons(var,seasons)
        
if __name__ == '__main__':
    unittest.main()

