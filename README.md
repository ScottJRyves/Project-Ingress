# Project Ingress: Automated News Data Pipeline

Project Ingress is a Python and Flask application that extracts online news articles and transforms them into structured CSV datasets for further analysis and machine-learning workflows.

The project was developed as my final-year computing artefact at Abertay University. Its purpose is to reduce the manual effort involved in collecting, cleaning and preparing online news data.

## Key Features

- Accepts online news-article URLs through a Flask web interface
- Extracts article information such as title, source, author, publication date and content
- Cleans and prepares raw article text
- Applies Natural Language Processing techniques
- Generates structured CSV output
- Flags incomplete or failed data entries rather than silently discarding them

## NLP Techniques

The application uses several Natural Language Processing techniques:

- **Text pre-processing:** cleans article content before analysis
- **TF-IDF keyword extraction:** identifies prominent keywords and phrases within each article
- **Sentiment analysis:** estimates the sentiment of article text
- **Part-of-speech filtering:** improves sentiment analysis by focusing on selected word types

## Technologies Used

- Python
- Flask
- Newspaper4k
- BeautifulSoup
- NLTK
- TextBlob
- scikit-learn
- pandas
- HTML and CSS

## How It Works

1. The user submits one or more article URLs through the Flask interface.
2. The application extracts article content and metadata.
3. The text is cleaned and prepared for analysis.
4. NLP techniques are applied to generate sentiment scores and keywords.
5. The results are exported as a structured CSV dataset.

## Screenshots

Add screenshots of the application interface and example CSV output here.

## Example Output

Add a small example CSV file inside a `sample-output` folder.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/ScottJRyves/Project-Ingress.git
cd Project-Ingress
