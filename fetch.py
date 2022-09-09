"""
a script to notify me when there are changes to a webpage. simple logic:

- hash content of a webpage
- after X period of time, hash the content of webpage again
- if there is a change between the two hashes, notify me via email. 
- if no change then wait for X period of time

- extend script to *only* notify me of specific changes and don't notify me of irrelevant changes

- ADD LOGGER FUNCTIONALITY
"""

import urllib.request
from bs4 import BeautifulSoup


fp = urllib.request.urlopen("https://piffa.applynow.net.au/")
markup_bytes = fp.read()
markup_str = markup_bytes.decode("utf8")
fp.close()

soup = BeautifulSoup(markup_str, "html.parser")
jobs = soup.find_all("div", {"class": "jobblock block"})

# Systems Analyst/Programmer will be the targets
targets = ['human resources', 'manager']

for job in jobs:
    job_title = job.get("data-title")
    expiration = job.get("data-expires_at")
    url = job.get("data-url")
    
    print(job_title)
    print(expiration)
    print(url)
    
    for target in targets:
        if target in job_title.casefold():
            print("target found")
    

# check if target is in jobs list.
# If yes, then retrieve data from div attributes, if no then do nothing.

