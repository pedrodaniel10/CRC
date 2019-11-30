from igraph import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
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
    activated_users = [activity for activity in activity_list if activity.activated == 1]
    return activated_users



def get_closest_index(value, list):
    return min(range(len(list)), key=lambda i: abs(list[i]-value))



def plot_infection_function(xs, ys_frac, starting_date, ending_date, activation_rate, color):
    period_index1 = get_closest_index(starting_date, xs)
    period_index2 = get_closest_index(ending_date, xs)

    period_lims = xs[period_index1:period_index2]
    initial_fraction = ys_frac[period_index1]

    plt.plot(period_lims, [1 - (1 - initial_fraction) * math.exp(-activation_rate*(xi - starting_date)) for xi in period_lims], "--", color=color)



# Plots activated users graphic
def plot_activated_users(activated_users):
    plt.figure()

    xs = [(activated_user.timestamp - activated_users[0].timestamp)/(60*60*24) for activated_user in activated_users]
    ys = range(1,len(activated_users)+1)
    ys_frac = [float(i)/(len(activated_users)+1) for i in ys]

    plt.plot(xs, ys_frac, marker=".", linestyle="", markersize=5)

    # Period I
    period_start = 0
    period_end = 0.62
    activation_rate = 0.0032
    plot_infection_function(xs, ys_frac, period_start, period_end, activation_rate, "r")


    # Period II
    period_start = 0.62
    period_end = 1.51
    activation_rate = 0.0168
    plot_infection_function(xs, ys_frac, period_start, period_end, activation_rate, "r")
    
    # Period III
    period_start = 1.51
    period_end = 3.21
    activation_rate = 0.0642
    plot_infection_function(xs, ys_frac, period_start, period_end, activation_rate, "r")
    
    # Period IV
    period_start = 3.21
    period_end = 7
    activation_rate = 1.3843
    plot_infection_function(xs, ys_frac, period_start, period_end, activation_rate, "r")

    # Draw vertical lines
    plt.axvline(x=0.62, color="k", linestyle=":")
    plt.axvline(x=1.51, color="k", linestyle=":")
    plt.axvline(x=3.21, color="k", linestyle=":")

    # Annotations
    plt.annotate(xy=[0.16, 10**-5], s="Period I", size=9)
    plt.annotate(xy=[0.89, 10**-5], s="Period II", size=9)
    plt.annotate(xy=[2.14, 10**-5], s="Period III", size=9)
    plt.annotate(xy=[4.85, 10**-5], s="Period IV", size=9)
    
    plt.annotate(xy=[0.16, 3*10**-4], s="    " + "0.192" + "\nusers/min", size=6)
    plt.annotate(xy=[0.87, 3.3*10**-3], s="    " + "1.008" + "\nusers/min", size=6)
    plt.annotate(xy=[2.06, 2.1*10**-2], s="    " + "3.852" + "\nusers/min", size=6)
    plt.annotate(xy=[3.88, 2.9*10**-1], s="   " + "83.058" + "\nusers/min", size=6)
    

    plt.yscale("log")
    plt.xlabel("Days from 1st July 2012")
    plt.ylabel("Fraction of activated users")
    plt.xlim(xmin=0, xmax=7)
    
    plt.show()



def plot_actions_psec(actions_list, line_style):
    xs = []
    ys = []
    cur_time = actions_list[0].timestamp
    n_actions = 0
    for action in actions_list:
        if action.timestamp < (cur_time + 10800):
            n_actions += 1
            
        else:
            interval = action.timestamp - cur_time
            xs.append(cur_time)
            ys.append(n_actions/interval)
            cur_time = action.timestamp
            n_actions = 0
    
    xs = [(xi - xs[0])/(60*60*24) for xi in xs]

    plt.plot(xs, ys, line_style)



def filter_action_type(activity_list, action_type):
    return [activity for activity in activity_list if activity.interaction == action_type]



def plot_activity_psec(activity_list):
    plt.figure()

    plot_actions_psec(activity_list, "-")
    plot_actions_psec(filter_action_type(activity_list, "RT"), "--")
    plot_actions_psec(filter_action_type(activity_list, "RE"), "-.")
    plot_actions_psec(filter_action_type(activity_list, "MT"), ":")

    any_legend = mlines.Line2D([], [], color='blue', ls='-', markersize=5, label='Any interaction')
    retweet_legend = mlines.Line2D([], [], color='orange', ls='--', markersize=5, label='Retweets')
    reply_legend = mlines.Line2D([], [], color='green', ls='-.', markersize=5, label='Replies')
    mention_legend = mlines.Line2D([], [], color='red', ls=':', markersize=5, label='Mentions')

    plt.legend(handles=[any_legend, retweet_legend, mention_legend, reply_legend])


    plt.yscale("log")
    plt.xlabel("Days from 1st July 2012")
    plt.ylabel("# of interactions / sec")
    plt.xlim(xmin=0, xmax=7)

    plt.show()