import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

NUM_USERS = 30
NUM_MOVIES = 1000
NUM_HISTORY = 2000
NUM_RATINGS = 1500

# 1. Sinh user.csv
with open('user.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'email', 'password_hash', 'name', 'dob', 'gender', 'country', 'google_id', 'created_at', 'updated_at'])
    for i in range(1, NUM_USERS + 1):
        name = fake.first_name()
        email = f"{name.lower()}{i}@gmail.com"
        password_hash = fake.sha256()
        dob = fake.date_of_birth(minimum_age=16, maximum_age=40)
        gender = random.choice(['Male', 'Female'])
        country = fake.country()
        google_id = '' if random.random() < 0.7 else fake.uuid4()
        now = fake.date_time_this_year()
        writer.writerow([i, email, password_hash, name, dob, gender, country, google_id, now, now])

# 2. Sinh movie.csv
genres_list = ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Romance', 'Animation', 'Crime', 'Adventure', 'Fantasy', 'Horror', 'Mystery', 'Biography', 'Sport']
with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'description', 'genres', 'country', 'year', 'director', 'actors', 'poster_url', 'trailer_url', 'duration', 'release_date', 'created_at', 'updated_at'])
    for i in range(1, NUM_MOVIES + 1):
        name = fake.sentence(nb_words=3).replace(',', '')
        description = fake.text(max_nb_chars=80)
        genres = '|'.join(random.sample(genres_list, k=random.randint(1, 3)))
        country = fake.country()
        year = random.randint(1980, 2024)
        director = fake.name()
        actors = ', '.join([fake.name() for _ in range(2)])
        poster_url = ''
        trailer_url = ''
        duration = random.randint(80, 180)
        release_date = f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        now = fake.date_time_this_year()
        writer.writerow([i, name, description, genres, country, year, director, actors, poster_url, trailer_url, duration, release_date, now, now])

# 3. Sinh history.csv
with open('history.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'user_id', 'movie_id', 'started_at', 'finished_at', 'status', 'device'])
    for i in range(1, NUM_HISTORY + 1):
        user_id = random.randint(1, NUM_USERS)
        movie_id = random.randint(1, NUM_MOVIES)
        start = fake.date_time_this_year()
        duration = timedelta(minutes=random.randint(60, 180))
        finish = start + duration
        status = random.choice(['watched', 'watching'])
        device = random.choice(['TV', 'Mobile', 'Desktop', 'Tablet'])
        writer.writerow([i, user_id, movie_id, start, finish, status, device])

# 4. Sinh rating.csv
with open('rating.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'user_id', 'movie_id', 'stars', 'content', 'created_at'])
    used = set()
    for i in range(1, NUM_RATINGS + 1):
        while True:
            user_id = random.randint(1, NUM_USERS)
            movie_id = random.randint(1, NUM_MOVIES)
            if (user_id, movie_id) not in used:
                used.add((user_id, movie_id))
                break
        stars = random.randint(1, 5)
        content = fake.sentence(nb_words=8)
        created_at = fake.date_time_this_year()
        writer.writerow([i, user_id, movie_id, stars, content, created_at])

print("Đã sinh dữ liệu user.csv, movie.csv, history.csv, rating.csv!")
