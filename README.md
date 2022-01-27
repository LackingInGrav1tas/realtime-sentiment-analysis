# realtime-sentiment-analysis #

Realtime sentiment analysis using the Twitter API 

## How to use ##

1. Clone the repository
2. Create a file called ```twitter_api_key.json```, which contains your api key, secret, and bearer token:
```Javascript
{
    "key": ...,
    "secret": ...,
    "bearer": ...,
}
```
3. Run the file with the format: ```python analysis.py <subject> [<refresh-rate>]```

## How does it work?

It finds new tweets fitting the query and calculates their polarity using nltk's vader sentiment analysis. It then adds each value to it's corresponding category (Negative, Positive).



![image](https://user-images.githubusercontent.com/42680395/151404573-350c7dab-c3ad-4f20-8376-baf40fda4eb7.png)