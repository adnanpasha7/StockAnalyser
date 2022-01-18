import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "HX103TTTEQBD4EQP"
NEWS_API_KEY = "3e2173cade4b46dfa49f9c6f8eed34a6"
TWILIO_SID = "YOUR_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN_FROM_TWILIO"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily

stock_param = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API_KEY,
}


response = requests.get(STOCK_ENDPOINT, params=stock_param)

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterdays_data = data_list[0]
yesterdays_closing_price = yesterdays_data["4. close"]
print(yesterdays_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#Find the difference between 1 and 2. 
difference = float(yesterdays_closing_price) - float(day_before_yesterday_closing_price)
print(difference)
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔽"
#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterdays_closing_price)) * 100)
print(diff_percent)

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if diff_percent > 1:
    news_params = {
        "apiKey" : NEWS_API_KEY,
        "qInTitle" : COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]
    print(articles)
#Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:4]
    # print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}.\n Brief: {article['description']}"for article in three_articles]
# Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, AUTH_TOKEN)

    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_="YOUR_TWILIO'S_PHONE_NUMBER",
            to="YOUR_PHONR_NUMBER",
        )


