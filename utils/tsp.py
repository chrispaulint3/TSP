"""
TSP problem definition and data loader
"""
import numpy as np
import pandas as pd


class Tsp:
    def __init__(self, path):
        """
        :param path: the tsp dataset path
        :param coordinate_x1:
        :param coordinate_y1:
        :param city_num:
        """
        # initialize the basic information in
        self.city_num = None
        self.x = None
        self.y = None
        self.id = None
        self.__ini_data(path=path)

        # distance map with n*n matrix
        self.distance_graph = self.__create_graph()
        self.fitness_list = []

    def __ini_data(self, path):
        df = pd.read_csv(path, header=None, sep=' ',names=["id","x","y"])
        self.x = df["x"]
        self.y = df["y"]
        self.id = df["id"]-1
        self.city_num = len(df)

    def __create_graph(self):
        x_mat = np.zeros((self.city_num,self.city_num))
        y_mat = np.zeros((self.city_num,self.city_num))
        for i in range(self.city_num):
            for j in range(i+1,self.city_num):
                x_mat[i][j] = np.power(self.x[i]-self.x[j],2)
                x_mat[j][i] = x_mat[i][j]
                y_mat[i][j] = np.power(self.y[i]-self.y[j],2)
                y_mat[j][i] = y_mat[i][j]
        return np.sqrt(x_mat+y_mat)

