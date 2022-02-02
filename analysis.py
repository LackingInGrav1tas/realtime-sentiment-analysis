import json, requests, sys
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def get_api_keys():
    """Gets API keys from file, returns (key, secret, bearer)"""
    f = open("twitter_api_key.json", "r")
    parsed = json.loads(f.read())
    return (parsed["key"], parsed["secret"], parsed["bearer"])

keys = get_api_keys()

def bearer_oauth(r):
    """ Method required by bearer token authentication. """
    r.headers["Authorization"] = f"Bearer {keys[2]}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

search_url = "https://api.twitter.com/2/tweets/search/recent"

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def analyze(source):
    scores = sia.polarity_scores(source)
    return (scores["neg"], scores["neu"], scores["pos"])

def shorten(num):
    s = str(num)
    if len(s) >= 5: return s[0:5]
    else:
        for i in range(5-len(s)): s += '0'
        return s

LABELS = ["Negative", "Positive"]
COLORS = ["red", "blue"]

def main(args):
    try:
        # parsing refresh rate
        refresh_rate = 4
        try: refresh_rate = float(args[2])
        except: pass

        try:
            print(f"tweet sentiment analysis - \"{args[1]}\"\n")
        except: # user did not add an arguement
            print("correct format: app.py <query> [<refresh-rate>]")
            exit(1)

        # setting up plot
        title = f"Tweet Sentiment Analysis - \"{args[1]}\""
        plt.rcParams["font.family"] = "Segoe UI" # old twitter font
        plt.rcParams["font.weight"] = 600
        plt.figure(num=title).patch.set_facecolor("#1DA1F2")
        plt.title(title, color="white", weight=700)

        query_params = {'query': f'"{args[1]}" (-is:retweet)'}
        pos = 0
        neg = 0
        neu = 0
        prev = None
        size = 0
        while True:
            print(f"\rpos: {pos} neg: {neg} neu: {neu}  ({shorten(neg/(neg+pos if neg+pos+neu != 0 else 1))}% negative)", end="                    ")
            
            json_response = connect_to_endpoint(search_url, query_params)
            data = json_response["data"]
            if prev in data:
                plt.pause(0.00001) # so it doesn't get detected as unresponsive
                continue
            for tweet in data:
                size += 1
                analysis = analyze(tweet["text"])
                neg += analysis[0]
                # neu += analysis[1]
                pos += analysis[2]

            # updating pie chart
            plt.clf()
            plt.text(1, 1, f"Sample Size: {size}", fontsize="small", color="white")
            plt.title(title, color="white", weight=700)
            plt.pie([neg, pos], labels=LABELS, colors=COLORS, autopct=lambda v: shorten(v))
            plt.pause(refresh_rate)

            # ensuring new data
            prev = data[0]

    except KeyboardInterrupt:
        print("\nexiting...")
    except KeyError:
        print("\nexiting, no data exists...")

if __name__ == "__main__":
    main(sys.argv)