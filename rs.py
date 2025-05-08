import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
from collections import Counter

fake = Faker()

# Đọc dữ liệu từ CSV
users = pd.read_csv('user.csv')
movies = pd.read_csv('movie.csv')
history = pd.read_csv('history.csv')
ratings = pd.read_csv('rating.csv')

def get_user_age(dob):
    """Tính tuổi của user từ ngày sinh"""
    today = datetime.now()
    dob = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_time_of_day(datetime_str):
    """Lấy thời gian trong ngày từ datetime"""
    hour = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 22:
        return 'evening'
    else:
        return 'night'

def get_season():
    """Xác định mùa hiện tại"""
    month = datetime.now().month
    if 3 <= month <= 5:
        return 'spring'
    elif 6 <= month <= 8:
        return 'summer'
    elif 9 <= month <= 11:
        return 'autumn'
    else:
        return 'winter'

def get_age_appropriate_genres(age):
    """Lấy thể loại phim phù hợp với độ tuổi"""
    if age < 18:
        return ['Animation', 'Family', 'Adventure', 'Comedy']
    else:
        return ['Horror', 'Thriller', 'Romance', 'Drama', 'Action']

def get_time_appropriate_genres(time_of_day):
    """Lấy thể loại phim phù hợp với thời gian xem"""
    if time_of_day == 'night':
        return ['Horror', 'Thriller', 'Romance']
    elif time_of_day == 'morning':
        return ['Comedy', 'Animation', 'Family']
    elif time_of_day == 'afternoon':
        return ['Action', 'Adventure', 'Drama']
    else:  # evening
        return ['Drama', 'Romance', 'Comedy']

def get_seasonal_genres(season):
    """Lấy thể loại phim phù hợp với mùa"""
    seasonal_genres = {
        'spring': ['Romance', 'Comedy', 'Family'],
        'summer': ['Action', 'Adventure', 'Comedy'],
        'autumn': ['Drama', 'Mystery', 'Thriller'],
        'winter': ['Family', 'Romance', 'Fantasy']
    }
    return seasonal_genres.get(season, [])

def calculate_trending_score(movie_id, days=30):
    """Tính điểm trending cho một phim"""
    now = datetime.now()
    
    # Lọc lịch sử xem trong N ngày gần đây
    recent_history = history[
        (history['movie_id'] == movie_id) & 
        (pd.to_datetime(history['started_at']) >= now - timedelta(days=days))
    ]
    
    # Lọc đánh giá trong N ngày gần đây
    recent_ratings = ratings[
        (ratings['movie_id'] == movie_id) & 
        (pd.to_datetime(ratings['created_at']) >= now - timedelta(days=days))
    ]
    
    # Tính điểm trending
    score = 0.0
    
    # 1. Điểm dựa trên số lượt xem gần đây (trọng số: 0.4)
    view_score = min(len(recent_history) / 100, 1.0)
    score += view_score * 0.4
    
    # 2. Điểm dựa trên số lượt đánh giá gần đây (trọng số: 0.3)
    rating_count_score = min(len(recent_ratings) / 50, 1.0)
    score += rating_count_score * 0.3
    
    # 3. Điểm dựa trên rating trung bình (trọng số: 0.2)
    if not recent_ratings.empty:
        avg_rating = recent_ratings['stars'].mean()
        rating_score = avg_rating / 5.0
        score += rating_score * 0.2
    
    # 4. Điểm dựa trên thời gian phát hành (trọng số: 0.1)
    movie = movies[movies['id'] == movie_id].iloc[0]
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
    days_since_release = (now - release_date).days
    recency_score = max(0, 1 - (days_since_release / 365))
    score += recency_score * 0.1
    
    return score

def calculate_user_activity_score(user_id):
    """Tính điểm hoạt động của user"""
    user_history = history[history['user_id'] == user_id]
    user_ratings = ratings[ratings['user_id'] == user_id]
    
    watch_score = min(len(user_history) / 50, 1.0)
    rating_score = min(len(user_ratings) / 30, 1.0)
    
    return (watch_score + rating_score) / 2

def analyze_user_preferences(user_id):
    """Phân tích sở thích của user"""
    # Lấy lịch sử xem phim của user
    user_history = history[history['user_id'] == user_id]
    user_ratings = ratings[ratings['user_id'] == user_id]
    
    # Phân tích thể loại phim yêu thích
    watched_movies = movies[movies['id'].isin(user_history['movie_id'])]
    all_genres = []
    for genres in watched_movies['genres']:
        all_genres.extend(genres.split('|'))
    genre_counter = Counter(all_genres)
    
    # Phân tích thời gian xem phim
    user_history['hour'] = pd.to_datetime(user_history['started_at']).dt.hour
    time_slots = {
        'Sáng (5h-12h)': len(user_history[user_history['hour'].between(5, 11)]),
        'Trưa (12h-17h)': len(user_history[user_history['hour'].between(12, 16)]),
        'Tối (17h-22h)': len(user_history[user_history['hour'].between(17, 21)]),
        'Đêm (22h-5h)': len(user_history[user_history['hour'].between(22, 23)]) + 
                        len(user_history[user_history['hour'].between(0, 4)])
    }
    
    # Phân tích rating
    rating_stats = user_ratings['stars'].describe()
    
    # Phân tích thiết bị xem phim
    device_counter = Counter(user_history['device'])
    
    # Phân tích quốc gia phim yêu thích
    country_counter = Counter(watched_movies['country'])
    
    return {
        'genres': genre_counter,
        'time_slots': time_slots,
        'rating_stats': rating_stats,
        'devices': device_counter,
        'countries': country_counter,
        'total_watched': len(user_history),
        'total_rated': len(user_ratings)
    }

def print_user_stats(user_id):
    """In thống kê chi tiết về user"""
    user = users[users['id'] == user_id].iloc[0]
    stats = analyze_user_preferences(user_id)
    
    print("\n=== THÔNG TIN CHI TIẾT USER ===")
    print(f"ID: {user['id']}")
    print(f"Tên: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Ngày sinh: {user['dob']}")
    print(f"Giới tính: {user['gender']}")
    print(f"Quốc gia: {user['country']}")
    
    print("\n=== THỐNG KÊ XEM PHIM ===")
    print(f"Tổng số phim đã xem: {stats['total_watched']}")
    print(f"Tổng số phim đã đánh giá: {stats['total_rated']}")
    
    print("\n=== THỂ LOẠI PHIM YÊU THÍCH ===")
    for genre, count in stats['genres'].most_common(5):
        print(f"- {genre}: {count} phim")
    
    print("\n=== THỜI GIAN XEM PHIM ===")
    for slot, count in stats['time_slots'].items():
        print(f"- {slot}: {count} lần")
    
    print("\n=== THIẾT BỊ XEM PHIM ===")
    for device, count in stats['devices'].most_common():
        print(f"- {device}: {count} lần")
    
    print("\n=== QUỐC GIA PHIM YÊU THÍCH ===")
    for country, count in stats['countries'].most_common(3):
        print(f"- {country}: {count} phim")
    
    print("\n=== THỐNG KÊ ĐÁNH GIÁ ===")
    print(f"Điểm trung bình: {stats['rating_stats']['mean']:.2f}")
    print(f"Điểm cao nhất: {stats['rating_stats']['max']:.2f}")
    print(f"Điểm thấp nhất: {stats['rating_stats']['min']:.2f}")
    print(f"Số lượng đánh giá: {stats['rating_stats']['count']:.0f}")

def recommend_movies(user_id, device, num_recommendations=20):
    # Lấy thông tin user
    user = users[users['id'] == user_id].iloc[0]
    user_age = get_user_age(user['dob'])
    user_country = user['country']
    user_gender = user['gender']
    current_time = datetime.now()
    current_season = get_season()
    
    # Tính điểm hoạt động của user
    user_activity_score = calculate_user_activity_score(user_id)
    
    # In thống kê user nếu là user cũ
    if user_activity_score >= 0.3:
        print_user_stats(user_id)
    else:
        print("\n=== PHÁT HIỆN USER MỚI - ÁP DỤNG CHIẾN LƯỢC COLD START ===")
    
    # Lấy lịch sử xem phim của user
    user_history = history[history['user_id'] == user_id]
    
    # Lọc lịch sử theo thiết bị
    device_history = user_history[user_history['device'] == device]
    
    # Lấy danh sách phim đã xem
    watched_movies = device_history['movie_id'].tolist()
    
    # Lấy danh sách phim chưa xem
    unwatched_movies = movies[~movies['id'].isin(watched_movies)].copy()
    
    # Tính điểm cho từng phim dựa trên nhiều yếu tố
    unwatched_movies['score'] = 0.0
    
    # Xử lý user mới (cold start)
    if user_activity_score < 0.3:
        # 1. Điểm dựa trên độ tuổi (trọng số: 0.25)
        age_genres = get_age_appropriate_genres(user_age)
        for genre in age_genres:
            unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.25
        
        # 2. Điểm dựa trên quốc gia (trọng số: 0.35)
        # Ưu tiên cao cho phim cùng quốc gia
        unwatched_movies.loc[unwatched_movies['country'] == user_country, 'score'] += 0.35
        
        # 3. Điểm dựa trên giới tính (trọng số: 0.15)
        if user_gender == 'Male':
            male_preferred_genres = ['Action', 'Adventure', 'Sci-Fi', 'Crime', 'Sport']
            for genre in male_preferred_genres:
                unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.03
        else:
            female_preferred_genres = ['Romance', 'Drama', 'Comedy', 'Family', 'Animation']
            for genre in female_preferred_genres:
                unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.03
        
        # 4. Điểm dựa trên thời gian xem (trọng số: 0.15)
        time_genres = get_time_appropriate_genres(get_time_of_day(current_time.strftime('%Y-%m-%d %H:%M:%S')))
        for genre in time_genres:
            unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.15
        
        # 5. Điểm dựa trên trending (trọng số: 0.1)
        unwatched_movies['trending_score'] = unwatched_movies['id'].apply(calculate_trending_score)
        unwatched_movies['score'] += unwatched_movies['trending_score'] * 0.1
        
        # Đảm bảo có ít nhất 3 phim cùng quốc gia trong top gợi ý
        same_country_movies = unwatched_movies[unwatched_movies['country'] == user_country].sort_values('score', ascending=False)
        if len(same_country_movies) > 0:
            # Lấy top 3 phim cùng quốc gia
            top_same_country = same_country_movies.head(3)
            # Lấy các phim khác
            other_movies = unwatched_movies[unwatched_movies['country'] != user_country].sort_values('score', ascending=False)
            # Kết hợp lại
            recommendations = pd.concat([top_same_country, other_movies.head(num_recommendations - 3)])
        else:
            recommendations = unwatched_movies.sort_values('score', ascending=False).head(num_recommendations)
        
    else:
        # Xử lý user cũ
        # 1. Điểm dựa trên độ tuổi (trọng số: 0.2)
        age_genres = get_age_appropriate_genres(user_age)
        for genre in age_genres:
            unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.2
        
        # 2. Điểm dựa trên quốc gia (trọng số: 0.25)
        unwatched_movies.loc[unwatched_movies['country'] == user_country, 'score'] += 0.25
        
        # 3. Điểm dựa trên thời gian xem (trọng số: 0.15)
        time_genres = get_time_appropriate_genres(get_time_of_day(current_time.strftime('%Y-%m-%d %H:%M:%S')))
        for genre in time_genres:
            unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.15
        
        # 4. Điểm dựa trên mùa (trọng số: 0.1)
        seasonal_genres = get_seasonal_genres(current_season)
        for genre in seasonal_genres:
            unwatched_movies.loc[unwatched_movies['genres'].str.contains(genre, na=False), 'score'] += 0.1
        
        # 5. Điểm dựa trên rating (trọng số: 0.2)
        user_ratings = ratings[ratings['user_id'] == user_id]
        if not user_ratings.empty:
            avg_rating = user_ratings['stars'].mean()
            movie_ratings = ratings.groupby('movie_id')['stars'].mean().reset_index()
            unwatched_movies = unwatched_movies.merge(movie_ratings, left_on='id', right_on='movie_id', how='left')
            unwatched_movies['stars'] = unwatched_movies['stars'].fillna(0)
            unwatched_movies['score'] += unwatched_movies['stars'] * 0.2
        
        # 6. Điểm dựa trên trending (trọng số: 0.1)
        unwatched_movies['trending_score'] = unwatched_movies['id'].apply(calculate_trending_score)
        unwatched_movies['score'] += unwatched_movies['trending_score'] * 0.1
        
        # Đảm bảo có ít nhất 2 phim cùng quốc gia trong top gợi ý
        same_country_movies = unwatched_movies[unwatched_movies['country'] == user_country].sort_values('score', ascending=False)
        if len(same_country_movies) > 0:
            # Lấy top 2 phim cùng quốc gia
            top_same_country = same_country_movies.head(2)
            # Lấy các phim khác
            other_movies = unwatched_movies[unwatched_movies['country'] != user_country].sort_values('score', ascending=False)
            # Kết hợp lại
            recommendations = pd.concat([top_same_country, other_movies.head(num_recommendations - 2)])
        else:
            recommendations = unwatched_movies.sort_values('score', ascending=False).head(num_recommendations)
    
    return recommendations, user, current_season

# Demo gợi ý phim
user_id = 32
device = 'TV'
recommendations, user, current_season = recommend_movies(user_id, device)

# In thông tin chi tiết
print("\n=== THÔNG TIN USER ===")
print(f"ID: {user['id']}")
print(f"Tên: {user['name']}")
print(f"Email: {user['email']}")
print(f"Ngày sinh: {user['dob']}")
print(f"Giới tính: {user['gender']}")
print(f"Quốc gia: {user['country']}")

print(f"\n=== DANH SÁCH PHIM GỢI Ý (Mùa {current_season}) ===")
for _, movie in recommendations.iterrows():
    print(f"\nPhim: {movie['name']}")
    print(f"Thể loại: {movie['genres']}")
    print(f"Quốc gia: {movie['country']}")
    print(f"Năm: {movie['year']}")
    print(f"Đạo diễn: {movie['director']}")
    print(f"Diễn viên: {movie['actors']}")
    print(f"Thời lượng: {movie['duration']} phút")
    if 'stars' in movie:
        print(f"Điểm đánh giá: {movie['stars']:.1f}")
    print(f"Điểm trending: {movie['trending_score']:.2f}")
    print(f"Điểm gợi ý: {movie['score']:.2f}")
    print("-" * 50)
