"""
a script to notify me when there are changes to a webpage. simple logic:

- ADD LOGGER FUNCTIONALITY

- make this easier to tailor to other sites etc
"""

import logging
import urllib.request
from bs4 import BeautifulSoup


formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s > %(message)s", datefmt="%d-%b-%Y %I:%M:%S %p"
)

handler = logging.FileHandler("./logs.log")
handler.setFormatter(formatter)

logger = logging.getLogger("summary")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


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

# print(target_jobs)
# print(len(target_jobs))

if len(target_jobs) > 0:
    logger.info("Target job(s) found")
    # TODO: send email notifying me about this
    pass
else:
    # TODO: log that no jobs were found
    logger.info("Target job(s) NOT found")
    pass
