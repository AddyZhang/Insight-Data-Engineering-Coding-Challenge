# Insight-Data-Engineering-Coding-Challenge

## Required Packages
```
os
sys
csv
time
datetime
```

## Run Instructions
To run the script, type`sh run.sh`in terminal </br>


## Approach
1. Since product and year are unique pairs, we create a dictionary called `product_dict` and its keys are product and year. For scalability, dictionary value is the object created by a class. </br>
2. This class needs product, year and company to initialize the object. Inside `__init__ method`, it will also initialize number of complaints and company list because we need to track number of complaints and company names for same product and year. </br>
3. The value for `product_dict` is then the object which has attributes of product, year, company, number of complaints and company list. We later access thoese attributes by `product_dict[(product,year)].ATTRIBUTE_NAME`. </br>
4. We also need two methods inside the class. When we find the key (product, year) not in dictionary, we create the object. If the key (product,year) exists in dictionary, we increment the complaint by one (`add_complaint instance method`) and append company to company list (`add_company instance method`). </br>
5. This is not the clean world. When we read line by line, we might encounter the following cases. It is necessary to create own edge tests and make code pass tests. Edge tests are in `insight_testsuite`.
```
1. Empty file
2. No headers
3. Empty lines before header
4. Has header but no data
5. Empty lines in data
6. Date received is empty
7. Date format is not YYYY-MM-DD
8. Product is empty
9. Company is empty
10. Product dictionary is empty
11. Line items less than header items
12. Line items larger than header items
```
6. To find the number of companies for the same product and year, we can find the number of unique items in the company list. To find the highest percentage of total complaints against one company, we can find the percentage of one company in the company list, e.g., [A,B,A]-> A:2/3, B:1/3. </br>
7. Sort results alphabetically and numerically in ascending order using `sorted()`.
8. When we write the data in output file, we need to add double quotes if there is a comma in product.
## Final Words
Thank you for providing me this opportunity. I would like to learn more and practice more. Let me know what I can improve on this code.
