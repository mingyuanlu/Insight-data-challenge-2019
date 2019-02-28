#!/bin/python

import unittest
import sys
import os
from mymodule import *
import filecmp
import operator

class MyModuleTest(unittest.TestCase):
    """Test functions in mymodule."""

    def get_script_path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def setUp(self):
        """Define data used in test."""

        pwd = self.get_script_path()
        self.test_drug_info_file =  pwd+'/../insight_testsuite/tests/my_test/input/test_input_file.txt'
        self.test_raw_tuple= [('jordanmichael', 'A', 23.00),
                   ('jameslebron', 'C', 23.10),
                   ('bryantkobe', 'B', 8),
                   ('bryantkobe', 'C', 24.9)]
        self.test_sorted_tuple = sorted(self.test_raw_tuple, key=operator.itemgetter(1))
        #print self.test_sorted_tuple
        self.test_dict = {'C':2, 'A':1, 'B':1}
        self.test_num_unique_name = [1, 1, 2]
        self.test_total_cost_each_drug = [23.00,8.00,48.00]
        self.test_output_file = pwd+'/../insight_testsuite/tests/my_test/output/test_output_file_1.txt'


    def test_read_line(self):
        """Line is correctlt split and missing/corrupetd fields are checked."""

        expected_data = ['lu','ming-yuan','DRUG1',135.999,True,3]
        input_string = '001,LU,MING-YUAN,DRUG1,135.999\n'
        data = read_line(input_string)
        self.assertEqual(expected_data[0],data[0])
        self.assertEqual(expected_data[1],data[1])
        self.assertEqual(expected_data[2],data[2])
        self.assertAlmostEqual(expected_data[3],data[3])
        self.assertEqual(expected_data[4],data[4])
        self.assertAlmostEqual(expected_data[5],data[5])

        #Check for missing fields
        input_string = '001,,MING-YUAN,DRUG1,135\n'
        data = read_line(input_string)
        self.assertFalse(data[4])

        input_string = '001,LU,MING-YUAN,DRUG1,\n'
        data = read_line(input_string)
        self.assertFalse(data[4])

        #Check for corrupted fields
        input_string = '001x,LU,MING-YUAN,DRUG1,135\n'
        data = read_line(input_string)
        self.assertFalse(data[4])

        input_string = '001,LU,MING-YUAN,DRUG1,1ag5\n'
        data = read_line(input_string)
        self.assertFalse(data[4])

    def test_read_input_file(self):
        """Inpue file is correctly read and tuple constructed."""

        test_max_digit = 2
        tuple1 = self.test_raw_tuple
        tuple2, max_digit = read_input_file(self.test_drug_info_file)
        self.assertEqual(tuple1, tuple2)
        self.assertAlmostEqual(max_digit,test_max_digit)

    def test_get_unique_drug_list(self):
        """Unique drug list dict is correctly returned."""
        dict1 = self.test_dict
        dict2 = get_unique_drug_list(self.test_sorted_tuple)
        self.assertEqual(dict1, dict2)

    def test_get_num_unique_name(self):
        """Number of unique names for each drug is correcy."""

        list1 = self.test_num_unique_name
        list2 = get_num_unique_name(self.test_sorted_tuple, self.test_dict)
        self.assertEqual(list1, list2)

    def test_get_total_cost_each_drug(self):
        """Total cost of each drug is correct."""

        list1 = self.test_total_cost_each_drug
        list2 = get_total_cost_each_drug(self.test_sorted_tuple, self.test_dict)
        self.assertEqual(list1, list2)

    def test_print_drug_info(self):
        """The output file is as expected."""

        pwd = self.get_script_path()
        fout1 = self.test_output_file
        fout2 = pwd+'/../insight_testsuite/tests/my_test/output/test_output_file_2.txt'
        print_drug_info(self.test_sorted_tuple, self.test_dict, self.test_num_unique_name, self.test_total_cost_each_drug, fout2, 2)
        self.assertTrue(filecmp.cmp(fout1, fout2))



if __name__ == '__main__':
    unittest.main()
