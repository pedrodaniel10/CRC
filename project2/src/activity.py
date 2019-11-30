from igraph import *
import numpy as np
import matplotlib.pyplot as plt
import warnings
from statistics import mean
import datetime
import math

BINS = 1

class Activity:
    def __init__(self, userA, userB, timestamp, interaction):
        self.userA = userA
        self.userB = userB
        self.timestamp = timestamp
        self.interaction = interaction
        self.activated = 0
    
    def __str__(self):
        return "Activity: {0} {1} {2} {3}".format(self.userA, self.userB, self.timestamp, self.interaction)



# Parses higgs-activity_time dataset
def parse_activity_time(dataset):
    activity_list = []
    with open(dataset) as fin:
            for line in fin:
                attrs = line.split()
                activity_list.append(Activity(int(attrs[0]), int(attrs[1]), int(attrs[2]), attrs[3]))
    return activity_list



# Builds activity_list
def build_activated_users(activity_list):
    activated_users = {}
    for activity in activity_list:
        if activity.userA not in activated_users:
            activated_users[activity.userA] = 1
            activity.activated = 1
    activity_list = [activity for activity in activity_list if activity.activated == 1]
    return activity_list



def plot_infection_function(x, starting_date, initial_fraction, activation_rate):

    plt.plot(x, 1 - (1 - initial_fraction) * math.exp(-activation_rate*(x - starting_date)), "-")


# Plots activated users graphic
def plot_activated_users(activated_users):
    plt.figure()

    xs = [(activated_user.timestamp - activated_users[0].timestamp)/(60*60*24) for activated_user in activated_users]
    ys = range(1,len(activated_users)+1)
    ys_frac = [float(i)/(len(activated_users)+1) for i in ys]

    plt.plot(xs, ys_frac, marker=".", linestyle="", markersize=2)

    #plot_infection_function(xs, 3.23541, 0.15685, 519.14)

    plt.yscale("log")
    plt.xlabel("Days from 1st July 2012")
    plt.ylabel("Fraction of activated users")
    plt.show()
