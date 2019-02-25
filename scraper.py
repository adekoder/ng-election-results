from pprint import pprint
import json
import re
import os
import tweepy


from dotenv import load_dotenv
load_dotenv()



auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('SECRET_KEY'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))

api = tweepy.API(auth)



def fetch_tweet_from_inecnigeria():
    return api.user_timeline('inecnigeria', count=1000, tweet_mode='extended')

def analysis_election_result_tweet():
    tweets = fetch_tweet_from_inecnigeria()
    result_tweets = {}
    for tweet in tweets:
        tweet_text =  tweet.full_text
        if is_result_tweet(tweet_text):
            state = get_state(tweet_text)
            # Bug in getting state when it FCT (patched...)
            result_tweets[ state if state else 'FCT'] = tweet_text
    return result_tweets 


def is_result_tweet(text):
    regex = re.compile('Total No: Reg Voters:')
    result = regex.search(text)
    if result:
        return True
    return False

def collate_result(text):
    result_text = text.split('\n')
    party_result_texts = result_text[-6:]
    result_by_party = {}
    for party_result_text in party_result_texts:
        party, number_of_votes = party_result_text.split(':')
        result_by_party[party] = number_of_votes.strip()
    
    return result_by_party




def get_state(text):
    regex = re.compile('State')
    result = regex.search(text)
    if result:
        return text[: result.start()].split(':')[-1].strip()

def result_scrapper():
    result_by_states_text =  analysis_election_result_tweet()
    with  open('result.json', 'w+') as file:
        try:
            results = json.load(file)
        except:
            results = {}
        for state, text in result_by_states_text.items():
            if state not in results:
                results[state] = collate_result(text)
        json.dump(results, file, indent=4)


def get_results_data():
    with  open('result.json', 'r') as file:
        results = json.load(file)
    return results