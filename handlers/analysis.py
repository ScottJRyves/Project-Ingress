# References
# Adapted from https://www.youtube.com/watch?v=8dTpNajxaH0 by Alex The Analyst.
# https://www.geeksforgeeks.org/python/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
# https://medium.com/@eskandar.sahel/exploring-feature-extraction-techniques-for-natural-language-processing-46052ee6514
# https://www.johnsnowlabs.com/the-experts-guide-to-keyword-extraction-from-texts-with-spark-nlp-and-python/
# https://www.youtube.com/watch?v=DCaKj3eIrro
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
# https://www.kaggle.com/code/rowhitswami/keywords-extraction-using-tf-idf-method
# https://www.youtube.com/watch?v=i74DVqMsRWY
# https://stackoverflow.com/questions/26826002/adding-words-to-stop-words-list-in-tfidfvectorizer-in-sklearn

from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from handlers.helpers import custom_stopwords

# NLTK data
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


# Part-of-Speech Tagging
# This is the main function that will be used to extract keywords from the text content
# It will take the Title and Main Content
def pos_tagging_analysis(data):
    title = data["Title"]
    content = data["Main Content"]

    # Combine the title and content into a single string (text)
    text = title + " " + content

    # Tokenize the text into words and tags
    words = word_tokenize(text)
    # Then tag the words to get the part-of-speech (POS) tags
    tagged_words = pos_tag(words)

    # Add the words into a keyword list
    keywords = []

    # Now to iterate through the tagged words
    for word, tag in tagged_words:
        # Then if the tag starts with:
        # "VB" is a verb, "JJ" is an adjective, "RB" is an adverb,
        # then add it to the list of keywords
        if tag.startswith("VB") or tag.startswith("JJ") or tag.startswith("RB"):
            keywords.append(word)
    return keywords


# Sentiment Analysis
def data_analysis(keywords):
    # Combine the keywords from the POS tagging into a single string (content)
    content = " ".join(keywords)

    # Blob is the library that will take the content and analyse it
    blob = TextBlob(content)
    # Sentiment score is a value between -1 and 1, where 1 is positive and -1 is negative
    sentiment_score = blob.sentiment.polarity

    # Added the weighting to the sentiment score, so that it is more accurate
    if sentiment_score > 0.05:
        sentiment_decision = "Positive"
    elif sentiment_score < -0.05:
        sentiment_decision = "Negative"
    else:
        sentiment_decision = "Neutral"

    return sentiment_decision, sentiment_score


# TF-IDF Keyword Extraction
def extract_tfidf_keywords(content):
    # Had to make custom stopwords to remove the words that were not useful here
    custom_stop_words = custom_stopwords()
    # Standard stopwords from the NLTK library
    standard_stop_words = stopwords.words('english')
    # Combining the two lists of stop words to create a final list of stop words
    # that's used in the TF-IDF vectorizer
    final_stop_words = standard_stop_words + list(custom_stop_words)

    tfidf = TfidfVectorizer(lowercase=True,  # Convert all words to lowercase
                            max_features=5,  # Only consider the top 5 most common words
                            ngram_range=(1, 2),  # ngram range of 1 to 2 which basically takes 1 to 2 words into account
                            sublinear_tf=True,
                            # instead of term frequency multiplied by inverse document frequency, use sublinear term frequency (x5 vs 0.5)
                            stop_words=final_stop_words  # Use the final list of stop words
                            )
    tfidf.fit_transform([content])  # Fit the vectorizer to the content
    keywords = tfidf.get_feature_names_out()  # Get the feature names which are the keywords
    return keywords
