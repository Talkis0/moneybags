import requests
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from dateutil import rrule
from datetime import datetime
import sys

analyzer = SentimentIntensityAnalyzer()
def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    pos = scores['pos']
    if pos > 0.:
        return pos
    else:
        return 0.

# create preprocess_text function
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

apiKey = "7CygHrPQm47XFRVnA6n2jb354HB7RQMG"
term = "Boeing"
# begin_date yyyymmdd
begin_date = "20010101"
end_date = "20010111"
n_documents = 0
page_num = 0
pages_done = False
sentiment_data = defaultdict( lambda: [0., 0.] )
try:
    while not pages_done:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&api-key={}&begin_date={}&end_date={}?page={}".format( term, apiKey, begin_date, end_date, page_num )
        res = requests.get( url ).json()
        # res['response']['docs'][0]
        # dict_keys(['abstract', 'web_url', 'snippet', 'lead_paragraph', 'source', 'multimedia', 'headline', 'keywords', 'pub_date', 'document_type', 'news_desk', 'section_name', 'byline', 'type_of_material', '_id', 'word_count', 'uri'])
        documents = res['response']['docs']
        hits = res['response']['meta']['hits']
        print(page_num, hits)
        for i in range( len(documents) ):
            document = documents[i]
            pub_date = document['pub_date'].split('T')[0]
            description = ' '.join( [ document['abstract'], document['snippet'], document['lead_paragraph'] ] )
            description = preprocess_text( description )
            sentiment = get_sentiment( description )
            sentiment_data[pub_date][0] = sentiment_data[pub_date][0] + sentiment        
            sentiment_data[pub_date][1] = sentiment_data[pub_date][1] + 1        
        n_documents = n_documents + len(documents)
        page_num = page_num + 1
        if n_documents >= hits:
            pages_done = True
finally:
    with open( '{}.csv'.format(end_date), 'w' ) as outfile:
        print( 'Dates', 'Sentiment', 'Number of Articles', sep=',', file=outfile )
        for dt in rrule.rrule( rrule.DAILY,
                                dtstart=datetime.strptime(begin_date, '%Y%m%d'),
                                until=datetime.strptime(end_date, '%Y%m%d') ):
            date = dt.strftime('%Y-%m-%d')
            print( date, sentiment_data[date][0], sentiment_data[date][1], sep=',', file=outfile )