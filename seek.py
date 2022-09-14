import os
import sendgrid
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from sendgrid.helpers.mail import Mail, Email, To, Content


def lambda_handler(event, context):
    jobs = get_markup()
    target_jobs = search_for_target(jobs)
    notify(target_jobs)


def get_markup():
    fp = urllib.request.urlopen(os.environ.get("SITE"))
    markup_bytes = fp.read()
    markup_str = markup_bytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(markup_str, "html.parser")
    jobs = soup.find_all("div", {"class": "jobblock block"})
    return jobs


def search_for_target(jobs):
    terms = ["systems analyst", "programmer"]

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
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    if len(target_jobs) > 0:
        print("Target job(s) found!")
        for job in target_jobs:
            from_email = Email(os.environ.get("SENDER"))
            to_email = To(os.environ.get("RECIPIENT"))
            subject = "Job Vacancy Found!!"
            message = get_found_message(job)
            content = Content("text/html", message)
            mail = Mail(from_email, to_email, subject, content)

            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()
            # Send an HTTP POST request to /mail/send
            response = sg.client.mail.send.post(request_body=mail_json)
            print(response.status_code)
            print(response.headers)
            print("Notification sent via email")
    else:
        print("Target job(s) NOT found")

        from_email = Email(os.environ.get("SENDER"))
        to_email = To(os.environ.get("RECIPIENT"))
        subject = "No Jobs Found :("
        message = get_not_found_message()
        content = Content("text/html", message)
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()
        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)
        print("Notification sent via email")


def get_found_message(job):
    message = """
    <p>Hi %s,</p>
    <br/>
    <p>Great News!</p>
    <p>There is a vacancy for <b>%s</b> at FFA. This vacancy will be closed on <i>%s</i>. 
    More information can be found <a href="%s">here</a>.</p>
    <br/>
    <p>Cheers,</p>
    <p>Your favorite bot :)</p>
    """ % (
        os.environ.get("NAME"),
        job["position"],
        convert_date_format(job["close_date"]),
        job["url"],
    )
    return message


def get_not_found_message():
    message = """
    <p>Hi %s,</p>
    <br/>
    <p>Unfortunately, no relevant vacancies were found on the FFA website. 
    I will check again next month! ;)</p>
    <br/>
    <p>Cheers,</p>
    <p>Your favorite bot :)</p>
    """ % (
        os.environ.get("NAME")
    )
    return message


def convert_date_format(datetime_str):
    dto = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S %z")
    # convert = datetime.strftime(dto, '%d-%B-%Y %H:%M:%S')
    convert = datetime.strftime(dto, "%c")
    return convert


if __name__ == "__main__":
    lambda_handler(None, None)
