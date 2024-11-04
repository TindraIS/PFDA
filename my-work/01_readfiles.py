# read in text and csv files

import csv

FILENAME_TXT = "01_data.txt"

print (FILENAME_TXT)
with open(FILENAME_TXT, "rt") as fp:
    total = 0
    for line in fp:
        total += int(line)
        print (f"{line} is size {len(line)}")
    print("")
    print (f"total is {total}\n__________TXT END__________\n")


FILENAME_CSV = "01_iris.csv"

with open (FILENAME_CSV, "rt") as fp:
    reader = csv.reader(fp, delimiter="," , quoting=csv.QUOTE_MINIMAL) # https://docs.python.org/3/library/csv.html
    linecount = 0
    total = 0
    for line in reader:
        if linecount == 0: # first row ie header row (same as >0)
            #print (f"{line}\n-------------------")
            pass
        else: # all subsequent rows
            try:
                total += float(line[1]) # Convert col 2 to float
            except ValueError:
                print(f"Non-numeric data encountered: {line[1]} at row {linecount}")
                continue
        linecount += 1
    print (f"average of col 2 is {total/(linecount-1)}")