#pragma once

#include <optional>
#include <random>
#include <vector>

#include "instance.h"

// for d18512, 10000 seems to be a good upper-bound; many runs stop between 6000-8000 generations
const int MAX_GENERATIONS = 10000;

// less than 200 results in premature convergence
const int CONVERGENCE_GENERATIONS = 200;
const int POPULATION_SIZE = 200;
const int SELECTION_SIZE = 7;
const double CROSSOVER_RATE = 0.85;

// having guaranteed mutation resulted in better, consistent tour diversity
const double MUTATION_RATE = 1.0;

struct Generation {
    int number;
    double time;
    long long elite_fitness;
};

// returned instead of printed; caller decides where output goes (file write happens after timing stops)
struct RunResult {
    long long elite_fitness;
    std::vector<int> elite_tour;
    std::vector<Generation> generations;
};

/**
 * @brief   Creates initial population of POPULATION_SIZE random tours.
 * @details Each tour is a shuffled permutation of nodes 0..dimension - 1.
 */
std::vector<std::vector<int>> create_population(int dimension, std::mt19937& rng);

/**
 * @brief   Computes fitness of tour; lower is better.
 * @details Sums distances between consecutive nodes, including return edge to start.
 */
long long compute_fitness(const std::vector<int>& tour, const Instance& instance);

/**
 * @brief   Finds elite; index of fittest tour in population.
 */
int run_elitism(const std::vector<long long>& fitnesses);

/**
 * @brief   Tournament selection; returns index of selected parent.
 * @details Picks SELECTION_SIZE random tours (with replacement), returns fittest.
 */
int run_selection(const std::vector<long long>& fitnesses, std::mt19937& rng);

/**
 * @brief   Order crossover (OX); combines two parents into one offspring.
 * @details With probability of 1 - CROSSOVER_RATE, returns random parent unchanged.
 *          Otherwise, keeps slice of parent1, fills rest in parent2's order.
 */
std::vector<int> run_crossover(const std::vector<int>& parent1, const std::vector<int>& parent2, std::mt19937& rng);

/**
 * @brief   Swap mutation; exchanges two random nodes in tour.
 * @details With probability of MUTATION_RATE; mutates in place.
 */
void run_mutation(std::vector<int>& tour, std::mt19937& rng);

/**
 * @brief   Creates one offspring from population.
 * @details Selects two distinct parents, then applies crossover and mutation.
 */
std::vector<int> make_offspring(const std::vector<std::vector<int>>& population, const std::vector<long long>& fitnesses, std::mt19937& rng);

/**
 * @brief   Neighbor-list 2-opt with don't-look bits; improves tour to local optimum.
 * @details Mutates in place.
 */
void run_two_opt(std::vector<int>& tour, const Instance& instance);

/**
 * @brief   Computes percent error of fitness relative to known optimum.
 * @details Returns empty optional if instance has no known optimum.
 */
std::optional<double> compute_percent_error(long long fitness, const Instance& instance);

/**
 * @brief   Runs genetic algorithm on instance.
 * @details Stops at MAX_GENERATIONS, CONVERGENCE_GENERATIONS without improvement, or known optimum.
 *          Returns elite fitness, elite tour, and per-generation history.
 */
RunResult run_genetic_algorithm(const Instance& instance, std::mt19937& rng);
