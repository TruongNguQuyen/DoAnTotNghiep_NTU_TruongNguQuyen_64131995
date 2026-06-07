import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time
from matplotlib.colors import ListedColormap
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score
from sklearn.datasets import load_iris
from sklearn.datasets import make_blobs
from sklearn.datasets import load_wine


# def load_data(file_path):

#     data = []

#     labels = []

#     start_data = False

#     with open(file_path, 'r') as file:

#         for line in file:

#             line = line.strip()

#             if line == "":
#                 continue

#             if line.startswith('%'):
#                 continue

#             if line.upper().startswith('@DATA'):

#                 start_data = True

#                 continue

#             if not start_data:
#                 continue

#             parts = line.split(',')

#             if len(parts) < 3:
#                 continue

#             x = float(parts[0])

#             y = float(parts[1])

#             label = int(parts[2])

#             data.append([x, y])

#             labels.append(label)

#     data = np.array(data, dtype=float)

#     labels = np.array(labels, dtype=int)

#     return data, labels

# load data nhiều chiều
def load_data(file_path):

    data = []

    labels = []

    start_data = False

    with open(file_path, 'r') as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            # Bỏ comment
            if line.startswith('%'):
                continue

            # Tìm phần dữ liệu
            if line.upper().startswith('@DATA'):

                start_data = True

                continue

            # Bỏ metadata
            if not start_data:
                continue

            parts = line.split(',')

            # Cần ít nhất:
            # 1 feature + 1 label
            if len(parts) < 2:
                continue

            # ==================================================
            # FEATURES
            # ==================================================
            features = [
                float(v)
                for v in parts[:-1]
            ]

            # ==================================================
            # LABEL
            # ==================================================
            label = parts[-1]

            # Nếu label dạng số
            try:
                label = int(label)

            except:
                pass

            data.append(features)

            labels.append(label)

    data = np.array(data, dtype=float)

    labels = np.array(labels)

    return data, labels

def compute_distance_matrix(data):

    # n = len(data)

    # dist = np.zeros((n, n))

    # for i in range(n):

    #     for j in range(n):

    #         xi = data[i][0]
    #         yi = data[i][1]

    #         xj = data[j][0]
    #         yj = data[j][1]

    #         d = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

    #         dist[i][j] = d

    diff = data[:, np.newaxis, :] - data[np.newaxis, :, :]

    dist = np.sqrt(np.sum(diff ** 2, axis=2))

    return dist

def compute_rho(dist_matrix, dc):

    # n = len(dist_matrix)

    # rho = np.zeros(n)

    # for i in range(n):

    #     density = 0

    #     for j in range(n):

    #         if i == j:

    #             continue

    #         dij = dist_matrix[i][j]

    #         value = np.exp(-(dij / dc) ** 2)

    #         density += value

    #     rho[i] = density

    rho = np.sum(
        np.exp(-(dist_matrix / dc) ** 2),
        axis=1
    ) - 1

    return rho

# def compute_delta_pgd(data, dist_matrix, rho, dc, k=1.0):

#     n = len(rho)

#     delta = np.zeros(n)

#     nearest_higher = np.full(n, -1, dtype=int)

#     comparison_count = 0

#     cell_size = dc * k

#     if cell_size <= 0:
#         cell_size = 1.0

#     # ==========================================================
#     # SẮP XẾP THEO MẬT ĐỘ GIẢM DẦN
#     # ==========================================================
#     order = np.lexsort((np.arange(n), -rho))

#     max_rho_idx = order[0]

#     # Điểm có mật độ cao nhất
#     delta[max_rho_idx] = np.max(dist_matrix[max_rho_idx])

#     # ==========================================================
#     # THÔNG TIN KHÔNG GIAN
#     # ==========================================================
#     x_min = np.min(data[:, 0])
#     y_min = np.min(data[:, 1])

#     x_max = np.max(data[:, 0])
#     y_max = np.max(data[:, 1])

#     # ==========================================================
#     # HÀM XÁC ĐỊNH CELL
#     # ==========================================================
#     def get_cell(point):

#         cell_x = int((point[0] - x_min) // cell_size)

#         cell_y = int((point[1] - y_min) // cell_size)

#         return (cell_x, cell_y)

#     # ==========================================================
#     # KÍCH THƯỚC GRID
#     # ==========================================================
#     grid_width = int((x_max - x_min) // cell_size) + 1

#     grid_height = int((y_max - y_min) // cell_size) + 1

#     max_radius = max(grid_width, grid_height)

#     # ==========================================================
#     # GRID
#     # Chỉ chứa các điểm đã xử lý trước đó
#     # ==========================================================
#     grid = {}

#     def add_point_to_grid(index):

#         cell = get_cell(data[index])

#         if cell not in grid:

#             grid[cell] = {
#                 "points": []
#             }

#         grid[cell]["points"].append(index)

#     # ==========================================================
#     # THÊM ĐIỂM CÓ RHO LỚN NHẤT
#     # ==========================================================
#     add_point_to_grid(max_rho_idx)

#     # ==========================================================
#     # KHOẢNG CÁCH NHỎ NHẤT TỪ ĐIỂM ĐẾN CELL
#     # ==========================================================
#     def min_distance_to_cell(point, cell):

#         cx, cy = cell

#         x1 = x_min + cx * cell_size
#         y1 = y_min + cy * cell_size

#         x2 = x1 + cell_size
#         y2 = y1 + cell_size

#         px = point[0]
#         py = point[1]

#         dx = 0.0

#         if px < x1:
#             dx = x1 - px

#         elif px > x2:
#             dx = px - x2

#         dy = 0.0

#         if py < y1:
#             dy = y1 - py

#         elif py > y2:
#             dy = py - y2

#         return np.sqrt(dx * dx + dy * dy)

#     # ==========================================================
#     # TÍNH DELTA
#     # ==========================================================
#     for i in range(1, n):

#         current_index = order[i]

#         current_point = data[current_index]

#         current_cell = get_cell(current_point)

#         best = float("inf")

#         best_parent = -1

#         r = 0

#         while r <= max_radius:

#             # ==================================================
#             # DUYỆT CÁC CELL TRÊN VIỀN RADIUS r
#             # ==================================================
#             for dx in range(-r, r + 1):

#                 for dy in range(-r, r + 1):

#                     # Chỉ lấy viền ngoài
#                     if max(abs(dx), abs(dy)) != r:
#                         continue

#                     neighbor_cell = (
#                         current_cell[0] + dx,
#                         current_cell[1] + dy
#                     )

#                     # Không có cell
#                     if neighbor_cell not in grid:
#                         continue

#                     # ==========================================
#                     # BOUNDING BOX PRUNING
#                     # ==========================================
#                     min_possible = min_distance_to_cell(
#                         current_point,
#                         neighbor_cell
#                     )

#                     # Cell không thể cải thiện nghiệm
#                     if min_possible >= best:
#                         continue

#                     cell_info = grid[neighbor_cell]

#                     # ==========================================
#                     # DUYỆT CANDIDATE TRONG CELL
#                     # ==========================================
#                     for candidate_index in cell_info["points"]:

#                         comparison_count += 1

#                         d = dist_matrix[
#                             current_index
#                         ][
#                             candidate_index
#                         ]

#                         if d < best:

#                             best = d

#                             best_parent = candidate_index

#             # ==================================================
#             # KIỂM TRA ĐIỀU KIỆN DỪNG
#             # ==================================================
#             if best < float("inf"):

#                 can_stop = True

#                 next_r = r + 1

#                 # Kiểm tra toàn bộ cell ở vòng tiếp theo
#                 for dx in range(-next_r, next_r + 1):

#                     for dy in range(-next_r, next_r + 1):

#                         if max(abs(dx), abs(dy)) != next_r:
#                             continue

#                         neighbor_cell = (
#                             current_cell[0] + dx,
#                             current_cell[1] + dy
#                         )

#                         min_possible = min_distance_to_cell(
#                             current_point,
#                             neighbor_cell
#                         )

#                         # Vẫn có khả năng tồn tại
#                         # điểm gần hơn best
#                         if min_possible < best:

#                             can_stop = False
#                             break

#                     if not can_stop:
#                         break

#                 if can_stop:
#                     break

#             r += 1

#         # ======================================================
#         # BACKUP AN TOÀN
#         # ======================================================
#         if best == float("inf"):

#             best = np.max(dist_matrix[current_index])

#         delta[current_index] = best

#         nearest_higher[current_index] = best_parent

#         # ======================================================
#         # THÊM ĐIỂM HIỆN TẠI VÀO GRID
#         # ======================================================
#         add_point_to_grid(current_index)

#     return delta, nearest_higher, comparison_count

# hàm PGD_delta đọc dữ liệu nhiều chiều:
# def compute_delta_pgd(data, dist_matrix, rho, dc, k=1.0):

#     import itertools

#     n = len(rho)

#     dim = data.shape[1]

#     delta = np.zeros(n)

#     nearest_higher = np.full(n, -1, dtype=int)

#     comparison_count = 0

#     cell_size = dc * k

#     if cell_size <= 0:
#         cell_size = 1.0

#     order = np.lexsort((np.arange(n), -rho))

#     max_rho_idx = order[0]

#     delta[max_rho_idx] = np.max(dist_matrix[max_rho_idx])

#     data_min = np.min(data, axis=0)

#     data_max = np.max(data, axis=0)

#     def get_cell(point):

#         cell = tuple(
#             int((point[d] - data_min[d]) // cell_size)
#             for d in range(dim)
#         )

#         return cell

#     grid_shape = []

#     for d in range(dim):

#         size = int((data_max[d] - data_min[d]) // cell_size) + 1

#         grid_shape.append(size)

#     max_radius = max(grid_shape)

#     grid = {}

#     def add_point_to_grid(index):

#         cell = get_cell(data[index])

#         if cell not in grid:

#             grid[cell] = {
#                 "points": []
#             }

#         grid[cell]["points"].append(index)

#     add_point_to_grid(max_rho_idx)

#     def min_distance_to_cell(point, cell):

#         squared_distance = 0.0

#         for d in range(dim):

#             c = cell[d]

#             cell_min = data_min[d] + c * cell_size

#             cell_max = cell_min + cell_size

#             p = point[d]

#             if p < cell_min:

#                 diff = cell_min - p

#             elif p > cell_max:

#                 diff = p - cell_max

#             else:

#                 diff = 0.0

#             squared_distance += diff * diff

#         return np.sqrt(squared_distance)

#     for i in range(1, n):

#         current_index = order[i]

#         current_point = data[current_index]

#         current_cell = get_cell(current_point)

#         best = float("inf")

#         best_parent = -1

#         r = 0

#         while r <= max_radius:

#             ranges = [range(-r, r + 1) for _ in range(dim)]

#             for offset in itertools.product(*ranges):

#                 if max(abs(v) for v in offset) != r:
#                     continue

#                 neighbor_cell = tuple(
#                     current_cell[d] + offset[d]
#                     for d in range(dim)
#                 )

#                 if neighbor_cell not in grid:
#                     continue

#                 min_possible = min_distance_to_cell(
#                     current_point,
#                     neighbor_cell
#                 )

#                 if min_possible >= best:
#                     continue

#                 cell_info = grid[neighbor_cell]

#                 for candidate_index in cell_info["points"]:

#                     comparison_count += 1

#                     d = dist_matrix[
#                         current_index
#                     ][
#                         candidate_index
#                     ]

#                     if d < best:

#                         best = d

#                         best_parent = candidate_index

#             if best < float("inf"):

#                 can_stop = True

#                 next_r = r + 1

#                 ranges = [
#                     range(-next_r, next_r + 1)
#                     for _ in range(dim)
#                 ]

#                 for offset in itertools.product(*ranges):

#                     if max(abs(v) for v in offset) != next_r:
#                         continue

#                     neighbor_cell = tuple(
#                         current_cell[d] + offset[d]
#                         for d in range(dim)
#                     )

#                     min_possible = min_distance_to_cell(
#                         current_point,
#                         neighbor_cell
#                     )

#                     if min_possible < best:

#                         can_stop = False

#                         break

#                 if can_stop:
#                     break

#             r += 1

#         if best == float("inf"):

#             best = np.max(dist_matrix[current_index])

#         delta[current_index] = best

#         nearest_higher[current_index] = best_parent

#         add_point_to_grid(current_index)

#     return delta, nearest_higher, comparison_count

def compute_delta_pgd(data, dist_matrix, rho, dc, k=1.0):
    n = len(rho)
    dim = data.shape[1]
    delta = np.zeros(n)
    nearest_higher = np.full(n, -1, dtype=int)
    comparison_count = 0  # Biến đếm số phép so sánh khoảng cách thực tế
    
    cell_size = dc * k
    if cell_size <= 0:
        cell_size = 1.0

    # ==========================================================
    # STEP 2: SẮP XẾP THEO MẬT ĐỘ GIẢM DẦN
    # ==========================================================
    order = np.lexsort((np.arange(n), -rho))
    max_rho_idx = order[0]

    # STEP 3: ĐIỂM CÓ ĐỘ ƯU TIÊN CAO NHẤT
    delta[max_rho_idx] = np.max(dist_matrix[max_rho_idx])

    # Xác định biên không gian dữ liệu phục vụ phân hoạch lưới
    data_min = [np.min(data[:, d]) for d in range(dim)]
    data_max = [np.max(data[:, d]) for d in range(dim)]

    # Cấu trúc lưu trữ Grid: quản lý bằng Dictionary thuần Python để đồng bộ tốc độ
    grid = {}

    def get_cell_coords(point):
        return tuple(int((point[d] - data_min[d]) // cell_size) for d in range(dim))

    # Nạp điểm gốc mật độ cao nhất vào hệ thống lưới
    first_cell = get_cell_coords(data[max_rho_idx])
    grid[first_cell] = [max_rho_idx]

    # Hàm tính khoảng cách tối thiểu từ điểm đến Bounding Box của ô lưới bằng Python thuần
    def min_distance_to_bounding_box(point, cell_coords):
        squared_distance = 0.0
        for d in range(dim):
            c = cell_coords[d]
            cell_min = data_min[d] + c * cell_size
            cell_max = cell_min + cell_size
            p = point[d]
            
            if p < cell_min:
                diff = cell_min - p
            elif p > cell_max:
                diff = p - cell_max
            else:
                diff = 0.0
            squared_distance += diff * diff
        return np.sqrt(squared_distance)

    # ==========================================================
    # TIẾN HÀNH XÁC ĐỊNH DELTA CHO CÁC PHẦN TỬ CÒN LẠI
    # ==========================================================
    for i in range(1, n):
        current_index = order[i]
        current_point = data[current_index]
        current_cell = get_cell_coords(current_point)
        
        best = float("inf")
        best_parent = -1
        
        # Tạo danh sách các ô hiện đang hoạt động (có chứa điểm mật độ cao hơn)
        active_cells = list(grid.keys())
        
        # Tính toán khoảng cách hình học và bán kính lưới bằng vòng lặp thuần Python
        # để đảm bảo tính công bằng tuyệt đối về mặt cấu trúc lệnh với giải thuật gốc
        cell_info_list = []
        for cell in active_cells:
            # Tính khoảng cách hình học tối thiểu đến hộp bao (Phục vụ Bước 5)
            d_min = min_distance_to_cell_fair(current_point, cell, data_min, cell_size, dim)
            
            # Tính bán kính lưới hình học Chebyshev (Phục vụ Bước 4)
            radius = max(abs(cell[d] - current_cell[d]) for d in range(dim))
            
            cell_info_list.append((radius, d_min, cell))
            
        # Sắp xếp các ô hoạt động theo thứ tự bán kính tăng dần (Bước 4: Mở rộng bán kính lưới)
        cell_info_list.sort(key=lambda x: x[0])
        
        # Duyệt qua từng ô theo chiến lược loang bán kính từ trong ra ngoài
        idx = 0
        total_active_cells = len(cell_info_list)
        
        while idx < total_active_cells:
            current_radius = cell_info_list[idx][0]
            
            # Thu thập toàn bộ các ô thuộc cùng tầng bán kính r hiện tại
            cells_in_current_radius = []
            while idx < total_active_cells and cell_info_list[idx][0] == current_radius:
                cells_in_current_radius.append(cell_info_list[idx])
                idx += 1
                
            # Duyệt các ô trên đường biên mở rộng của bán kính hiện tại
            for radius, d_min, cell in cells_in_current_radius:
                
                # STEP 5: BOUNDING-BOX PRUNING (Cắt tỉa không gian)
                if d_min >= best:
                    continue  # Bỏ qua hoàn toàn ô lưới, không duyệt các điểm bên trong
                    
                # STEP 6: CẬP NHẬT NGHIỆM TỐI ƯU CỤC BỘ
                for candidate_index in grid[cell]:
                    comparison_count += 1  # Chỉ tăng khi thực hiện phép so sánh thực tế
                    
                    d = dist_matrix[current_index][candidate_index]
                    if d < best:
                        best = d
                        best_parent = candidate_index
                        
            # STEP 7: ĐIỀU KIỆN DỪNG TÌM KIẾM SỚM NGHIÊM NGẶT
            # Nếu đã tìm được nghiệm tốt nhất và khoảng cách nhỏ nhất tới TẤT CẢ các ô ở vòng ngoài
            # đều lớn hơn hoặc bằng 'best' hiện tại, lập tức bẻ gãy vòng lặp.
            if best < float("inf") and idx < total_active_cells:
                stop_search = True
                for remaining_idx in range(idx, total_active_cells):
                    if cell_info_list[remaining_idx][1] < best:
                        stop_search = False
                        break
                if stop_search:
                    break

        # Khôi phục an toàn (Backup) cho các điểm vùng biên cô lập
        if best == float("inf"):
            best = np.max(dist_matrix[current_index])
            
        delta[current_index] = best
        nearest_higher[current_index] = best_parent

        # STEP 8: CẬP NHẬT CẤU TRÚC LƯỚI
        if current_cell not in grid:
            grid[current_cell] = []
        grid[current_cell].append(current_index)

    return delta, nearest_higher, comparison_count

# Hàm bổ trợ độc lập sử dụng biến cục bộ tăng tốc tối đa cho vòng lặp Python thuần
def min_distance_to_cell_fair(point, cell, data_min, cell_size, dim):
    squared_distance = 0.0
    for d in range(dim):
        cell_min = data_min[d] + cell[d] * cell_size
        cell_max = cell_min + cell_size
        p = point[d]
        if p < cell_min:
            diff = cell_min - p
        elif p > cell_max:
            diff = p - cell_max
        else:
            diff = 0.0
        squared_distance += diff * diff
    return np.sqrt(squared_distance)


def find_optimal_dc(dist_list, dist_matrix, min_percent, max_percent):

    n = len(dist_list)

    start_index = int(n * min_percent / 100)

    end_index = int(n * max_percent / 100)

    start_index = max(0, start_index)

    end_index = min(n - 1, end_index)

    if end_index <= start_index:
        end_index = start_index + 1

    best_dc = dist_list[start_index]

    best_entropy = float("inf")

    candidate_dc = dist_list[start_index:end_index]

    max_candidates = 500

    if len(candidate_dc) > max_candidates:

        indices = np.linspace(0, len(candidate_dc) - 1, max_candidates, dtype=int)

        candidate_dc = candidate_dc[indices]

    for dc in candidate_dc:

        rho = compute_rho(dist_matrix, dc)

        total_rho = np.sum(rho)

        if total_rho == 0:
            continue

        probability = rho / total_rho

        probability = probability[probability > 0]

        entropy = -np.sum(probability * np.log(probability))

        if entropy < best_entropy:

            best_entropy = entropy

            best_dc = dc

    return best_dc

def cluster_data(rho, nearest_higher, centers):

    n = len(rho)

    labels = np.full(n, -1, dtype=int)

    for cluster_id, center_index in enumerate(centers):

        labels[center_index] = cluster_id

    order = np.argsort(-rho)

    for index in order:

        if labels[index] != -1:
            continue

        current = index

        while current != -1 and labels[current] == -1:
            current = nearest_higher[current]

        if current != -1:
            labels[index] = labels[current]

    return labels

def get_distance_list(dist_matrix):

    n = len(dist_matrix)

    distances = dist_matrix[np.triu_indices(n, 1)]

    distances = np.sort(distances)

    return distances

def compute_gamma(rho, delta):

    gamma = rho * delta

    return gamma

def get_top_gamma(gamma, top_k=10):

    indices = np.argsort(-gamma)

    top_indices = indices[:top_k]

    return top_indices

class CSDPPO_UI:

    def __init__(self, data, rho, delta, gamma, nearest_higher):

        self.data = data

        self.rho = rho

        self.delta = delta

        self.gamma = gamma

        self.nearest_higher = nearest_higher

        self.selected_centers = []

        self.create_ui()

    def create_ui(self):

        self.fig = plt.figure(figsize=(12, 6))

        self.ax_data = self.fig.add_axes([0.05, 0.15, 0.40, 0.75])

        self.scatter_data = self.ax_data.scatter(
            self.data[:, 0],
            self.data[:, 1],
            s=20
        )

        self.ax_data.set_title("Original Data")

        self.ax_data.set_aspect('equal', adjustable='datalim')
        
        self.ax_data.autoscale()

        self.ax_dg = self.fig.add_axes([0.55, 0.15, 0.40, 0.75])

        self.scatter_dg = self.ax_dg.scatter(
            self.rho,
            self.delta,
            s=25,
            picker=True
        )

        self.ax_dg.set_title("Decision Graph")

        self.ax_dg.set_xlabel("rho")
        self.ax_dg.set_ylabel("delta")

        top_points = get_top_gamma(self.gamma, top_k=5)

        for rank, idx in enumerate(top_points):

            x = self.rho[idx]
            y = self.delta[idx]

            self.ax_dg.scatter(
                x,
                y,
                s=300,
                facecolors='none',
                edgecolors='red',
                linewidths=2
            )

            self.ax_dg.text(
                x,
                y,
                str(rank + 1),
                ha='center',
                va='center',
                fontsize=9,
                color='red'
            )

        self.btn_cluster = Button(
            plt.axes([0.43, 0.03, 0.14, 0.06]),
            "Cluster"
        )

        self.btn_cluster.on_clicked(self.cluster)

        self.fig.canvas.mpl_connect(
            'pick_event',
            self.on_pick
        )

    def on_pick(self, event):

        if event.artist != self.scatter_dg:
            return
        
        index = event.ind[0]

        if index in self.selected_centers:
            return
        
        self.selected_centers.append(index)

        self.ax_dg.scatter(
            self.rho[index],
            self.delta[index],
            s=500,
            marker='*',
            color='black'
        )

        self.fig.canvas.draw_idle()

        print("Selected center:", index)

    def cluster(self, event):

        if len(self.selected_centers) == 0:
            print("Chưa chọn center")
            return
        
        labels = cluster_data(
            self.rho,
            self.nearest_higher,
            self.selected_centers
        )

        unique_labels = np.unique(labels)
        cmap = ListedColormap(['purple', 'yellow', 'blue', 'green', 'red'])

        self.scatter_data.set_array(labels)
        self.scatter_data.set_cmap(cmap)
        self.scatter_data.set_clim(-0.5, len(unique_labels)-0.5)

        self.scatter_data.set_sizes(
            np.full(len(labels), 30)
        )

        
        ari = adjusted_rand_score(true_labels, labels)

        nmi = normalized_mutual_info_score(true_labels, labels)

        print(f"ARI: {ari:.4f}")

        print(f"NMI: {nmi:.4f}")

        self.fig.canvas.draw_idle()

        print("Cluster done")


if __name__ == "__main__":
    
    # chọn 1 trong 2 dòng dưới để đọc dữ liệu từ file hoặc từ sklearn dataset

    # data, true_labels = load_data("hepta.arff")

    # đọc dữ liệu Iris từ sklearn

    wine = load_wine()

    data = wine.data

    true_labels = wine.target

    # đọc dữ liệu make blobs từ sklearn

    # data, true_labels = make_blobs(
    # n_samples=1200,
    # centers=4,
    # n_features=5,
    # cluster_std=1,
    # random_state=42
    # )

    dist_matrix = compute_distance_matrix(data)

    dist_list = get_distance_list(dist_matrix)

    dc = find_optimal_dc(dist_list, dist_matrix, 0.5, 10)

    print(f"Optimal dc: {dc}")

    rho = compute_rho(dist_matrix, dc)

    start_time = time.perf_counter()

    delta, nearest_higher, comparisons = compute_delta_pgd(data,dist_matrix, rho, dc, k=10.0)

    end_time = time.perf_counter()

    delta_time = end_time - start_time

    print(f"Delta computation time: {delta_time:.4f} seconds")
    print("PGD comparisons:", comparisons)

    gamma = compute_gamma(rho, delta)

    app = CSDPPO_UI(
        data,
        rho,
        delta,
        gamma,
        nearest_higher
    )

    plt.show()
