# DoAnTotNghiep_NTU_TruongNguQuyen_64131995

Lưu trữ các kết quả thực nghiệm của đồ án tốt nghiệp.

---

## 1. Kết quả trực quan hóa phân cụm (Visualizations)

Mỗi dòng dưới đây tương ứng với 4 ảnh kết quả nằm trên cùng một hàng:

### Bộ dữ liệu 1
<table>
  <tr>
    <td align="center"><b>Dữ liệu ban đầu</b><br><img src="path/to/image1_initial.png" width="200"/></td>
    <td align="center"><b>Ground Truth</b><br><img src="path/to/image1_gt.png" width="200"/></td>
    <td align="center"><b>CSDPPO</b><br><img src="path/to/image1_csdppo.png" width="200"/></td>
    <td align="center"><b>PGD-CSDPPO</b><br><img src="path/to/image1_pgd.png" width="200"/></td>
  </tr>
</table>

### Bộ dữ liệu 2
<table>
  <tr>
    <td align="center"><b>Dữ liệu ban đầu</b><br><img src="path/to/image2_initial.png" width="200"/></td>
    <td align="center"><b>Ground Truth</b><br><img src="path/to/image2_gt.png" width="200"/></td>
    <td align="center"><b>CSDPPO</b><br><img src="path/to/image2_csdppo.png" width="200"/></td>
    <td align="center"><b>PGD-CSDPPO</b><br><img src="path/to/image2_pgd.png" width="200"/></td>
  </tr>
</table>

### Bộ dữ liệu 3
<table>
  <tr>
    <td align="center"><b>Dữ liệu ban đầu</b><br><img src="path/to/image3_initial.png" width="200"/></td>
    <td align="center"><b>Ground Truth</b><br><img src="path/to/image3_gt.png" width="200"/></td>
    <td align="center"><b>CSDPPO</b><br><img src="path/to/image3_csdppo.png" width="200"/></td>
    <td align="center"><b>PGD-CSDPPO</b><br><img src="path/to/image3_pgd.png" width="200"/></td>
  </tr>
</table>

---

## 2. Kết quả thực nghiệm các bộ dữ liệu thành phố và dữ liệu nhóm

Bảng thống kê và so sánh chỉ số Silhouette cùng thời gian thực thi (Runtime) giữa thuật toán Gốc và Cải tiến.

| Datasets | Thuật toán | Silhouette | Runtime (seconds) | % Silhouette vs Original | % Runtime vs Original | No. Clusters |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **CanTho** | Gốc | 0.8211 | 1.8944 | 100% | 100% | 3 |
| | Cải tiến | 0.8211 | 0.0765 | 100% | 4% | 3 |
| **DongNai** | Gốc | 0.6456 | 0.9925 | 100% | 100% | 2 |
| | Cải tiến | 0.6456 | 0.0673 | 100% | 7% | 2 |
| **Nhom1** | Gốc | 0.7040 | 7.1503 | 100% | 100% | 5 |
| | Cải tiến | 0.7040 | 2.4182 | 100% | 34% | 5 |
| **Nhom2** | Gốc | 0.6631 | 2.4563 | 100% | 100% | 2 |
| | Cải tiến | 0.6631 | 0.2112 | 100% | 9% | 2 |
| **Nhom3** | Gốc | 0.5970 | 4.3370 | 100% | 100% | 3 |
| | Cải tiến | 0.5970 | 0.2246 | 100% | 5% | 3 |

---

## 3. Kết quả thời gian thực thi (Bộ dữ liệu gốc)

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

## 4. Thống kê số lượng phép so sánh khoảng cách và tỉ lệ cắt

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

## 5. So sánh kết quả phân cụm (Chất lượng phân cụm)

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