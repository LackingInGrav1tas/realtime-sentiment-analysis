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

It finds new tweets fitting the query and checks if they contain one of [these negative connotation words](https://ptrckprry.com/course/ssd/data/negative-words.txt). Notably, this method is context free due to performance so judgements can be very inaccurate.



![image](https://user-images.githubusercontent.com/42680395/150697284-ec2a7767-3664-4257-8414-d30245cb1958.png)
