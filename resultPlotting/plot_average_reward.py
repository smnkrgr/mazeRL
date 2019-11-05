import csv
import matplotlib.pyplot as plt
import numpy as np


def readAverageRewardsFromCSV(path):

    average_rewards = []
    with open(path) as datafile:
        datafile_reader = csv.reader(datafile, delimiter = ",")
        for row in datafile_reader:
            average_rewards.append(np.array(row).astype(np.float))

    return average_rewards

if __name__ == '__main__':

    average_rewards = readAverageRewardsFromCSV("average_rewards.csv")

    plt.plot(average_rewards[0], label = r'$\alpha = 0.3$, $\epsilon = 0.1$, $\gamma = 1.0$') 
    plt.plot(average_rewards[1], label = r'$\alpha = 0.8$, $\epsilon = 0.1$, $\gamma = 1.0$') 

    plt.legend(loc='lower right')
    plt.show()

