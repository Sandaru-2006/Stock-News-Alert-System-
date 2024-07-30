import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "YOUR NEWS API KEY"
STOCK_API_KEY = "YOUR STOCK API KEY"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ACC_SID = "YOUR TWILLIO A/C SID"
AUTH_TOKEN = "YOUR TWILLIO AUTH-TOKEN"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

r = requests.get(STOCK_ENDPOINT, params=params)
stock_data = r.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stock_data.items()]

yesterday_stock_data = data_list[0]
yesterday_closing_value = yesterday_stock_data["4. close"]

day_bfr_yesterday_stock_data = data_list[1]
day_bfr_yesterday_closing_value = day_bfr_yesterday_stock_data["4. close"]

difference = float(yesterday_closing_value) - float(day_bfr_yesterday_closing_value)
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔽"

dif_percentage = round((difference/ float(yesterday_closing_value)) * 100)

if abs(dif_percentage) > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]


    formatted_articles = [f"{STOCK}: {up_down}{dif_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(ACC_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            from_="whatsapp: YOUR TWILLIO WHATSAPP NUMBER",
            body=article,
            to="whatsapp: YOUR WHATSAPP NUMBER"
        )

        print(message.status)

