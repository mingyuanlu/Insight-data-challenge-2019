#!/bin/python

import sys
import mymodule
import operator
from datetime import datetime

#arg 1: input file

if(len(sys.argv) != 3):
    print("Expected 2 argument (input file). Now have: %d") % (len(sys.argv))
    sys.exit(1)

start_time = datetime.now()

input_file = sys.argv[1]
output_file = sys.argv[2]

# A list of tuples. Columns: (full name, drug name, cost)
clean_table = mymodule.read_input_file(input_file)
#print clean_table

# sort by drug name in ascending order
clean_table.sort(key=operator.itemgetter(1))
#print clean_table

# dict {drug_name: count}
unique_drug_dict = mymodule.get_unique_drug_list(clean_table)
#print unique_drug_dict

# obtain list of unique names for each drug
num_unique_name_each_drug = mymodule.get_num_unique_name(clean_table, unique_drug_dict)

# obtain the total cost of each drug
total_cost_each_drug = mymodule.get_total_cost_each_drug(clean_table, unique_drug_dict)#, num_unique_name_each_drug)

mymodule.print_drug_info(clean_table, unique_drug_dict, num_unique_name_each_drug, total_cost_each_drug, output_file)

print datetime.now() - start_time
