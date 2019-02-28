"""Define functions for data ETL and I/O."""
import sys
import numpy as np
import operator


def read_line(row):
    """Read line from input file."""

    good_line = True #If true, this line contains valid data. Else, the line is skipped

    # Check for "" instances, which occurs in prescriber names and drug names
    quotation_loc = [i for i in range(len(row)) if row.startswith('\"', i)]
    #print quotation_loc

    if len(quotation_loc) > 0:
        #If we have odd number of quotation marks, a quotation mark is missing. Skip Line
        if len(quotation_loc)%2 != 0:
            good_line = False
            return [None, None, None, None, good_line, -1]
        else:
            data = []
            substrings = [row[0:quotation_loc[0]]] + [row[quotation_loc[i]:quotation_loc[i+1]+1] for i in range(len(quotation_loc)-1)] + [row[quotation_loc[len(quotation_loc)-1]+1:len(row)]]

            if(len(substrings[0].split(',')[:-1])>0):
                for x in substrings[0].split(',')[:-1]:
                    data.append(x)

            for s in range(1,len(substrings)-1):
                if s%2==1: #odd entry is between ""
                    data.append(substrings[s])
                else:
                    if(len(substrings[s].split(',')[1:-1])>0):
                        for x in substrings[s].split(',')[1:-1]:
                            data.append(x)
            if(len(substrings[len(substrings)-1].rstrip().split(',')[1:])>0):
                for x in substrings[len(substrings)-1].rstrip().split(',')[1:]:
                    data.append(x)

    else:
        data = row.rstrip().split(',')

    #print ('raw data'), data

    # Check for number of fields, which should be 5
    if len(data) != 5:
        good_line = False
        return [None, None, None, None, good_line, -1]

    # Check for missing fields. If any field is missing, the row is skipped
    if "" in data:
        good_line = False

    try:
        val = int(data[0])
    except ValueError:
        print("First column is not an ID number! This row will be skipped.")
        good_line = False

    try:
        val = float(data[4])
    except ValueError:
        print("5th column is not a number! This row will be skipped.")
        good_line = False

    if(good_line):
        #Don't distinguish lowercase & uppercase names. So lowercase for all names. However, since the code challenge instruction specifically states the output drug name should be "exactly" the same as the input, we won't make the drug name lowercase.
        if not '.' in data[4]:
            num_decimals = 0
        else:
            num_decimals = len(data[4].split('.')[1])
        return [data[1].lower(), data[2].lower(), data[3], float(data[4]), good_line, num_decimals]
    else:
        return [None, None, None, None, good_line, -1]


def read_input_file(input_file):
    """Read raw input file. Check missing/corrupted data at each cell. Make all last names and first names lowercase for comparison"""

    tuple = []
    max_digit = 0

    with open(input_file) as f:
        for row in f:
            last_name, first_name, drug_name, drug_cost, good_line, num_decimals = read_line(row)
            if(good_line):
                #name.append(last_name+first_name)
                #drug.append(drug_name)
                #cost.append(drug_cost)
                tuple.append((last_name+first_name, drug_name, drug_cost))
                if num_decimals > max_digit:
                    max_digit = num_decimals

    return [tuple, max_digit]

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

    while i < len(drug_list):
        n_names = len(set(name_list[i:i+unique_drug_dict[drug_list[i]]]))
        num_unique_name.append(n_names) #in sorted alphabetically ascending order of drug name
        i += unique_drug_dict[drug_list[i]]

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

def print_drug_info(clean_table, unique_drug_dict, num_unique_name_each_drug, total_cost_each_drug, output_file, error_digit):
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
    temp = '{0:.'+str(error_digit)+'f}'

    with open(output_file, "w") as f:
        f.write('drug_name,num_prescriber,total_cost\n')
        for tuple in output_table:
            f.write(tuple[0]+','+str(tuple[1])+','+temp.format(round(tuple[2],error_digit))+'\n')
