from utils.tsp import Tsp
import random
import copy
import time


class Ga:
    def __init__(self, mutation_rate=0.3, cross_rate=0.5, gene_num=40, gene_length=100, step_length=100):
        self.step_length = step_length
        self.mutation_rate = mutation_rate
        self.cross_rate = cross_rate
        self.gene_num = gene_num
        self.gene_length = gene_length
        self.gene_set_p = self.initial_geneSet()  # 父辈基因列表
        self.gene_set_c = []  # 字辈基因列表
        self.city_info = Tsp(distance_x, distance_y, len(distance_x))
        self.fitness_list = []
        self.probability = []
        self.memory_point = []

    def initial_geneSet(self):
        temp = []
        for j in range(self.gene_num):
            gene = []
            for i in range(self.gene_length):
                gene.append(i)
                random.shuffle(gene)
            temp.append(gene)
        return temp

    def bear(self):
        gene1 = 0
        gene2 = 0
        while gene1 == gene2:
            gene1 = self.get_one()
            gene2 = self.get_one()
        position = random.randrange(0, self.gene_length)
        child = self.gene_set_p[gene1][0:position] + self.gene_set_p[gene2]
        child1 = []
        for i in child:
            if i not in child1:
                child1.append(i)
        self.gene_set_c.append(child1)

    def mutation(self):
        position1 = 0
        position2 = 0
        while position1 == position2:
            position1 = random.randrange(0, self.gene_length)
            position2 = random.randrange(0, self.gene_length)
        temp = self.gene_set_c[-1][position1]
        self.gene_set_c[-1][position1] = self.gene_set_c[-1][position2]
        self.gene_set_c[-1][position2] = temp

    def fitness_function(self, path, distance_graph):
        distance = 0.0
        for i in range(self.city_info.city_num - 1):
            start, end = path[i], path[i + 1]
            distance += distance_graph[start][end]
        distance += distance_graph[self.city_info.city_num - 1][0]
        self.fitness_list.append(distance)
        return 100000 / distance

    def calc_probability(self):
        temp = []
        total_score = 0.0
        for i in range(self.gene_num):
            score = self.fitness_function(self.gene_set_p[i], self.city_info.distance_graph)
            temp.append(score)
            total_score += score
        for i in range(self.gene_num):
            self.probability.append(temp[i] / total_score)

    def get_one(self):
        selection_total = 0.0
        b = random.random()
        for i in range(len(self.probability)):
            selection_total += self.probability[i]
            if selection_total >= b:
                return i

    def find_the_best(self):
        temp = self.fitness_list[0]
        index = 0
        for i in range(len(self.fitness_list)):
            if self.fitness_list[i] <= temp:
                index = i
                temp = self.fitness_list[i]
        return index

    def find_better_parent(self, num):
        index_all = []
        data_store = []
        while len(index_all) < num:
            b = min(self.fitness_list)
            index = self.fitness_list.index(b)
            index_all.append(index)
            data_store.append(self.fitness_list[index])
            self.fitness_list[index] = float("inf")
            j = 0
        for i in index_all:
            self.fitness_list[i] = data_store[j]
            j += 1
        return index_all


def life_cycle(iterate_time):
    gene = Ga(gene_length=len(distance_x))
    for i in range(iterate_time):
        gene.fitness_list.clear()
        gene.calc_probability()
        while len(gene.gene_set_c) < gene.gene_num:
            best_parent = gene.find_the_best()
            gene.gene_set_c.append(gene.gene_set_p[best_parent])
            gene.bear()
            random_value = random.random()
            if random_value < gene.mutation_rate:
                gene.mutation()
        gene.gene_set_p = copy.deepcopy(gene.gene_set_c)
        gene.gene_set_c.clear()
        gene.probability.clear()
    return gene


def life_cycle_new(iterate_time):
    gene = Ga(gene_length=len(distance_x))
    for i in range(iterate_time):
        gene.fitness_list.clear()
        gene.calc_probability()
        while len(gene.gene_set_c) < gene.gene_num:
            best_parent = gene.find_the_best()
            gene.gene_set_c.append(gene.gene_set_p[best_parent])
            gene.bear()
            random_value = random.random()
            if random_value < gene.mutation_rate:
                gene.mutation()
        gene.gene_set_p = copy.deepcopy(gene.gene_set_c)
        gene.gene_set_c.clear()
        gene.probability.clear()
        if i == 0:
            gene.memory_point.append(gene.fitness_list[best_parent])
        elif i % 100 == 0:
            gene.memory_point.append(gene.fitness_list[best_parent])
            if abs(gene.memory_point[-1] - gene.memory_point[-2]) / gene.memory_point[-2] < 0.03:
                break
    return gene



