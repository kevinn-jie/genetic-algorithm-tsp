/**
 * @file  instance.h
 * @brief TSPLIB EUC_2D instance; node coordinates, distance lookup, neighbor lists, and known optimum.
 */

#pragma once
#include <cmath>
#include <optional>
#include <string>
#include <utility>
#include <vector>

// distance matrix memory budget (n * n ints); 1.5 GB fits all EUC_2D instances (d18512 ~1.37 GB)
// instances over budget -> on-the-fly distances
const long long MAX_MATRIX_BYTES = 1536LL * 1024 * 1024;

// nearest nodes kept per node for 2-opt candidate moves; n * k ints (d18512 ~1.2 MB)
// 16 over 10: lower GA error on every tested instance at similar speed
const int NEIGHBOR_COUNT = 16;

struct Node {
    int number;
    double x_coord;
    double y_coord;
};

/**
 * @brief   TSPLIB EUC_2D instance; nodes, distances, neighbor lists, and known optimum.
 * @details Builds distance matrix and neighbor lists on construction.
 */
class Instance {
public:
    explicit Instance(std::string name, std::vector<Node> nodes, std::optional<long long> optimal_fitness)
        : name(std::move(name)),
          nodes(std::move(nodes)),
          dimension(static_cast<int>(this->nodes.size())),
          optimal_fitness(optimal_fitness) {
            build_distance_matrix();
            build_neighbor_lists();
          }

    /**
     * @brief   Loads TSPLIB instance from .tsp file.
     * @details Looks up known optimum in optimality_file by filename; throws on invalid file.
     */
    static Instance get_instance(const std::string& instance_file, const std::string& optimality_file);

    // matrix lookup several times faster than sqrt; empty matrix (over budget or allocation failed) -> computed on the fly
    // size_t index; node1 * dimension can overflow int on large instances
    int get_distance(int node1, int node2) const {
        if (distance_matrix.empty()) {
            return compute_distance(node1, node2);
        }

        return distance_matrix[static_cast<std::size_t>(node1) * dimension + node2];
    }

    // rank 0 = nearest; sorted by distance ascending
    int get_neighbor(int node, int rank) const {
        return neighbor_lists[static_cast<std::size_t>(node) * neighbor_count + rank];
    }

    // TSPLIB node number from the .tsp file (1-based); tours store 0-based indices
    int get_node_number(int node) const {
        return nodes[node].number;
    }

    int get_neighbor_count() const {
        return neighbor_count;
    }

    int get_dimension() const {
        return dimension;
    }

    const std::string& get_name() const {
        return name;
    }

    std::optional<long long> get_optimal_fitness() const {
        return optimal_fitness;
    }

/**
 * @brief   Computes TSPLIB EUC_2D distance; Euclidean distance rounded to nearest int.
 */
private:
    int compute_distance(int node1, int node2) const {
        double dx = nodes[node1].x_coord - nodes[node2].x_coord;
        double dy = nodes[node1].y_coord - nodes[node2].y_coord;

        // TSPLIB nint = (int)(x + 0.5); same result as std::lround for x >= 0, much faster
        return static_cast<int>(std::sqrt(dx * dx + dy * dy) + 0.5);
    }

    /**
     * @brief   Builds flat n * n distance matrix; precomputes all pairwise distances.
     * @details Skipped if over MAX_MATRIX_BYTES or allocation fails.
     */
    void build_distance_matrix();

    /**
     * @brief   Builds neighbor lists; nearest neighbor_count nodes per node for 2-opt.
     */
    void build_neighbor_lists();

    /**
     * @brief   Extracts value after ':' in "KEY : value" line, trimmed.
     * @details Returns empty string if no colon or no value.
     */
    static std::string get_header(const std::string& line);

    /**
     * @brief   Finds known optimum for instance_name in optimality_file.
     * @details Returns empty optional if instance not listed.
     */
    static std::optional<long long> find_optimal_fitness(const std::string& optimality_file, const std::string& instance_name);

    std::string name;
    std::vector<Node> nodes;
    int dimension = 0;

    // empty if no known optimum
    std::optional<long long> optimal_fitness;
    
    // flat n * n, row-major; one contiguous block for cache efficiency
    std::vector<int> distance_matrix;

    // min(NEIGHBOR_COUNT, dimension - 1); flat n * neighbor_count, row-major
    int neighbor_count = 0;
    std::vector<int> neighbor_lists;
};
