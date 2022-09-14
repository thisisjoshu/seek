# Seek

Seek is a simple tool that periodically checks a webpage for specific keywords. I was urged to keep checking a website for specific job vacancies and I knew that I would always forget to do so. Hence, I went ahead and wrote a simple script to do the checking for me and subsequently notify me via email if a relevant job vacancy is found or not. The live version of *Seek* is hosted on AWS Lambda so you will notice that this repository and the code is tailored to suit Lambda. This can be modified to work with any website, although some adjustments to the code will be necessary to fit the HTML of the target website. 


### Prerequisites & Installing

Simply install requirements with:

```
pip install -r requirements.txt
```

Ensure that the environment variables are set to your preference then it should be good to go!


## Built With

* [Sendgrid](https://app.sendgrid.com/) - Email API

## Authors

* **Joshua Zobule** - [thisisjoshu](https://github.com/thisisjoshu)