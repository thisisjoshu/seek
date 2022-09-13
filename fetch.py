import logging
import urllib.request
from bs4 import BeautifulSoup

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


def main():
    jobs = get_markup()
    target_jobs = search_for_target(jobs)
    notify(target_jobs)


def get_logger():
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s > %(message)s", datefmt="%d-%b-%Y %I:%M:%S %p"
    )

    handler = logging.FileHandler("./logs.log")
    handler.setFormatter(formatter)

    logger = logging.getLogger("summary")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def get_markup():
    fp = urllib.request.urlopen("https://piffa.applynow.net.au/")
    markup_bytes = fp.read()
    markup_str = markup_bytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(markup_str, "html.parser")
    jobs = soup.find_all("div", {"class": "jobblock block"})
    return jobs


def search_for_target(jobs):
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
    return target_jobs


def notify(target_jobs):
    logger = get_logger()

    if len(target_jobs) > 0:
        logger.info("Target job(s) found")
        
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("joshuxbot@gmail.com")  # Change to your verified sender
        to_email = To("joshwhizkid@gmail.com")  # Change to your recipient
        subject = "Sending with SendGrid is Fun"
        content = Content("text/plain", "and easy to do anywhere, even with Python")
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()
        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)
        logger.info("Notification sent via email")
    else:
        logger.info("Target job(s) NOT found")


if __name__ == "__main__":
    main()
