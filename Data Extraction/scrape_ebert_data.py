from bs4 import BeautifulSoup

import requests

import time
import pickle

def extract_page_reviews_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    reviews_list = soup.find_all(class_="review-stack--poster")
    return reviews_list

def get_review_urls(review_items):
    reviews_links_list = [r['href'] for r in review_items]
    return reviews_links_list

def count_stars(star_div):
    return len(star_div.find_all(class_="icon-star-full")) + 0.5 * len(star_div.find_all(class_="icon-star-half"))

def extract_ebert_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Title
    title_divs = [t.text.strip() for t in soup.find_all(class_="page-content--title")]
    assert(len(title_divs) == 1)
    title = title_divs[0]
    
    # Author
    author_divs = [t.text.strip() for t in soup.find_all(class_="byline")]
    assert(len(author_divs) == 1)
    author = author_divs[0]
    
    # Stars
    star_divs = soup.find_all(class_="page-content--star-rating")
    assert(len(star_divs) == 1)
    star_div = star_divs[0]

    star_count = count_stars(star_div)
    
    # Time
    time_divs = soup.find_all("time")
    assert(len(time_divs) == 1)
    time_div = time_divs[0]

    time_info = time_div.text.strip()
    
    # Content
    content_paragraphs = []
    content_divs_tmp = soup.find_all(class_="page-content--block_editor-content")
    for c in content_divs_tmp:
        content_paragraphs.extend([t.text.strip() for t in c.find_all(["p", "li"])])
        
    return title, author, time_info, star_count, content_paragraphs


page_index = 1
review_links = {}
review_count = len(review_links)

while True:
    review_count = len(review_links)
    url = f"https://www.rogerebert.com/reviews/page/{page_index}"
    tmp_urls = get_review_urls(extract_page_reviews_list(url))
    
    # Each page includes 4 recommended reviews
    if len(tmp_urls) < 5:
        break
    
    review_links[page_index] = tmp_urls
    
    with open('raw_urls.pkl', 'wb') as f:
        pickle.dump(review_links, f, pickle.HIGHEST_PROTOCOL)
        
    page_index += 1
    
    print(f"page_index {page_index} and review_links {len(review_links.keys())}",  end='\r')
    
with open('raw_urls.pkl', 'wb') as f:
    pickle.load(f, review_links)
    
review_data = {}

for k in review_links.keys():
    for url in review_links[k]:
        if url not in review_data:
            review_data[url] = extract_ebert_info("https://www.rogerebert.com" + url)
    
    with open('raw_reviews.pkl', 'wb') as f:
        pickle.dump(review_data, f, pickle.HIGHEST_PROTOCOL)
        
    print(f"review_link {k} and current size {len(review_data.keys())}",  end='\r')
