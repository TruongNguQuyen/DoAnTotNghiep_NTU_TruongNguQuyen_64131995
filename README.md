# DoAnTotNghiep_NTU_TruongNguQuyen_64131995

Lưu trữ các kết quả thực nghiệm của đồ án tốt nghiệp.

---

## 1. Kết quả thời gian thực thi (Runtime Performance)

Bảng dưới đây so sánh thời gian thực thi (tính bằng giây) giữa thuật toán Gốc và thuật toán Cải tiến trên các bộ dữ liệu khác nhau.

| Datasets | Thuật toán | Runtime (seconds) | % Runtime vs Original | Số lượng mẫu (N) | Số chiều | No. Clusters |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Flame** | Gốc | 0.0234 | 100% | 240 | 2 | 2 |
| | Cải tiến | 0.0149 | 64% | 240 | 2 | 2 |
| **Spiral** | Gốc | 0.0302 | 100% | 312 | 2 | 3 |
| | Cải tiến | 0.0128 | 42% | 312 | 2 | 3 |
| **Aggregation** | Gốc | 0.1461 | 100% | 788 | 2 | 7 |
| | Cải tiến | 0.0385 | 26% | 788 | 2 | 7 |
| **Iris** | Gốc | 0.0048 | 100% | 150 | 4 | 3 |
| | Cải tiến | 0.0042 | 88% | 150 | 4 | 3 |

---

## 2. Thống kê số lượng phép so sánh khoảng cách và tỉ lệ cắt

Bảng so sánh số lượng phép tính khoảng cách cần thực hiện và tỷ lệ cắt giảm được nhờ thuật toán cải tiến.

| Datasets | Thuật toán | Số phép so sánh | 1 – (Số phép so sánh vs Original) % | Số lượng mẫu (N) | Số chiều | No. Clusters |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Flame** | Gốc | 28,680 | - | 240 | 2 | 2 |
| | Cải tiến | 2,651 | 91% | 240 | 2 | 2 |
| **Spiral** | Gốc | 48,516 | - | 312 | 2 | 3 |
| | Cải tiến | 3,134 | 94% | 312 | 2 | 3 |
| **Aggregation** | Gốc | 310,078 | - | 788 | 2 | 7 |
| | Cải tiến | 6,253 | 98% | 788 | 2 | 7 |
| **Iris** | Gốc | 11,175 | - | 150 | 4 | 3 |
| | Cải tiến | 4,100 | 63% | 150 | 4 | 3 |

---

## 3. So sánh kết quả phân cụm (Clustering Quality)

Bảng so sánh chất lượng phân cụm thông qua các chỉ số ARI, NMI và Sai số tuyệt đối nhằm chứng minh thuật toán cải tiến giữ nguyên được độ chính xác.

| Datasets | Thuật toán | ARI | NMI | Sai số tuyệt đối | Số lượng mẫu (N) | Số chiều | No. Clusters |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Flame** | Gốc | 1.0000 | 1.0000 | 0.0 | 240 | 2 | 2 |
| | Cải tiến | 1.0000 | 1.0000 | 0.0 | 240 | 2 | 2 |
| **Spiral** | Gốc | 1.0000 | 1.0000 | 0.0 | 312 | 2 | 3 |
| | Cải tiến | 1.0000 | 1.0000 | 0.0 | 312 | 2 | 3 |
| **Aggregation** | Gốc | 0.9978 | 0.9957 | 0.0 | 788 | 2 | 7 |
| | Cải tiến | 0.9978 | 0.9957 | 0.0 | 788 | 2 | 7 |
| **Iris** | Gốc | 0.8343 | 0.8244 | 0.0 | 150 | 4 | 3 |
| | Cải tiến | 0.8343 | 0.8244 | 0.0 | 150 | 4 | 3 |