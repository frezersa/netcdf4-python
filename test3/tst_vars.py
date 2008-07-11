import sys
import unittest
import os
import tempfile
import numpy as NP
from numpy.random.mtrand import uniform 
from numpy.testing import assert_array_equal, assert_array_almost_equal
import netCDF3

# test variable creation.

FILE_NAME = tempfile.mktemp(".nc")
VAR_DOUBLE_NAME="dummy_var"
VAR_SHORT_NAME='dummy_var_short'
VARNAMES = [VAR_DOUBLE_NAME,VAR_SHORT_NAME]
VARNAMES.sort()
DIM1_NAME="x"
DIM1_LEN=2
DIM2_NAME="y"
DIM2_LEN=3
DIM3_NAME="z"
DIM3_LEN=25

randomdata = uniform(size=(DIM1_LEN,DIM2_LEN,DIM3_LEN))

class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        self.file = FILE_NAME
        f  = netCDF3.Dataset(self.file, 'w')
        f.createDimension(DIM1_NAME, DIM1_LEN)
        f.createDimension(DIM2_NAME, DIM2_LEN)
        f.createDimension(DIM3_NAME, DIM3_LEN)
        v1 = f.createVariable(VAR_DOUBLE_NAME, 'f8',(DIM1_NAME,DIM2_NAME,DIM3_NAME))
        v2 = f.createVariable(VAR_SHORT_NAME, 'i2',(DIM2_NAME,DIM3_NAME))
        v1.long_name = 'dummy data root'
        v1[:] = randomdata
        f.close()

    def tearDown(self):
        # Remove the temporary files
        os.remove(self.file)

    def runTest(self):
        """testing primitive variables"""
        f  = netCDF3.Dataset(self.file, 'r')
        # check variables in root group.
        varnames = f.variables.keys()
        varnames.sort()
        v1 = f.variables[VAR_DOUBLE_NAME]
        v2 = f.variables[VAR_SHORT_NAME]
        assert varnames == VARNAMES
        assert v1.dtype.str[1:] == 'f8'
        assert v2.dtype.str[1:] == 'i2'
        assert v1.long_name == 'dummy data root'
        assert v1.dimensions == (DIM1_NAME,DIM2_NAME,DIM3_NAME)
        assert v2.dimensions == (DIM2_NAME,DIM3_NAME)
        assert v1.shape == (DIM1_LEN,DIM2_LEN,DIM3_LEN)
        assert v2.shape == (DIM2_LEN,DIM3_LEN)
        #assert NP.allclose(v1[:],randomdata)
        assert_array_almost_equal(v1[:],randomdata)
        f.close()

if __name__ == '__main__':
    unittest.main()