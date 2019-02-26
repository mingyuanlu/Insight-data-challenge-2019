"""Define functions for data ETL and I/O."""
import sys
import numpy as np
import operator

'''
def is_all_alphabets(data):
    """Check that data composes of entirely alphabets, as a requirement for names."""

    good_line = True
    try:
        if not data.isalpha():
            raise ValueError("Not alphabets")
    except ValueError:
        print("%s is not entirely alphabets! This row will be skipped.")
        good_line = False

    return good_line
'''

def read_line(row):
    """Read line from input file."""

    good_line = True #If true, this line contains valid data. Else, the line is skipped
    data = row.rstrip().split(',')

    # Check for missing fields. If any field is missing, the row is skipped
    if "" in data:
        good_line = False

    try:
        val = int(data[0])
    except ValueError:
        print("First column is not an ID number! This row will be skipped.")
        good_line = False

    '''
    if not is_all_alphabets(data[1])
        good_line = False

    if not is_all_alphabets(data[2])
        good_line = False

    if not is_all_alphabets(data[3])
        good_line = False
    '''

    try:
        val = float(data[4])
    except ValueError:
        print("5th column is not a number! This row will be skipped.")
        good_line = False

    if(good_line):
        #Don't distinguish lowercase & uppercase names. So lowercase for all names. However, since the code challenge instruction specifically states the output drug name should be "exactly" the same as the input, we won't make the drug name lowercase.
        return [data[1].lower(), data[2].lower(), data[3], float(data[4]), good_line]
    else:
        return [None, None, None, None, good_line]


def read_input_file(input_file):
    """Read raw input file. Check missing/corrupted data at each cell. Make all last names and first names lowercase for comparison"""

    tuple = []

    with open(input_file) as f:
        for row in f:
            last_name, first_name, drug_name, drug_cost, good_line = read_line(row)
            if(good_line):
                #name.append(last_name+first_name)
                #drug.append(drug_name)
                #cost.append(drug_cost)
                tuple.append((last_name+first_name, drug_name, drug_cost))


    #return [map(lambda x:x.lower(), name), drug, cost]
    return tuple

def get_unique_drug_list(clean_table):
    """Return a dictionary. Key: unique drug. Value: number of prescriptions of the drug."""

    drug_list = [data[1] for data in clean_table]
    unique, counts = np.unique(drug_list, return_counts=True)
    return dict(zip(unique, counts))

def get_num_unique_name(clean_table, unique_drug_dict):
    """Return a list of number of unique person names for each drug."""

    num_unique_name = []
    i = 0
    name_list = [data[0] for data in clean_table]
    drug_list = [data[1] for data in clean_table]
    #print 'name_list', name_list
    #rint 'drug_list', drug_list
    while i < len(drug_list):
        #print 'i: ', i, ' drug_list[i] ', drug_list[i], unique_drug_dict[drug_list[i]]
        #print name_list[i:i+unique_drug_dict[drug_list[i]]]
        n_names = len(set(name_list[i:i+unique_drug_dict[drug_list[i]]]))
        num_unique_name.append(n_names) #in sorted alphabetically ascending order of drug name
        i += unique_drug_dict[drug_list[i]]
        #print 'n_names', n_names, ' i: ',i

    return num_unique_name


def get_total_cost_each_drug(clean_table, unique_drug_dict):#, num_unique_name_each_drug):
    """Compute the total cost for each drug."""

    total_cost_each_drug = []
    drug_list = [data[1] for data in clean_table]
    cost_list = [data[2] for data in clean_table]
    i = 0
    while i < len(drug_list):
        total_cost_each_drug.append(sum(cost_list[i:i+unique_drug_dict[drug_list[i]]])) #in sorted alphabetically ascending order of drug name
        i += unique_drug_dict[drug_list[i]]

    return total_cost_each_drug

def print_drug_info(clean_table, unique_drug_dict, num_unique_name_each_drug, total_cost_each_drug, output_file):
    """Print to output file."""

    #print clean_table
    #print unique_drug_dict
    #print num_unique_name_each_drug
    #print total_cost_each_drug

    output_table = []
    drug_list = [data[1] for data in clean_table]
    drug_count = 0
    i = 0
    while i < len(drug_list):
        output_table.append((drug_list[i], num_unique_name_each_drug[drug_count], total_cost_each_drug[drug_count]))
        drug_count += 1
        i += unique_drug_dict[drug_list[i]]

    #Sort first by drug name in ascending order
    output_table.sort(key=operator.itemgetter(0))
    #Sort then by total cost in descending order
    output_table.sort(key=operator.itemgetter(2), reverse=True)

    #Round to integer for the cost
    error_digit = 0
    temp = '{0:.'+str(error_digit)+'f}'

    with open(output_file, "w") as f:
        f.write('drug_name,num_prescriber,total_cost\n')
        for tuple in output_table:
            f.write(tuple[0]+','+str(tuple[1])+','+temp.format(round(tuple[2],error_digit))+'\n')
