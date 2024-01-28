![ebert wordcloud](/images/wordcloud.png)

# Natural Ebert Processing

Roger Ebert's career as a film critic lasted decades and produced thousands of movie reviews, each including a number score (out of 4 stars) and a text segment of his own thoughts. This data science/machine learning project predicts the star rating of a film based on Ebert's review.




## Installation

Install all requirements for natural-ebert-processing with the following command:

```bash
  pip install requirements.txt
```
    
## Data

### Source Data

All data was scraped from [RogerEbert.com](https://www.rogerebert.com/) using BeautifulSoup. Each data sample for each review included the url, the title of the film, the author, the date that the review was published, the star rating of the film, and the text of the actual review.


### Data Acquisition

A list of URLs were scraped from the [RogerEbert.com](https://www.rogerebert.com/) site by iterating through [/reviews/page/](https://www.rogerebert.com/reviews/page/1) until no new URLs could be scraped. This yielded 14508 URLs. For each URL, a data sample was created by pulling the title of the film, the author, the date that the review was published, the star rating of the film, and the text of the actual review. All web scraping was done with requests and BeautifulSoup. Look under the 'Data Extraction' folder for code.


### Data Preprocessing