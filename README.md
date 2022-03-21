# HackCWRU Submission
This project was created as a submission to [HackCWRU](https://hackcwru-2022.devpost.com/) and won `Most Creative Use of GitHub`. The submission can be found [here](https://devpost.com/software/tipship).
**Team Members**: _Jonathan Lo, Eric Wang, Bryton Lee,_ and _Ajay Ahooja_. 

## TipShip
TipShip, with just a few commands and clicks, the user can pay another user in the server a designated amount of money. The bot will create an order through Paypal, and the user can simply login and execute the payment. This discord bot is also accompanied by a web app that displays the user's transactions, spending's and earnings, and analysis with predictions on future spending trends.

## Inspiration
We play MMO games regularly, using Discord voice channels to communicate, and we have often wanted to sell each other legendary or rare equipment. Instead of opening Venmo or remembering to pay our friends the next time we see each other (shoutout the pandemic), we wanted a quick, easy, and safe way to send money through platforms that we already regularly use. Many game platforms do not support players exchanging real currency to each other, so the next best thing for us is Discord, and I'm sure many other gamers have felt the same way!


## Tech Stack
The backend is in Python utilizing the [Django](https://www.djangoproject.com/) framework. The front end is a mix of HTML/CSS and JavaScript. We use Jquery AJAX requests to asynchronously update the front end. Moreover, we use [Chart.js](https://www.chartjs.org/) to create a chart of spending over a period of time. The ML analysis and pipline utilize [scikit-learn](https://scikit-learn.org/stable/). The database is running on a [GCP MySQL](https://cloud.google.com/sql/docs/mysql) instance. 

The discord bot lives on a Flask runtime and utilizes it to `GET` and `POST` to our Django WebApp utilzing an open CORS policy and built API endpoints. Moreover, it utilizes PayPal's REST SDK to securely transfer payments.

Code Flow:
![](https://cdn.discordapp.com/attachments/942218891952783421/955350480983298058/unknown.png)

## Running

 1. Clone the repository.
 2. Install `pipenv` and the dependencies in `Pipfile`.
 3. Launch `pipenv` enviroment using:
```bash
pipenv shell
```
 4. Create a `config.json` and input Client IDs, Secrets, and Tokens according to `config.json.example`. You will need PayPal and Discord credentials.
 5. Connect **Google Cloud Platform** MySQL instance using [official documentation](https://cloud.google.com/python/django/appengine).
 6. Start local server using: 
  ```
  python3 manage.py runserver
  ```
  7. In a different terminal, launch **TipShip** Discord Bot by running `notebooks/flask_server.py` concurrently with `notebooks/test_script.py`.
