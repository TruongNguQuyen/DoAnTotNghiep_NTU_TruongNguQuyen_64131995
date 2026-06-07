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

def compute_delta(dist_matrix, rho):

    n = len(rho)

    delta = np.zeros(n)

    nearest_higher = np.full(n, -1, dtype=int)

    comparison_count = 0

    order = np.lexsort((np.arange(n), -rho))

    highest_priority = order[0]

    delta[highest_priority] = np.max(dist_matrix[highest_priority])

    for i in range(1, n):

        current_index = order[i]

        best_distance = float("inf")

        best_candidate = -1

        for j in range(i):

            candidate_index = order[j]

            comparison_count += 1

            d = dist_matrix[current_index][candidate_index]

            if d < best_distance:

                best_distance = d

                best_candidate = candidate_index    

        delta[current_index] = best_distance

        nearest_higher[current_index] = best_candidate

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

    delta, nearest_higher, comparisons = compute_delta(dist_matrix, rho)

    end_time = time.perf_counter()

    delta_time = end_time - start_time

    print(f"Delta computation time: {delta_time:.4f} seconds")
    print("Brute force comparisons:", comparisons)

    gamma = compute_gamma(rho, delta)

    app = CSDPPO_UI(
        data,
        rho,
        delta,
        gamma,
        nearest_higher
    )

    plt.show()
