# 🎬 Hệ Thống Gợi Ý Phim Thông Minh

## 📝 Mô tả
Hệ thống gợi ý phim thông minh sử dụng kết hợp nhiều phương pháp để đưa ra các gợi ý phim phù hợp cho người dùng. Hệ thống đặc biệt tập trung vào việc xử lý vấn đề "cold start" - khi người dùng mới tham gia hệ thống.

## 🎯 Tính năng chính

### 1. Xử lý Cold Start
- Phát hiện người dùng mới
- Áp dụng chiến lược gợi ý đặc biệt
- Kết hợp nhiều yếu tố để đưa ra gợi ý phù hợp

### 2. Tính điểm Trending
- Xét đến thời gian phát hành
- Số lượt xem
- Đánh giá trung bình
- Yếu tố thời gian

### 3. Tính điểm Nội dung
- Thể loại phim
- Quốc gia sản xuất
- Năm sản xuất
- Thông tin diễn viên/đạo diễn

## 🔄 Lưu đồ thuật toán

### Tổng quan
```
[User Request] → [Cold Start Check] → [Recommendation Strategy] → [Result Generation]
```

### Chi tiết xử lý
1. **Kiểm tra Cold Start**
   ```
   [User Request]
           ↓
   [Check User History]
           ↓
   [Is New User?] → Yes → [Apply Cold Start Strategy]
           ↓ No
   [Apply Regular Recommendation]
   ```

2. **Chiến lược Cold Start**
   ```
   [Apply Cold Start Strategy]
           ↓
   [Calculate Trending Score]
           ↓
   [Calculate Content Score]
           ↓
   [Calculate Final Recommendation Score]
           ↓
   [Sort and Filter Results]
   ```

## 📊 Công thức tính điểm

### Trending Score
```
TrendingScore = (TimeDecayFactor * ViewCountWeight) + (RatingWeight * AverageRating)
```

### Content Score
```
ContentScore = (GenreWeight * GenreMatch) + (CountryWeight * CountryMatch) + (YearWeight * YearMatch)
```

### Final Recommendation Score
```
FinalScore = (α * TrendingScore) + (β * ContentScore)
```

## ⚙️ Các tham số quan trọng

| Tham số | Mô tả |
|---------|--------|
| Time Decay Factor | Hệ số suy giảm theo thời gian |
| View Count Weight | Trọng số cho số lượt xem |
| Rating Weight | Trọng số cho đánh giá |
| Genre Weight | Trọng số cho thể loại |
| Country Weight | Trọng số cho quốc gia |
| Year Weight | Trọng số cho năm sản xuất |

## 🎨 Định dạng đầu ra

Mỗi phim được gợi ý sẽ hiển thị:
- Tên phim
- Thể loại
- Quốc gia
- Năm sản xuất
- Đạo diễn
- Diễn viên
- Thời lượng
- Điểm trending
- Điểm gợi ý

## 🔍 Xử lý lỗi và ngoại lệ

- Kiểm tra tính hợp lệ của dữ liệu
- Xử lý dữ liệu thiếu
- Áp dụng chiến lược dự phòng

## ⚡ Tối ưu hóa hiệu suất

- Sử dụng caching cho các tính toán phức tạp
- Tối ưu hóa truy vấn cơ sở dữ liệu
- Sử dụng các cấu trúc dữ liệu hiệu quả

## 📈 Kết quả đánh giá

### Ưu điểm
- Đa dạng về thể loại, quốc gia, năm sản xuất
- Phân biệt rõ ràng về điểm gợi ý
- Kết hợp cả yếu tố trending và điểm gợi ý
- Có phim từ quốc gia của user

### Điểm cần cải thiện
- Nhiều phim có điểm trending = 0.00
- Cần thêm thông tin về rating trung bình
- Cần thêm mô tả ngắn về nội dung phim
- Cần thêm số lượt xem để tăng độ tin cậy

## 🔮 Hướng phát triển

1. Cải thiện thuật toán tính điểm trending
2. Thêm các yếu tố mới:
   - Rating trung bình
   - Số lượt xem
   - Mô tả nội dung
   - Thông tin giải thưởng
3. Tối ưu hóa hiệu suất
4. Cải thiện độ chính xác của gợi ý

## 📚 Tài liệu tham khảo

- [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering)
- [Content-based Filtering](https://en.wikipedia.org/wiki/Content-based_filtering)
- [Cold Start Problem](https://en.wikipedia.org/wiki/Cold_start_(computing))
