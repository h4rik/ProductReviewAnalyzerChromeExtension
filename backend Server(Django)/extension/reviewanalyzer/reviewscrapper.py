import requests
from bs4 import BeautifulSoup

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url})
    soup = BeautifulSoup(r.text, 'html.parser')
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #r = requests.get(url, headers=headers, params={'wait': 1})
    #soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(url):
    reviewlist = []
    prev_review_count = 0

    for x in range(1, 50):
        page_url = f'{url}&pageNumber={x}'
        print(f'Fetching reviews from URL: {page_url}')
        soup = get_soup(page_url)
        print(f'Getting page: {x}')
        reviews = soup.find_all('div', {'data-hook': 'review'})
        if not reviews:
            break

        try:
            for item in reviews:
                review = {
                    #'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                    #'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip()
                }
                reviewlist.append(review)
        except Exception as e:
            print(f"Error processing reviews: {e}")

        if len(reviewlist) == prev_review_count:
            break

        prev_review_count = len(reviewlist)

    print(f'Total reviews extracted: {len(reviewlist)}')  # Print total number of reviews extracted
    #print(reviewlist)
    return reviewlist



# Function to call from other file
def fetch_reviews(url):
    reviews = get_reviews(url)
    return reviews

'''
if __name__ == '__main__':
    # Example usage
    url = 'https://www.amazon.in/Puma-Dazzler-Black-Puma-Silver-Sneaker/product-reviews/B09RGJCVW6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews'
    reviews = fetch_reviews(url)
    print(f'Total reviews extracted: {len(reviews)}')
    print(reviews)
'''
