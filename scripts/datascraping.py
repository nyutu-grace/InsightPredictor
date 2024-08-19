from bs4 import BeautifulSoup
import requests
import csv
import os

url = 'https://www.airlinequality.com/airline-reviews/british-airways'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

reviews = []

review_articles = soup.find_all('article', class_='comp_media-review-rated list-item media position-content review-900630')
    
for article in review_articles:
    # Extracting review details
    title = article.find('h2', class_='text_header').text.strip()
    name = article.find('span', itemprop='name').text.strip()
    date = article.find('time', itemprop='datePublished').text.strip()
    review_body = article.find('div', class_='text_content ', itemprop='reviewBody').text.strip()
    
    # Extract rating
    rating = article.find('span', itemprop='ratingValue').text.strip()

    # Extracting additional details (Type of Traveller, Seat Type, etc.)
    table = article.find('table', class_='review-ratings')
    rows = table.find_all('tr')
    
    type_of_traveller = rows[0].find_all('td', class_='review-value')[0].text.strip()
    seat_type = rows[0].find_all('td', class_='review-value')[1].text.strip()
    
    # Extract the star ratings
    stars = table.find('td', class_='review-rating-stars').find_all('span', class_='star fill')
    star_rating = len(stars)  # Count the number of filled stars
    
    # Append the extracted data to reviews list
    reviews.append({
        'title': title,
        'name': name,
        'date': date,
        'review_body': review_body,
        'rating': rating,
        'type_of_traveller': type_of_traveller,
        'seat_type': seat_type,
        'star_rating': star_rating
    })

    # Ensure the data directory exists
    os.makedirs('../data', exist_ok=True)

    # Save the data to a CSV file in the 'data' folder
    csv_file_path = os.path.join('../data', 'reviews.csv')

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'name', 'date', 'review_body', 'rating', 'type_of_traveller', 'seat_type', 'star_rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for review in reviews:
            writer.writerow(review)

    print(f'Data successfully written to {csv_file_path}')