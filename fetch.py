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

terms = ["human resources", "manager"]
# terms = ["systems analyst", "programmer"]

target_jobs = []
for job in jobs:
    position = job.get("data-title")
    for term in terms:
        if term in position.casefold():
            close_date = job.get("data-expires_at")
            url = job.get("data-url")
            metadata = {"position": position, "close_date": close_date, "url": url}

            # ensure that only unique data is appended
            if len(target_jobs) == 0:
                target_jobs.append(metadata)
            else:
                for found_jobs in target_jobs:
                    if url not in found_jobs.values():
                        target_jobs.append(metadata)

print(target_jobs)
print(len(target_jobs))
# check if target is in jobs list.
# If yes, then retrieve data from div attributes, if no then do nothing.

