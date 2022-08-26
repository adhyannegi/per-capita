##########################################################################
#    Computer Project #8
#    Algorithm
#        >5 functions defined.        
#        >Main function starts with calling open_file() and read_file()
#        and then calls add_per_capita(). Then it prints summary data
#        of each region and country by creating a for loop and calling
#        display_region() for each iteration. Ends by printing a 
#        thank you message.
##########################################################################

import csv
from operator import itemgetter

def open_file():
    ''' 
    Tries to open file based on user input and returns file pointer.           
    Value: Takes no value.
    Returns: File pointer.
    '''
    ans = True
    #Appropriate file or else ask for user input again.
    while ans:
        filename = input("Input a file: ")
        try:
            fp = open(filename, encoding='utf-8')
            return fp
            ans = False
        except:
            print("Error: file does not exist. Please try again.")


def max_in_region(D,region):
    '''
    Calculates maximum per-capita diabetes in the given region.
    Param: Dictionary of lists
    Returns: Tuple
    '''
    max1 = 0    #setting max to a small number
    list2 = D[region]
    for i in list2:
        #if value is greater than max, replace max and set the 
        #list of that max as focused list.
        if i[3] > max1:
            max1 = i[3]
            list3 = i
    ans1 = list3[0], max1    #list3[0] is country name.
    return ans1

                
def min_in_region(D,region):
    '''
    Calculates minimum per-capita diabetes in the given region.
    Param: Dictionary of lists
    Returns: Tuple
    '''
    min1 = 99999999    #setting min to a large number
    list2 = D[region]
    for i in list2:
        #i value is less than min, replace min and set the
        #list of that min as foucused list.
        if i[3] < min1:
            if i[3] != 0.0:
                min1 = i[3]
                list3 = i
    ans1 = list3[0], min1    #list3[0] is country name.
    return ans1


def read_file(fp):
    '''
    Reads file and creates a dictionary according to data.
    Param: File pointer
    Returns: Dictionary of sorted list of lists
    '''
    reader = csv.reader(fp)    #csv reader object
    next(reader, None)    #skips first line
    D = {}
    for line in reader:
        region = line[1]    #assigning values
        country = line[2]
        diabetes = line[9]
        population = line[5]
        #to replace "," with an empty string in population
        population = population.replace(",", "")    
        #skips line if diabetes or population have no value
        if diabetes == "-" or population == "-":
            continue
        
        if region not in D:
            #initializes empty list and appends value
            D[region] = []
            D[region].append([country, float(diabetes), float(population)])
        else:
            #appends value to already existing list
            D[region].append([country, float(diabetes), float(population)])
    
    #Sorts the dictionary where each list of countries in each region is 
    #sorted alphabetically by county name
    for key in D:
        D[key].sort(key = itemgetter(0))
    
    return D


def add_per_capita(D):
    '''
    Calculates diabestes per capita for each country and appends it into each
    country's list.
    Param: Dictionary of lists
    Returns: Dictionary of lists
    '''
    #loops through lists present in region list
    for key in D:
        for i in range(0, len(D[key])):              
            #appends 0.0 if there is a ZeroDivisionError, else 
            #divides diabetes by population and appends that value.
            try:         
                diabetes = D[key][i][1]
                population = D[key][i][2]
                per_capita = float(diabetes/population)
                D[key][i].append(per_capita)
            except ZeroDivisionError:
                D[key][i].append(0.0)
    return D


def display_region(D,region):
    '''
    Displays summary data for the region followed by a table with 
    the data for each country.
    Param: Dictionary of lists, String
    Returns: Nothing
    Displays: table of region data
    '''
    #to find out region cases and region population
    for i in D[region]:
        if i[0] == region:            
            total_cases = i[1]
            total_population = i[2]
    #region per capita
    total_per_capita = total_cases/total_population    
    
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Region","Cases", \
        "Population","Per Capita"))
    #this is the summary of the region: total cases, total population
    #and total diabetes per captia
    print("{:<37s} {:>9.0f} {:>12,.0f} {:>11.5f}".format(region, total_cases,\
         total_population, total_per_capita))
    print()    #empty line
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Country","Cases",\
        "Population","Per Capita"))
    
    #sorts the region list from highest to lowest diabetes per capita value
    D[region].sort(key = itemgetter(3), reverse = True)
    
    #prints summary for each country in the region
    for i in range(len(D[region])):
        #skips if country is region name
        if D[region][i][0] == region:
            continue
        print("{:<37s} {:>9.1f} {:>12,.0f} {:>11.5f}".format(D[region][i][0],\
             D[region][i][1], D[region][i][2], D[region][i][3]))
    
    print("\nMaximum per-capita in the {} region".format(region))
    print("{:<37s} {:>11s}".format("Country","Per Capita"))
    #prints maximum per capita value with the help of max_in_region() function
    max_country, max_per_capita = max_in_region(D, region)
    
    print("{:<37s} {:>11.5f}".format(max_country, max_per_capita))
    print("\nMinimum per-capita in the {} region".format(region))
    print("{:<37s} {:>11s}".format("Country","Per Capita"))
    #prints minimum per capita value with the help of min_in_region() function
    min_country, min_per_capita = min_in_region(D, region)
    
    print("{:<37s} {:>11.5f}".format(min_country, min_per_capita))
    
    
def main():
    fp = open_file()
    Dict1 = read_file(fp)
    Dict2 = add_per_capita(Dict1)
    for region in Dict2:
        print("Type1 Diabetes Data (in thousands)")
        display_region(Dict2, region)
        print()
        print("-"*72)
    print('\n Thanks for using this program!\nHave a good day!')
    

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__": 
    main()
