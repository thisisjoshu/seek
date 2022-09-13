import os
import logging
import sendgrid
import urllib.request
from time import sleep
from bs4 import BeautifulSoup
from sendgrid.helpers.mail import Mail, Email, To, Content


def main():
    while True: 
        jobs = get_markup()
        target_jobs = search_for_target(jobs)
        notify(target_jobs)
        sleep(10)


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

        for job in target_jobs:
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
            from_email = Email("joshuxbot@gmail.com")  # Change to your verified sender
            to_email = To("joshwhizkid@gmail.com")  # Change to your recipient
            subject = "Job Vacancy Found!!"
            message = """
            <p>Hi Joshua,</p>

            <p>There is a vacancy for %s at FFA. This vacancy will be closed on <i>%s</i>. More information can be found <a href="%s">here</a>.</p>
            <br/>
            <p>Regards,</p>
            <p>Your favorite bot :)</p>
            """ % (
                job["position"],
                job["close_date"],
                job["url"],
            )

            content = Content("text/html", message)
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


if __name__ == "__main__":
    main()
