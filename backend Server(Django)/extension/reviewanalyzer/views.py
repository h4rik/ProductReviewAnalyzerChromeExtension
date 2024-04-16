from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


VOCAB_SIZE = 10000
MAX_LEN = 250
model_path = r'C:\Users\hp\OneDrive\Desktop\major API\extension\reviewanalyzer\sentiment_analysis.keras'
tokenizer_path = r'C:\Users\hp\OneDrive\Desktop\major API\extension\reviewanalyzer\tokenizer.pickle'

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait':1})
    soup = BeautifulSoup(r.text, 'html.parser')
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
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip()
                }
                reviewlist.append(review)
        except Exception as e:
            print(f"Error processing reviews: {e}")

        if len(reviewlist) == prev_review_count:
            break

        prev_review_count = len(reviewlist)

    print(f'Total reviews extracted: {len(reviewlist)}')  # Print total number of reviews extracted
    return reviewlist

def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

def load_sentiment_model(model_path):
    model = load_model(model_path)
    return model

def encode_text(tokenizer, text_or_dict):   
    if isinstance(text_or_dict, dict):
        text = text_or_dict.get('body', '')
    else:
        text = text_or_dict

    tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
    encoded = tokenizer.texts_to_sequences([tokens])
    padded = tf.keras.preprocessing.sequence.pad_sequences(encoded, maxlen=MAX_LEN, padding='post')
    return padded

def analyze_comments(comments):
    print("Analyzing comments:", comments)
    tokenizer = load_tokenizer(tokenizer_path)
    model = load_sentiment_model(model_path)
    positive_count = 0
    negative_count = 0

    for comment in comments:
        encoded_comment = encode_text(tokenizer, comment)
        prediction = np.argmax(model.predict(encoded_comment))

        if prediction == 0:
            negative_count += 1
        else:
            positive_count += 1

    total_comments = len(comments)
    positive_percentage = (positive_count / total_comments) * 100
    negative_percentage = (negative_count / total_comments) * 100
    print(positive_percentage)
    print(negative_percentage)
    return positive_percentage, negative_percentage

@csrf_exempt
@require_POST
def analyze_reviews(request):
    data = json.loads(request.body)
    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'Invalid request, URL not provided'}, status=400)

    reviews = get_reviews(url)
    positive_percentage, negative_percentage = analyze_comments(reviews)
    return JsonResponse({'positive_percentage': positive_percentage, 'negative_percentage': negative_percentage})


def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        product_name = data.get('product_name')
        subject = 'Subscription Confirmation'
        message = f'Thank you for subscribing to price alerts for the product: {product_name}. You will be notified when the price gets reduced.'
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return JsonResponse({'message': 'Email sent successfully'})
    return JsonResponse({'message': 'Invalid request method'})

def subscribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        price = data['price']
        print('Received subscription request:', email, price)
        # Process subscription request
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
