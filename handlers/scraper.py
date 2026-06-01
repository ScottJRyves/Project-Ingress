# References
# Adapted from https://www.youtube.com/watch?v=8dTpNajxaH0 by Alex The Analyst.
# https://www.geeksforgeeks.org/python/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
# https://medium.com/@eskandar.sahel/exploring-feature-extraction-techniques-for-natural-language-processing-46052ee6514
# https://www.johnsnowlabs.com/the-experts-guide-to-keyword-extraction-from-texts-with-spark-nlp-and-python/
# https://www.youtube.com/watch?v=DCaKj3eIrro
# https://pypi.org/project/tldextract/
# https://github.com/AndyTheFactory/newspaper4k
# https://newspaper4k.readthedocs.io/en/latest/

import newspaper
from tldextract import tldextract


def article_extraction(url):
    try:
        # Extracting the article data using newspaper4k fork here
        # This downloads the article and parses it, so it is much faster than newspaper3k
        # Also it has better support for different websites
        article_data = newspaper.article(url)
        return article_data
    except Exception as e:
        return None


def get_domain(url):
    # Extracting the domain name from the URL using tldextract
    domain = tldextract.extract(url)
    # the dictionary domain holds the domain name, so we target that, also I added captialize.
    return domain.domain.capitalize()


def parse_news(url):
    # Setting up a dictionary to store the data
    # Decided to set most of the fields to None to standardise the data
    # and make it easier to find any missing data
    data = {
        "URL": url,
        "Source": None,
        "Title": None,
        "Author": None,
        "Published Date": None,
        "Main Content": None,
        "Data Quality": "Failed",
        "Error Message": None
    }

    try:
        # Extracting the article data using newspaper4k fork here
        article_data = article_extraction(url)

        # Boolean to say that the data is complete until it isn't.
        full_data = True
        # List of fields that we want to check for
        data_fields = ['Source', 'Title', 'Author', 'Published Date', 'Main Content']
        # List to store any missing data fields
        missing_data = []

        # So if there is article data, then run this
        if article_data:
            # Grab the domain
            data['Source'] = get_domain(url)
            # Grab the Title, Author, Publish Date and Main Content
            data['Title'] = article_data.title
            # If there is an author, then grab the first one in the list as Newspaper4k returns a list of authors
            # Encountered crashes if there was no author, so added this check to make sure it doesn't break the app
            if article_data.authors:
                data['Author'] = str(article_data.authors[0])
            data['Published Date'] = article_data.publish_date
            data['Main Content'] = article_data.text

            # Check if all the fields are not None
            for fields in data_fields:
                # If any of the fields are None, then set full_data to False
                if not data[fields]:
                    missing_data.append(fields)
                    full_data = False

            # If full_data is True, then the data is complete, otherwise it is Partial
            if full_data:
                data['Data Quality'] = "Complete"
            elif not full_data:
                data['Data Quality'] = "Partial"
                # Joining the missing data fields into a string
                data['Error Message'] = "Missing data: " + ", ".join(missing_data)
        else:
            # If nothing is returned, then the data failed
            data['Data Quality'] = "Failed"
            data['Error Message'] = "Article extraction returned nothing"

    # If there is any error during the process, we can catch it and store the error message in the data dictionary
    # To be used later on to display the error message on the app page
    except Exception as e:
        data['Error Message'] = str(e)

    return data

# OLD SOUP SETUP (Started failing on BBC News for Author so had to switch to newspaper4k fork)

# def article_extractor(url):
#     try:
#         # Extracting the article using newspaper3k
#         article = Article(url)
#         # Downloading the article and parsing it
#         article.download()
#         # Parsing the article
#         article.parse()
#         # Extracting the article text
#         return article.text
#     except Exception as e:
#         return None
#
#
#

# def parse_news(url):
#     # Setting up a dictionary to store the data
#     data = {
#         "URL": url,
#         "Source": "Unknown",
#         "Title": None,
#         "Author": "Unknown",
#         "Published Date": None,
#         "Main Content": None,
#         "Data Quality": "Failed",
#         "Error Message": None
#     }
#
#     try:
#         response = requests.get(url)
#         # Setup Soup with content & text
#         soup_content = BeautifulSoup(response.content, 'html.parser')
#         soup_text = BeautifulSoup(response.text, 'html.parser')
#
#         # If soupcontent has meta tags, then we can get the data from there
#
#         # If inside soup_content we have the site name
#         if soup_content.find("meta", property="og:site_name"):
#             data["Source"] = soup_content.find("meta", property="og:site_name").get("content").title()
#
#         # If we get the title of the article
#         if soup_content.find("meta", property="og:title"):
#             data["Title"] = soup_content.find("meta", property="og:title").get("content")
#
#         # And if we get the author of the article
#         if soup_content.find("meta", property="article:author"):
#             data["Author"] = soup_content.find("meta", property="article:author").get("content")
#
#         # Here we can get the main content of the article using newspaper3k
#         data["Main Content"] = article_extractor(url)
#
#         # If title and main content are not None, then we can say that the data is complete
#         if data["Title"] and data["Main Content"]:
#             data["Data Quality"] = "Complete"
#         # Else the data is incomplete
#         else:
#             data["Data Quality"] = "Failed"
#             data["Error Message"] = "Could not identify Title or Body content"
#     # If there is any error during the process, we can catch it and store the error message in the data dictionary
#     except Exception as e:
#         # Capture the error message and store it in the data dictionary
#         data["Error Message"] = str(e)
#
#     return data
