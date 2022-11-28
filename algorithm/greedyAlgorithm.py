import tsp
import random
from dataInterface import *


class greedy_algorithm:
    def __init__(self):
        # 初始化tsp模型
        self.city_info = tsp.Tsp(coordinate_x1=distance_x, coordinate_y1=distance_y, city_num=len(distance_x))
        # 初始化禁忌表
        self.tabooList = [True for i in range(self.city_info.city_num)]
        # 记录最适值
        self.fitness_value = 0
        # 记录最优路径
        self.path = []

    def search_func(self, start_city):
        temp_start = start_city
        path = [start_city]
        self.tabooList[start_city] = False
        while self.test_tabooList():
            temp_distance = []
            temp_index = []
            for i in range(len(self.tabooList)):
                if self.tabooList[i]:
                    temp_distance.append(self.city_info.distance_graph[temp_start][i])
                    temp_index.append(i)
            next_city = temp_index[find_the_best(temp_distance)]
            self.tabooList[next_city] = False
            temp_start = next_city
            path.append(next_city)
        return path

    def search_all_city(self):
        value = float('inf')
        temp_path = []
        for i in range(self.city_info.city_num):
            self.tabooList = [True for i in range(self.city_info.city_num)]
            path = self.search_func(i)
            value_of_path = self.fitness_function(path, self.city_info.distance_graph)
            if value_of_path < value:
                value = value_of_path
                temp_path = path
        self.fitness_value = value
        self.path = temp_path
        return temp_path

    def search_FromRandomCity(self):
        start_city = random.randrange(self.city_info.city_num)
        temp_start = start_city
        path = [start_city]
        self.tabooList[start_city] = False
        while self.test_tabooList():
            temp_distance = []
            temp_index = []
            for i in range(len(self.tabooList)):
                if self.tabooList[i]:
                    temp_distance.append(self.city_info.distance_graph[temp_start][i])
                    temp_index.append(i)
            next_city = temp_index[find_the_best(temp_distance)]
            self.tabooList[next_city] = False
            temp_start = next_city
            path.append(next_city)
            self.fitness_value = self.fitness_function(path)
            self.path = path

    def test_tabooList(self):
        for i in self.tabooList:
            if i:
                return True
        return False

    def fitness_function(self, path, distance_graph):
        distance = 0.0
        for i in range(self.city_info.city_num - 1):
            start, end = path[i], path[i + 1]
            distance += distance_graph[start][end]
        distance += distance_graph[self.city_info.city_num - 1][0]
        return distance


def find_the_best(nextCity_list):
    index = 0
    value = nextCity_list[0]
    for i in range(1, len(nextCity_list)):
        if nextCity_list[i] <= value:
            value = nextCity_list[i]
            index = i
    return index


def execute_greedy():
    greedy = greedy_algorithm()
    start = random.randrange(greedy.city_info.city_num)
    path = greedy.search_func(start)
    greedy.path = path
    greedy.fitness_value = greedy.fitness_function(path,greedy.city_info.distance_graph)
    return greedy


def execute_greedy_all():
    greedy = greedy_algorithm()
    greedy.search_all_city()
    return greedy
