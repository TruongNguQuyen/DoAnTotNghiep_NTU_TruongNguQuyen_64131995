import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score

def load_data(file_path):
    
    data = []

    with open(file_path, 'r') as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            x = float(parts[0])
            y = float(parts[1])

            data.append([x, y])

    data = np.array(data, dtype=float)

    return data

def compute_distance_matrix(data):

    n = len(data)

    dist = np.zeros((n, n))

    for i in range(n):

        for j in range(n):

            xi = data[i][0]
            yi = data[i][1]

            xj = data[j][0]
            yj = data[j][1]

            d = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

            dist[i][j] = d

    return dist

def compute_rho(dist_matrix, dc):

    n = len(dist_matrix)

    rho = np.zeros(n)

    for i in range(n):

        density = 0

        for j in range(n):

            if i == j:

                continue

            dij = dist_matrix[i][j]

            value = np.exp(-(dij / dc) ** 2)

            density += value

        rho[i] = density

    return rho

def compute_delta_pgd(data, dist_matrix, rho, dc, k=1.0):

    n = len(rho)

    delta = np.zeros(n)

    nearest_higher = np.full(n, -1, dtype=int)

    comparison_count = 0

    cell_size = dc * k

    if cell_size <= 0:
        cell_size = 1.0

    # ==========================================================
    # SẮP XẾP THEO MẬT ĐỘ GIẢM DẦN
    # ==========================================================
    order = np.lexsort((np.arange(n), -rho))

    max_rho_idx = order[0]

    # Điểm có mật độ cao nhất
    delta[max_rho_idx] = np.max(dist_matrix[max_rho_idx])

    # ==========================================================
    # THÔNG TIN KHÔNG GIAN
    # ==========================================================
    x_min = np.min(data[:, 0])
    y_min = np.min(data[:, 1])

    x_max = np.max(data[:, 0])
    y_max = np.max(data[:, 1])

    # ==========================================================
    # HÀM XÁC ĐỊNH CELL
    # ==========================================================
    def get_cell(point):

        cell_x = int((point[0] - x_min) // cell_size)

        cell_y = int((point[1] - y_min) // cell_size)

        return (cell_x, cell_y)

    # ==========================================================
    # KÍCH THƯỚC GRID
    # ==========================================================
    grid_width = int((x_max - x_min) // cell_size) + 1

    grid_height = int((y_max - y_min) // cell_size) + 1

    max_radius = max(grid_width, grid_height)

    # ==========================================================
    # GRID
    # Chỉ chứa các điểm đã xử lý trước đó
    # ==========================================================
    grid = {}

    def add_point_to_grid(index):

        cell = get_cell(data[index])

        if cell not in grid:

            grid[cell] = {
                "points": []
            }

        grid[cell]["points"].append(index)

    # ==========================================================
    # THÊM ĐIỂM CÓ RHO LỚN NHẤT
    # ==========================================================
    add_point_to_grid(max_rho_idx)

    # ==========================================================
    # KHOẢNG CÁCH NHỎ NHẤT TỪ ĐIỂM ĐẾN CELL
    # ==========================================================
    def min_distance_to_cell(point, cell):

        cx, cy = cell

        x1 = x_min + cx * cell_size
        y1 = y_min + cy * cell_size

        x2 = x1 + cell_size
        y2 = y1 + cell_size

        px = point[0]
        py = point[1]

        dx = 0.0

        if px < x1:
            dx = x1 - px

        elif px > x2:
            dx = px - x2

        dy = 0.0

        if py < y1:
            dy = y1 - py

        elif py > y2:
            dy = py - y2

        return np.sqrt(dx * dx + dy * dy)

    # ==========================================================
    # TÍNH DELTA
    # ==========================================================
    for i in range(1, n):

        current_index = order[i]

        current_point = data[current_index]

        current_cell = get_cell(current_point)

        best = float("inf")

        best_parent = -1

        r = 0

        while r <= max_radius:

            # ==================================================
            # DUYỆT CÁC CELL TRÊN VIỀN RADIUS r
            # ==================================================
            for dx in range(-r, r + 1):

                for dy in range(-r, r + 1):

                    # Chỉ lấy viền ngoài
                    if max(abs(dx), abs(dy)) != r:
                        continue

                    neighbor_cell = (
                        current_cell[0] + dx,
                        current_cell[1] + dy
                    )

                    # Không có cell
                    if neighbor_cell not in grid:
                        continue

                    # ==========================================
                    # BOUNDING BOX PRUNING
                    # ==========================================
                    min_possible = min_distance_to_cell(
                        current_point,
                        neighbor_cell
                    )

                    # Cell không thể cải thiện nghiệm
                    if min_possible >= best:
                        continue

                    cell_info = grid[neighbor_cell]

                    # ==========================================
                    # DUYỆT CANDIDATE TRONG CELL
                    # ==========================================
                    for candidate_index in cell_info["points"]:

                        comparison_count += 1

                        d = dist_matrix[
                            current_index
                        ][
                            candidate_index
                        ]

                        if d < best:

                            best = d

                            best_parent = candidate_index

            # ==================================================
            # KIỂM TRA ĐIỀU KIỆN DỪNG
            # ==================================================
            if best < float("inf"):

                can_stop = True

                next_r = r + 1

                # Kiểm tra toàn bộ cell ở vòng tiếp theo
                for dx in range(-next_r, next_r + 1):

                    for dy in range(-next_r, next_r + 1):

                        if max(abs(dx), abs(dy)) != next_r:
                            continue

                        neighbor_cell = (
                            current_cell[0] + dx,
                            current_cell[1] + dy
                        )

                        min_possible = min_distance_to_cell(
                            current_point,
                            neighbor_cell
                        )

                        # Vẫn có khả năng tồn tại
                        # điểm gần hơn best
                        if min_possible < best:

                            can_stop = False
                            break

                    if not can_stop:
                        break

                if can_stop:
                    break

            r += 1

        # ======================================================
        # BACKUP AN TOÀN
        # ======================================================
        if best == float("inf"):

            best = np.max(dist_matrix[current_index])

        delta[current_index] = best

        nearest_higher[current_index] = best_parent

        # ======================================================
        # THÊM ĐIỂM HIỆN TẠI VÀO GRID
        # ======================================================
        add_point_to_grid(current_index)

    return delta, nearest_higher, comparison_count

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

    max_candidates = 100

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

        parent = nearest_higher[index]

        if parent != -1:

            labels[index] = labels[parent]

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

        self.scatter_data.set_array(labels.astype(float))

        self.scatter_data.set_sizes(
            np.full(len(labels), 30)
        )

        self.fig.canvas.draw_idle()

        print("Cluster done")


if __name__ == "__main__":
    
    data = load_data("flame_data.txt")

    dist_matrix = compute_distance_matrix(data)

    dist_list = get_distance_list(dist_matrix)

    dc = find_optimal_dc(dist_list, dist_matrix, 0.5, 10)

    print(f"Optimal dc: {dc}")

    rho = compute_rho(dist_matrix, dc)

    start_time = time.perf_counter()

    delta, nearest_higher, comparisons = compute_delta_pgd(data,dist_matrix, rho, dc, k=5.0)

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
