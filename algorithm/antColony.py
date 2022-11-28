# 最大最小蚁群算法
# 记录每次基因算法迭代后最适函数变化值
from utils.tsp import Tsp
import random


class AntColony(Tsp):
    def __init__(self, path,pheromone_max=10, pheromone_min=0.5,
                 iterate_time=20, alpha=3, beta=12, Q=3, ant_num=40, p=0.2):
        """
        初始化算法参数
        init the algorithm parameters
        :param path: 数据集路径
        :param pheromone_max: 信息素最大值
        :param pheromone_min: 信息素最小值
        :param iterate_time: 迭代次数
        :param alpha: 信息因素启发因子
        :param beta: 路径距离启发因子
        :param Q: 信息素释放常数
        :param ant_num: 蚁群数量
        :param p: 信息素挥发因子
        """
        super().__init__(path)

        # 算法参数定义
        self.pheromone_max = pheromone_max
        self.pheromone_min = pheromone_min
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.P = p
        self.iterate_time = iterate_time
        self.ant_num = ant_num

        # 算法数据结构定义
        self.tabooList = [True for i in range(self.city_num)]
        self.current_city = -1
        # 蚁群信息素矩阵
        self.pheromone_graph = [[self.pheromone_max for i in range(self.city_num)]
                                for j in range(self.city_num)]
        # 记录单一蚂蚁的路径值
        self.each_path = []
        # 记录所有蚂蚁的路径
        self.all_path = []
        # 记录转移概率
        self.probability = []
        self.distance_list = []
        self.best_path = None
        self.best_distance = None

    def initial_position(self):
        position = random.randrange(0, self.city_num)
        self.tabooList = [True for i in range(self.city_num)]
        self.tabooList[position] = False
        self.current_city = position

    def transfer_to_next(self):
        # 计算转移到每座城市的概率
        transfer_index = []
        counter = 0
        for i in self.tabooList:
            if i:
                transfer_index.append(counter)
            counter += 1
        each_value = []
        for i in range(len(transfer_index)):
            p = pow(self.pheromone_graph[self.current_city][transfer_index[i]], self.alpha) * \
                pow(1 / self.distance_graph[self.current_city][transfer_index[i]], self.beta)
            each_value.append(p)
        total_value = sum(each_value)  # 算总和
        for i in range(len(each_value)):
            self.probability.append(each_value[i] / total_value)
        # 轮盘赌算法，根据概率寻找下一座城市
        random_value = random.random()
        selection_total = 0.0
        city_index = -1
        for i in range(len(self.probability)):
            selection_total += self.probability[i]
            if selection_total >= random_value:
                city_index = i
                break
        self.current_city = transfer_index[city_index]
        self.each_path.append(self.current_city)
        self.tabooList[self.current_city] = False
        self.probability.clear()

    def travel(self):
        for i in range(self.iterate_time):
            for j in range(self.ant_num):
                self.initial_position()
                self.each_path.append(self.current_city)
                while self.test_tabooList():
                    self.transfer_to_next()
                self.all_path.append(self.each_path)
                self.each_path = []
            k = self.find_the_best()  # 第k只蚂蚁是最优蚂蚁
            self.best_path = self.all_path[k]
            self.best_distance = self.distance_list[k]
            self.update_pheromone(self.best_path)
            self.all_path.clear()
            self.distance_list.clear()

    def test_tabooList(self):
        for i in range(len(self.tabooList)):
            if self.tabooList[i]:
                return True
        return False

    def fitness_function(self, path, distance_graph):
        distance = 0.0
        for i in range(self.city_num - 1):
            start, end = path[i], path[i + 1]
            distance += distance_graph[start][end]
        distance += distance_graph[self.city_num - 1][0]
        self.distance_list.append(distance)
        return distance

    def find_the_best(self):
        score = self.fitness_function(self.all_path[0], self.distance_graph)
        index = 0
        for i in range(1, len(self.all_path)):
            temp = self.fitness_function(self.all_path[i], self.distance_graph)
            if temp < score:
                score = temp
                index = i
        return index

    def update_pheromone(self, path):
        for i in range(self.city_num):
            for j in range(self.city_num):
                self.pheromone_graph[i][j] = (1 - self.P) * self.pheromone_graph[i][j]
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            # 蚁量模型改为蚁周模型
            # delta_pheromone = self.Q / self.city_info.distance_graph[start][end]
            delta_pheromone = self.Q
            self.pheromone_graph[start][end] += delta_pheromone
        for i in range(self.city_num):
            for j in range(self.city_num):
                if self.pheromone_graph[i][j] > self.pheromone_max:
                    self.pheromone_graph[i][j] = self.pheromone_max
                if self.pheromone_graph[i][j] < self.pheromone_min:
                    self.pheromone_graph[i][j] = self.pheromone_min

    def update_use_path(self, path):
        for i in range(len(self.pheromone_graph) - 1):
            self.pheromone_graph[path[i]][path[i + 1]] += 4
        self.pheromone_graph[-1][0] += 4

if __name__ =="__main__":
    ant = AntColony("../assets/kroA100.tsp")
    ant.travel()
    print(ant.best_distance)