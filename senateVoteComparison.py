#imports the HTML parsing tool from the class 'HTMLParser' to be used for
#parsing HTML code into a readable string
from html.parser import HTMLParser

#imports the 'urllib' library to fetch the web pages
import urllib.request

#imports the 'time' library so that the 'sleep' function can be used when
#requesting the web pages. This will cause a delay in the requests so
#that the hosting server does not block the program from making many of
#these requests one after another
import time

#import ssl and then disable the cert checking
#*this is not recommended*
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

###placed here as a note to help remember the formatting code to loop
###through the vote number in the url (example: vote 00001 - vote 00392).
###It is tricky because of the leading 0's. Here is the code: 000%d'%(i)

#sets the program to loop through a range of webpages to pull multiple pieces
#of the desired information at one time. So, for example, it can pull
#votes 100-150 of a given session rather than just vote 100
for i in range(1,50):
    req = urllib.request.Request('http://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=112&session=1&vote={:05d}'.format(i), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'})
    response = urllib.request.urlopen(req)
    page_in_html_byte = response.read()
    time.sleep(1)

    #decode the entire HTML byte-string into a Python string
    #and rename it as a variable, 'page', for ease 
    page = page_in_html_byte.decode('utf-8')

    #sets the variable 'info' equal to the information needed from the
    #question to the last senator needed
    info = page[page.index("<question>")-10:page.index("Sanders")]

    #remove the tags and other HTML syntax from 'info'
    #and just give the raw data, or what we would see on the actual webpage
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()  # call the parent's constructor
            self.stuff = ""
        def handle_data(self, data):
            self.stuff += data
           
    parser = MyHTMLParser()
    parser.feed(info)

    #print the desired information about the bill including: 
    #1) measure/amendment/nomination number
    #2) vote number
    #3) measure title/statementxof purpose/nomination description
    #4) vote date

    #1) print the measure number, amendment number, or nomination number
    if "Measure Number" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Measure Number"):parser.stuff.index("Measure Title")])
    elif "Amendment Number" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Amendment Number"):parser.stuff.index("Statement of Purpose")])
    elif "Nomination Number" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Nomination Number"):parser.stuff.index("Nomination Description")])

    #2) print the vote number
    print(parser.stuff[parser.stuff.index("Vote Number"):parser.stuff.index("Vote Date")])

    #3) print the measure title, statement of purpose, or nomination description
    if "Measure Title" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Measure Title"):parser.stuff.index("Vote Count")])
    elif "Statement of Purpose" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Statement of Purpose"):parser.stuff.index("Vote Count")])
    elif "Nomination Description" in parser.stuff:
        print(parser.stuff[parser.stuff.index("Nomination Description"):parser.stuff.index("Vote Count")])

    #4) print the vote date
    print(parser.stuff[parser.stuff.index("Vote Date"):parser.stuff.index("Req")])

    #print how the senators voted (Yay, Nay, or Not Voting)
    #Senator Rand Paul of Kentucky (since 2011)
    print(parser.stuff[parser.stuff.index("Paul (R-KY)"):parser.stuff.index("Paul")+18])
    #Senator Marco Rubio of Florida (since 2011)
    print(parser.stuff[parser.stuff.index("Rubio (R-FL)"):parser.stuff.index("Rubio")+18])
    #Senator Ted Cruz of Texas (since 2013)
    #print(parser.stuff[parser.stuff.index("Cruz (R-TX)"):parser.stuff.index("Cruz")+18])
    #Senator Lindsey Graham of South Carolina (since 2003)
    print(parser.stuff[parser.stuff.index("Graham (R-SC)"):parser.stuff.index("Graham")+18])

    #print a spacer for ease of reading
    print()
    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print()
    print()

#let the user know the program has finished running
print("The program has finished running")
