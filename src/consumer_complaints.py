#!/user/bin/env python3

##
## Yuanhui Zhang
## 04/17/2020
##
## Process number of complaints, number of companies
## and highest percentage of total complaints against
## one company for the same product and year.
## To handle unexpectd data in a large amount of dataset
## when we read line by line, we print error messgaes
## including line number instead of raising error.
## This way could help us to find where the error is and fix data.
## We use edge cases to test the code if it passes rare cases.
##

import os
import sys
import csv
import time
import datetime

class Product_Record():
    """
    This class keeps track of product, year,
    company, the number of complaint increment,
    and list of companies.
    """
    def __init__(self,product,year,company):
        # product: Product
        # year: year from Date Received
        # num_of_complaint: the number of
        # complaints is 1 when we create
        # the object.
        # company: Company
        # company_list: initialize the
        # list and put a object company
        # in it; we will append the company
        # to this list.
        self.product = product
        self.year = year
        self.num_of_complaints = 1
        self.company = company
        self.company_list = [company]

    def add_complaint(self):
        # increase the number of complaint by 1
        self.num_of_complaints += 1

    def add_company(self, company):
        # append the company to company list
        self.company_list.append(company)

def add_to_product_dict(product_dict, product, year, company):
    """
    Check if (product,year) in dictionary keys, if it is, it calls
    add_complaint to increment the number of complaint by one and add_company
    to append the company to the company list. If it is not, it creates
    the new object.
    """

    if (product,year) in product_dict.keys():
        product_dict[(product,year)].add_complaint()
        product_dict[(product,year)].add_company(company)
    else:
        product_dict[(product,year)] = Product_Record(product,year,company)

def get_num_companies(company_list):
    """Count the number of unique companies"""
    # use set to remove duplicates
    num_companies = len(set(company_list))
    return int(num_companies)

def get_highest_per(company_list):
    """Find the highest percentage of company"""
    percentage_list = []
    total = len(company_list)
    for comp in set(company_list):
        # count the number of comp in company list
        val = company_list.count(comp)
        res = round(val/total*100,0)
        percentage_list.append(res)

    # return the maximum percentage
    return int(max(percentage_list))

def validate(date_string):
    """Check datetime if its formate is YYYY-MM-DD"""
    try:
        # check if the below statement raises error
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except:
        return False
    else:
        return True

def date_to_year(date):
    """Extract Year from Date"""
    # split the date with '-'
    year = [d for d in date.split('-')][0]
    return int(year)

def check_item(attribute, attribute_names):
    """ Check if attribute exists in attribute names"""
    if attribute in attribute_names:
        # get index
        index = attribute_names.index(attribute)
    else:
        print('Could not find %s in header!'%attribute)
        print('The program will exit!')
        exit()
    return index

def read_csv(file):
    """Read the csv file and output dictionary"""
    # can we check if it is not comma seperated
    # use csv module to read the csv file
    csvreader = csv.reader(file,quotechar='"',delimiter=',')
    attribute_names = next(csvreader)

    # count line, starting from header (line 1)
    line_count = 1

    # skip the empty lines
    while True:
        # check if line is empty or not
        if len(attribute_names) == 0:
            # assign the next line to attribute_names
            attribute_names = next(csvreader)
            line_count += 1
        else:
            # if we find nonempty line then break
            break

    # check if attribute_names is a header by checking if digit inside
    if any(cell.isdigit() for cell in attribute_names):
        print("Please add header!")
        print("Program will exit")
        exit()

    # check if date received exists in header
    idx_date = check_item('Date received', attribute_names)

    # check if product exists in header
    idx_product = check_item('Product', attribute_names)

    # check if company exists in header
    idx_company = check_item('Company', attribute_names)

    # identify if the rest of csvreader has rows or not
    has_rows = False

    # create product dictionary
    product_dict = {}

    # unexpected data will show on console with the line number
    print("\n------The unexpectd data with line number------\n")
    # read data line by line
    for line in csvreader:
        # set has_rows to true
        has_rows = True

        # increment the line count
        line_count += 1

        # check if line is empty or not
        if len(line) == 0:
            # skip this line
            continue

        # check if line has complete items as header
        if len(line) < len(attribute_names):
            print("Missing some of Line %i data\n"%line_count)
            # skip this line
            continue

        # if line overbound
        if len(line) > len(attribute_names):
            print("Items in Line %i are over bound!\n"%line_count)
            # skip this line
            continue

        # check if the date is empty
        if not line[idx_date]:
            print("Line %i Item[%i] is empty. Expected input is date received!"%(line_count,idx_date))
            # skip the line
            continue
        else:
            # validate the date
            if validate(line[idx_date]):
                # get year
                year = date_to_year(line[idx_date])
            else:
                print("Line %i has invalid date format. It should be YYYY-MM-DD"%line_count)
                # skip this line
                continue

        # check if product is empty
        if not line[idx_product]:
            print("Line %i Item[%i] is empty. Expected input is product!"%(line_count,idx_product))
            # skip the line
            continue
        else:
            # get product
            product = line[idx_product]
            # lowercase product
            product = product.lower()

        # check if company is empty
        if not line[idx_company]:
            print("Line %i Item[%i] is empty. Expected input is company!"%(line_count,idx_company))
            # skip the line
            continue
        else:
            # get company
            company = line[idx_company]
            # lowercase company
            company = company.lower()

        # add product, year, company to product_dict (python dict)
        add_to_product_dict(product_dict,product,year,company)

    # if has_rows still false, exit the program
    if not has_rows:
        print("The csv file only has only header but no data")
        print("Program will exit!")
        exit()

    # check if product_dict is empty or not
    if not product_dict:
        print("No result! Check your data in the csv file")
        print("Program will exit!")
        exit()
    else:
        print("\n-------Required data in results_dict now-------\n")

    return product_dict

def open_file(filepath):
    """
    Open csv file if not
    found throw IOError.
    """

    try:
        # open file
        file = open(filepath, 'r')

    except IOError:
        # display error message on console
        print("INPUT FILE NOT FOUND OR PATH NOT CORRECT")
        exit()

    else:
        # check file if it is empty or not
        if os.stat(filepath).st_size > 0:
            # read csv file
            with file as f:
                data = read_csv(f)
            # close file
            file.close()
        else:
            print("Empty file!")
            print("Program will exit!")
            exit()

        return data

def save_file(filepath,data):
    """
    Save as a csv file
    """
    try:
        # create a file
        file = open(filepath, "x")

    except IOError:
        # throw error and append data
        print("File Already Exists!")
        print("Will Append to Existing File")
        file = open(filepath, 'a')

    finally:
        # write header
        # file.write("product, year, total number of complaints, total number of companies received at least one complaint, highest percentage\n")

        # write data
        for record in data:
            # add double quotes if comma in product and set product string lowercase
            if ',' in record[0]:
                file.write('"%s",%i,%i,%i,%i\n'%(record[0], record[1],
                            record[2], record[3], record[4]))
            else:
                file.write('%s,%i,%i,%i,%i\n'%(record[0], record[1],
                            record[2], record[3], record[4]))
        file.close()

def main():
    '''Main Routine'''

    ###########################################################
    #  Input files					      #
    ###########################################################
    PRODUCT_PATH = sys.argv[1]
    OUTPUT_PATH = sys.argv[2]

    # open file and process data
    results_dict = open_file(PRODUCT_PATH)

    ####################################################################################
    # Generate report: 								       #
    # 	  1) product: a list of products in alphabetical order                         #
    #     2) year: a list of years in ascending order                                  #
    #     3) num_of_complaints: number of complaints received for the product and year #
    #     4) num_of_companies: number of unique companies recevices complaints         #
    #     5) highest_per: highest percentage that company receives complaints          #
    #										       #
    ####################################################################################

    # results_list
    #
    # results_list[0] = product
    # results_list[1] = year
    # results_list[0] = num_of_complaints
    # results_list[1] = num_of_companies
    # results_list[0] = highest_per

    # create a new results list
    results_list = []

    # convert dictionary to list
    for key, value in results_dict.items():
        # lowercase company_list

        # get number of companies
        num_of_companies = get_num_companies(value.company_list)

        # get highest percentage
        highest_per = get_highest_per(value.company_list)

        # append results to results_list
        results_list.append([value.product,value.year,value.num_of_complaints,
                            num_of_companies, highest_per])

    # sort results alphabetically and numerically in ascending order
    sorted_results_list = sorted(results_list)

    # save sorted_results_list as csv file
    save_file(OUTPUT_PATH, sorted_results_list)

if __name__ == "__main__":

    # start time
	start_time = time.time()

	# main routine
	main()

	# print total time
	elapsed = time.time() - start_time
	print("\n--------This script runs %.2f seconds!---------\n" % elapsed)
