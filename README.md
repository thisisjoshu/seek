# Seek

Seek is a simple tool that periodically checks a webpage for specific keywords. I was urged to keep checking a website for specific job vacancies and I knew that I would always forget to, so I went ahead and wrote a simple script to do the checking for me and subsequently notify me via email if a relevant job vacancy is found or not. The live version of *Seek* is hosted on AWS Lambda so you will find that the repository is tailored to suit Lambda. 


### Prerequisites & Installing

Simply install requirements with:

```
pip install -r requirements
```

Ensure that the environment variables are set to your preference then it should be good to go!


## Built With

* [Sendgrid](https://app.sendgrid.com/) - Email API

## Authors

* **Joshua Zobule** - [thisisjoshu](https://github.com/thisisjoshu)