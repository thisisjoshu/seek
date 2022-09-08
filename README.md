# get-me-a-job

a script to notify me when there are changes to a webpage. simple logic:

- hash content of a webpage
- after X period of time, hash the content of webpage again
- if there is a change between the two hashes, notify me via email. 
- if no change then wait for X period of time


going forward:
- extend script to *only* notify me of specific changes and don't notify me of irrelevant changes
