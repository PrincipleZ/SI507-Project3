from bs4 import BeautifulSoup
import unittest
import requests
import csv
import os


#########
# Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
# Of course, it could be structured in an easier/neater way, and if a
# student decides to commit to that, that is OK.

# NOTE OF ADVICE:
# When you go to make your GitHub milestones, think pretty seriously about
# all the different parts and their requirements, and what you need to
# understand. Make sure you've asked your questions about Part 2 as much
# as you need to before Fall Break!

# Function to fetch and cache a website and return the data in the form that
# BeautifulSoup can use. The function should fit into the first parameter of
# a BeautifulSoup object constructor.


def get_and_cache(url, filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
            return data
    except:
        data = requests.get(url).text
        f = open(filename, "w")
        f.write(data)
        f.close()
        return data

######### PART 0 #########

# Write your code for Part 0 here.
soup_part0 = BeautifulSoup(
    get_and_cache(
        "http://newmantaylor.com/gallery.html",
        "gallery.html"),
    "html.parser")

imgList = soup_part0.find_all("img")
for i in imgList:
    try:
        print(i["alt"])
    except:
        print("No alternative text provided!")

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but
# if you prefer to build up the code to do this scraping and caching
# yourself, that is OK.
main_soup = BeautifulSoup(
    get_and_cache(
        "https://www.nps.gov/index.htm",
        "nps_gov_data.html"),
    "html.parser")

# Get individual states' data...


dropdown_menu = main_soup.find("ul", {"role": "menu"})
state_list = dropdown_menu.find_all("li")
for i in range(len(state_list)):
    temp = state_list[i].a
    state_list[i] = temp

# helper function to navigate through main_soup object and access certain
# state as defined in the parameter and return the BeautifulSoup object of
# that state's website.


def get_state_data(state):
    for i in state_list:
        if i.text == state:
            print("URL found:" + "https://www.nps.gov" + i["href"])
            return BeautifulSoup(
                get_and_cache(
                    "https://www.nps.gov" +
                    i["href"],
                    state.lower() +
                    "_data.html"),
                "html.parser")
    print("The state you entered is not valid. \
          Please entered as first letter is capitalized such as 'California'")

three_states = []
three_states.append(get_state_data("Arkansas"))
three_states.append(get_state_data("California"))
three_states.append(get_state_data("Michigan"))

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using
# the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href'
# attributes of the 'a' tag objects in each li, instead of the full li
# objects

# Filter the list of relative URLs you just got to include only the 3 you
# want: AR's, CA's, MI's, using the accumulator pattern & conditional
# statements

# Create 3 URLs to access data from by appending those 3 href values to
# the main part of the NPS url. Save each URL in a variable.

# To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is
# "http://www.nps.gov/state/me/index.htm", Michigan's is
# "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the
# values in those href attributes you just got... how can you build the
# full URLs?

# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)

# And then, write each set of data to a file so this won't have to run
# again.

######### PART 2 #########

# Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might
# be useful for your investigation! So, of course, might be .find or
# .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the
# parks/sites/etc in a certain state, but you want the class to represent
# just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that
# represents the HTML about 1 park. However, your code should rely upon
# HTML data about Michigan, Arkansas, and Califoria you saved and accessed
# in Part 1.

# However, to begin your investigation and begin to plan your class
# definition, you may want to open this file and create a BeautifulSoup
# instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in
# the instructions -- e.g. if no type of park/site/monument is listed in
# input, one of your instance variables should have a None value...

# Define your class NationalSite here:

# Recommendation: to test the class, at various points, uncomment the
# following code and invoke some of the methods / check out the instance
# variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


class NationalSite(object):

    def __init__(self, soupObject):
        generalSoup = soupObject.find_all("div")[0]
        self.location = generalSoup.h4.text
        self.name = generalSoup.h3.text
        self.type = generalSoup.h2.text
        self.description = generalSoup.p.text.replace("\n", "")
        infoSoup = soupObject.find_all("div")[1].find_all("div")[1]
        infoList = infoSoup.find_all("a")
        self.infoUrl = ""
        for i in infoList:
            if "Basic" in i.text:
                self.infoUrl = i["href"]

    def __str__(self):
        return self.name + " | " + self.location

    def get_mailing_address(self):
        if not os.path.exists("park_cache/"):
            os.makedirs("park_cache/")
        mailingSoup = BeautifulSoup(
            get_and_cache(
                self.infoUrl,
                "park_cache/" + self.name +
                "_info.html"),
            "html.parser")
        address_div = mailingSoup.find("div", {"class": "mailing-address"})
        address_text = address_div.find("p", {"class": "adr"}).text
        address_text = address_text.strip().replace("\n", "/").replace("///", "/")
        return address_text

    def __contains__(self, name):
        return name in self.name


test = NationalSite(three_states[0].find_all("li", {"class": "clearfix"})[0])


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that
# represent each park, for each state.

# Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)

arkansas_natl_sites = []
california_natl_sites = []
michigan_natl_sites = []

ar_list = three_states[0].find("ul", {"id": "list_parks"}) \
    .find_all("li", {"class": "clearfix"})
ca_list = three_states[1].find("ul", {"id": "list_parks"}) \
    .find_all("li", {"class": "clearfix"})
mi_list = three_states[2].find("ul", {"id": "list_parks"}) \
    .find_all("li", {"class": "clearfix"})

for i in ar_list:
    arkansas_natl_sites.append(NationalSite(i))

for i in ca_list:
    california_natl_sites.append(NationalSite(i))

for i in mi_list:
    michigan_natl_sites.append(NationalSite(i))


######### PART 4 #########

# Remember the hints / things you learned from Project 2 about writing CSV
# files from lists of objects!

# Note that running this step for ALL your data make take a minute or few
# to run -- so it's a good idea to test any methods/functions you write
# with just a little bit of data, so running the program will take less
# time!

# Also remember that IF you have None values that may occur, you might run
# into some problems and have to debug for where you need to put in some
# None value / error handling!
def toDict(park):
    returnDict = {"Name": park.name, "Location": park.location,
                  "Type": park.type, "Address": park.get_mailing_address(),
                  "Description": park.description}
    for keys in returnDict:
        if returnDict[keys] == "":
            returnDict[keys] = "None"
    return returnDict


def toCSV(filename, inputList):
    if not os.path.isfile(filename):
        with open(filename, "w", newline="", encoding='utf-8') as f:
            fieldnames = ["Name", "Location", "Type", "Address", "Description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in inputList:
                writer.writerow(toDict(item))
    else:
        current_name_list = []
        with open(filename, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                current_name_list.append(row["Name"])
        with open(filename, "a", newline="", encoding='utf-8') as f:
            fieldnames = ["Name", "Location", "Type", "Address", "Description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for item in inputList:
                if str(item.name) not in current_name_list:
                    writer.writerow(toDict(item))

toCSV("arkansas.csv", arkansas_natl_sites)
toCSV("california.csv", california_natl_sites)
toCSV("michigan.csv", michigan_natl_sites)
