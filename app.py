# Implemented Flask GUI following these tutorials, but did not use Vue.js as planned
# GET/POST requests also were learnt from the following
# References:
# https://www.youtube.com/watch?v=_YeN69XoqqU
# https://www.youtube.com/watch?v=9MHYHgh4jYc
# https://stackoverflow.com/questions/2688079/how-to-iterate-over-the-first-n-elements-of-a-list
# https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python

from flask import Flask
from flask import render_template
from flask import request
from dotenv import load_dotenv

from handlers.helpers import cleaning_url_list
from handlers.scraper import parse_news
from handlers.analysis import pos_tagging_analysis
from handlers.analysis import data_analysis
from handlers.analysis import extract_tfidf_keywords

import csv
import os
import time

load_dotenv('./.flaskenv')

# Need to create an instance of the Flask class
app = Flask(__name__)


# GUI
# First is the landing page.
@app.route('/')
def index():
    # returns the index page, which is the first page of the app
    return render_template('index.html')


# Second is the application page, where the tool is used
@app.route('/app', methods=['GET', 'POST'])
def application():
    # Need to set results to an empty dictionary
    total_time = 0
    results = []

    # We get the POST from the form action on the HTML page, so then it can execute
    if request.method == 'POST':

        # We GET the urls from the form, so inside the textarea
        urls = request.form.get('urls')
        # We now execute the cleaning_url_list function to clean the urls, for example, removing duplicates, or removing whitespace
        url_list = cleaning_url_list(urls)

        # Added a timer to measure the time taken to run the tool
        start_time = time.time()

        # Now inside this loop, we loop through each url inside url_list
        # Added a limit of 5 urls to keep the tool aligned with Ethics
        for url in url_list[:5]:

            # Added a delay of 2 seconds as to not overload the server with requests
            time.sleep(2)

            # Parsing all the data from the url, through the parse_news function,
            # which will return a dictionary with all the data we need, such as title, main content, source, etc.
            data = parse_news(url)

            # If the data is not failed then we can go through analysis, if it does it skips all of this
            if data['Data Quality'] != 'Failed':
                # Part of speech tagging, sentiment analysis, and TF-IDF extraction

                # Parts of speech basically takes the words and identifies what part of speech
                # they are, such as noun, verb, adjective, etc.
                pos_words = pos_tagging_analysis(data)
                # Sentiment analysis is basically taking the words and identifying
                # if they are positive, negative, or neutral, and giving a score to it
                sentiment_decision, sentiment_score = data_analysis(pos_words)
                # TF-IDF extraction is basically taking the words and identifying
                # which words are the most important in the text, and giving them a score,
                # and then we can take the top n keywords.
                top_keywords = extract_tfidf_keywords(data['Main Content'])

                # Then we append the results to the results list, which will be displayed on the app page
                results.append({
                    'url': url,
                    'source': data['Source'],
                    'title': data['Title'],
                    'author': data['Author'],
                    'published_date': data['Published Date'],
                    'main_content': data['Main Content'],
                    'sentiment': sentiment_decision,
                    # Rounding the score to 3 decimal places
                    'score': round(sentiment_score, 3),
                    # Joining the top keywords into a string, separated by commas
                    'keywords': ", ".join(top_keywords),
                    'data_quality': data['Data Quality'],
                    'error': data['Error Message']
                })
            else:
                # Else if it failed then we append the results to the results list, which will be displayed on the app page
                # Also so it doesn't break the app.
                results.append({
                    'url': url,
                    'source': 'N/A',
                    'title': 'N/A',
                    'author': 'N/A',
                    'published_date': 'N/A',
                    'main_content': 'N/A',
                    'sentiment': 'N/A',
                    'score': 'N/A',
                    'keywords': 'N/A',
                    'data_quality': 'Failed',
                    'error': data['Error Message']  # Can get the error message to display here from the str(e).
                })

        # End timer
        end_time = time.time()
        # Total time taken to run the tool and rounded to 2 decimal places
        total_time = round(end_time - start_time, 2)

        # Reference
        # https://www.geeksforgeeks.org/python/writing-csv-files-in-python/
        # https://www.scaler.com/topics/dict-to-csv-python/

        # Writing the results to a CSV file
        csv_path = os.path.join('static', 'dataset.csv')
        # Open the path to write to the CSV file, and we set newline to '' to avoid adding extra newlines
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # Writing the results to the CSV file
            # We use the DictWriter to write the results to the CSV file
            # We use the fieldnames from the first result in the results list which is all the dict keys
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # We return the app.html file, which is the main page of the app with the results
    # We pass the results to the app.html file so then it can display the results
    return render_template('app.html', results=results, total_time=total_time)


# Initalising the app
if __name__ == '__main__':
    app.run()
