import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()

# Đọc dữ liệu từ CSV
movies = pd.read_csv('movie.csv')
ratings = pd.read_csv('rating.csv')

def generate_trending_data(num_trending=50):
    """
    Sinh dữ liệu trending cho phim dựa trên:
    - Rating trung bình
    - Số lượng rating
    - Thời gian phát hành
    - Thể loại phim
    """
    # Tính rating trung bình và số lượng rating cho mỗi phim
    movie_stats = ratings.groupby('movie_id').agg({
        'stars': ['mean', 'count']
    }).reset_index()
    movie_stats.columns = ['movie_id', 'avg_rating', 'rating_count']
    
    # Merge với thông tin phim
    movie_data = pd.merge(movies, movie_stats, left_on='id', right_on='movie_id', how='left')
    movie_data['avg_rating'] = movie_data['avg_rating'].fillna(0)
    movie_data['rating_count'] = movie_data['rating_count'].fillna(0)
    
    # Tính điểm trending
    now = datetime.now()
    movie_data['days_since_release'] = movie_data['release_date'].apply(
        lambda x: (now - datetime.strptime(x, '%Y-%m-%d')).days
    )
    
    # Chuẩn hóa các chỉ số
    movie_data['rating_score'] = movie_data['avg_rating'] / 5.0
    movie_data['count_score'] = movie_data['rating_count'] / movie_data['rating_count'].max()
    movie_data['recency_score'] = 1 - (movie_data['days_since_release'] / movie_data['days_since_release'].max())
    
    # Tính điểm trending tổng hợp
    movie_data['trending_score'] = (
        movie_data['rating_score'] * 0.4 +  # Trọng số cho rating
        movie_data['count_score'] * 0.3 +   # Trọng số cho số lượng rating
        movie_data['recency_score'] * 0.3   # Trọng số cho độ mới
    )
    
    # Thêm các trường bổ sung
    movie_data['trending_rank'] = movie_data['trending_score'].rank(ascending=False)
    movie_data['is_trending'] = movie_data['trending_rank'] <= num_trending
    
    # Tạo dữ liệu trending
    trending_data = movie_data[movie_data['is_trending']].copy()
    trending_data['trending_start_date'] = trending_data.apply(
        lambda x: fake.date_time_between(
            start_date='-30d',
            end_date='now'
        ).strftime('%Y-%m-%d %H:%M:%S'),
        axis=1
    )
    
    # Thêm các thông tin bổ sung
    trending_data['trending_reason'] = trending_data.apply(
        lambda x: random.choice([
            'Phim mới phát hành',
            'Được đánh giá cao',
            'Nhiều người xem',
            'Phim hot trong tuần',
            'Phim được yêu thích'
        ]),
        axis=1
    )
    
    # Chọn các cột cần thiết
    trending_data = trending_data[[
        'movie_id', 'trending_score', 'trending_rank',
        'trending_start_date', 'trending_reason', 'is_trending'
    ]]
    
    return trending_data

def print_trending_stats(trending_data):
    """In thống kê về dữ liệu trending"""
    print("\n=== THỐNG KÊ DỮ LIỆU TRENDING ===")
    print(f"Tổng số phim trending: {len(trending_data)}")
    print(f"\nĐiểm trending:")
    print(f"- Cao nhất: {trending_data['trending_score'].max():.2f}")
    print(f"- Thấp nhất: {trending_data['trending_score'].min():.2f}")
    print(f"- Trung bình: {trending_data['trending_score'].mean():.2f}")
    
    print("\nLý do trending:")
    for reason, count in trending_data['trending_reason'].value_counts().items():
        print(f"- {reason}: {count} phim")

# Sinh dữ liệu trending
trending_data = generate_trending_data()

# In thống kê
print_trending_stats(trending_data)

# Lưu vào file CSV
trending_data.to_csv('trending.csv', index=False)
print("\nĐã lưu dữ liệu trending vào file trending.csv") 