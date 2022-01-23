import json, requests, nltk, pickle, sys
import matplotlib.pyplot as plt

neg_words = pickle.loads(open("wordlist.bin", "rb").read())

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

def negative(source):
    for word in source:
        if word in neg_words: return True
    return False

def shorten(num):
    s = str(num)
    if len(s) >= 5: return s[0:5]
    else:
        for i in range(5-len(s)): s += '0'
        return s

LABELS = ["Positive", "Negative"]
COLORS = ["blue", "red"]

def main(args):
    try:
        # parsing refresh rate
        refresh_rate = 4
        try: 
            refresh_rate = float(args[2])
        except: pass

        try:
            print(f"tweet sentiment analysis - \"{args[1]}\"\n")
        except: # user did not add an arguement
            print("correct format: app.py <query> [<refresh-rate>]")
            exit(1)

        # setting up plot
        title = f"Tweet Sentiment Analysis - \"{args[1]}\""
        plt.figure(num=title)
        plt.title(title)

        query_params = {'query': f'"{args[1]}" (-is:retweet)'}
        pos = 0
        neg = 0
        prev = None
        while True:
            print(f"\rpos: {pos} neg: {neg}  ({shorten(neg/(neg+pos if neg+pos != 0 else 1))}% negative)", end="")
            
            json_response = connect_to_endpoint(search_url, query_params)
            data = json_response["data"]
            if prev in data:
                plt.pause(0.00001) # so it doesn't get detected as unresponsive
                continue
            for tweet in data:
                if (negative(nltk.word_tokenize(tweet['text'].lower()))): neg += 1
                else: pos += 1

            # updating pie chart
            plt.clf()
            plt.text(1, 1, f"Sample Size: {pos+neg}", fontsize="small")
            plt.title(title)
            plt.pie([pos, neg], labels=LABELS, colors=COLORS, autopct=lambda v: shorten(v))
            plt.pause(refresh_rate)

            # ensuring new data
            prev = data[0]

    except KeyboardInterrupt:
        print("\nexiting...")
    except KeyError:
        print("\nexiting, no data exists...")
    except:
        print("\nexiting due to error...")

if __name__ == "__main__":
    main(sys.argv)