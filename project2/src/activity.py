from igraph import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import warnings
from statistics import mean
import datetime
import math

BINS = 1
MAIN_EVENT_TIME = 1341360000

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



def get_first_index_from_time(time_value, activity_list):
    index = 0
    for activity in activity_list:
        index+=1
        if activity.timestamp >= time_value:
            return index



def get_closest_index(value, list):
    return min(range(len(list)), key=lambda i: abs(list[i]-value))



def plot_new_model_function(xs, ys_frac, starting_date, ending_date, activation_rate):
    period_index1 = get_closest_index(starting_date, xs)
    period_index2 = get_closest_index(ending_date, xs)

    period_lims = xs[period_index1:period_index2]
    initial_fraction = ys_frac[period_index1]

    plt.plot(period_lims, [1 - (1 - initial_fraction) * \
        math.exp(-activation_rate*(xi - starting_date)) for xi in period_lims], "--", color="r")



def plot_new_model_fit(xs, ys_frac):
    plt.figure()

    plt.plot(xs, ys_frac, marker=".", linestyle="", markersize=5)

    # Period I
    period_start = 0
    period_end = 0.62
    activation_rate = 0.0032
    plot_new_model_function(xs, ys_frac, period_start, period_end, activation_rate)


    # Period II
    period_start = 0.62
    period_end = 1.51
    activation_rate = 0.0168
    plot_new_model_function(xs, ys_frac, period_start, period_end, activation_rate)
    
    # Period III
    period_start = 1.51
    period_end = 3.21
    activation_rate = 0.0642
    plot_new_model_function(xs, ys_frac, period_start, period_end, activation_rate)
    
    # Period IV
    period_start = 3.21
    period_end = 7
    activation_rate = 1.3843
    plot_new_model_function(xs, ys_frac, period_start, period_end, activation_rate)

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
    


def plot_si_function(xs, ys_frac, starting_date, ending_date, activation_rate, avg_degree):
    
    period_index1 = get_closest_index(starting_date, xs)
    period_index2 = get_closest_index(ending_date, xs)

    period_lims = xs[period_index1:period_index2]
    initial_fraction = ys_frac[period_index1]

    tau = (activation_rate*avg_degree)**-1

    plt.plot(period_lims, [initial_fraction*math.exp(xi/tau) for xi in period_lims], "--", color="r")



def plot_si_fit(xs, ys_frac):
    plt.figure()

    plt.plot(xs, ys_frac, marker=".", linestyle="", markersize=5)

    avg_degree = 32.53

    # Period I
    period_start = 0
    period_end = 0.62
    activation_rate = 0.32
    plot_si_function(xs, ys_frac, period_start, period_end, activation_rate, avg_degree)


    # Period II
    period_start = 0.62
    period_end = 1.51
    activation_rate = 0.037
    plot_si_function(xs, ys_frac, period_start, period_end, activation_rate, avg_degree)
    
    # Period III
    period_start = 1.51
    period_end = 3.21
    activation_rate = 0.017
    plot_si_function(xs, ys_frac, period_start, period_end, activation_rate, avg_degree)
    
    # Period IV
    period_start = 3.21
    period_end = 7
    activation_rate = 0.01
    plot_si_function(xs, ys_frac, period_start, period_end, activation_rate, avg_degree)

    # Draw vertical lines
    plt.axvline(x=0.62, color="k", linestyle=":")
    plt.axvline(x=1.51, color="k", linestyle=":")
    plt.axvline(x=3.21, color="k", linestyle=":")

    # Annotations
    plt.annotate(xy=[0.16, 10**-5], s="Period I", size=9)
    plt.annotate(xy=[0.89, 10**-5], s="Period II", size=9)
    plt.annotate(xy=[2.14, 10**-5], s="Period III", size=9)
    plt.annotate(xy=[4.85, 10**-5], s="Period IV", size=9)
    

    plt.yscale("log")
    plt.xlabel("Days from 1st July 2012")
    plt.ylabel("Fraction of activated users")
    plt.xlim(xmin=0, xmax=7)
    
    plt.show()



# Plots activated users graphic
def plot_activated_users(activated_users):

    xs = [(activated_user.timestamp - activated_users[0].timestamp)/(60*60*24) for activated_user in activated_users]
    ys = range(1,len(activated_users)+1)
    ys_frac = [float(i)/(len(activated_users)+1) for i in ys]

    plot_si_fit(xs, ys_frac)
    plot_new_model_fit(xs, ys_frac)


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



def plot_active_user_density(activity_list):
    xs = []
    ys = []
    
    time_interval = 1800
    cur_time = MAIN_EVENT_TIME

    main_event_list = activity_list[get_first_index_from_time(cur_time, activity_list): \
    get_first_index_from_time(cur_time + 180000, activity_list)]
    
    n_active = 0
    activated_users = {}

    for activity in main_event_list:
        if activity.timestamp < (cur_time + time_interval):
            if  activity.userA not in activated_users:
                n_active += 1
                activated_users[activity.userA] = 1
            
        else:
            xs.append(cur_time)
            ys.append(n_active)
            cur_time = cur_time + time_interval
            n_active = 0
            activated_users = {}
    
    xs = [(xi - xs[0])/(60*60) for xi in xs]

    activated_users_list = build_activated_users(activity_list)
    ys_frac = [float(i)/(len(activated_users_list)+1) for i in ys]

    plt.plot(xs, ys_frac, marker="x", linestyle="", markersize=5)



def plot_deact_function(xs, starting_date, ending_date, cur_density, cur_activation, deact_rate, tau, activity_list):
    
    period_index1 = get_closest_index(starting_date, xs)
    period_index2 = get_closest_index(ending_date, xs)
    period_lims = xs[period_index1:period_index2+1]

    ys = [cur_density]

    for xi in period_lims[1:]:
        cur_activation = (1 - 1/tau)*cur_activation
        cur_density = (1 - deact_rate)*cur_density + (1 - cur_density)*cur_activation
        ys.append(cur_density)
    
    period_lims = [(xi - xs[0])/(60*60) for xi in period_lims]

    plt.plot(period_lims, ys, "--", color="r")



def plot_deact_fit(activity_list):
    xs = range(MAIN_EVENT_TIME, MAIN_EVENT_TIME + 180000, 3600)

    # Period I
    period_start = MAIN_EVENT_TIME + 11*1800
    period_end = MAIN_EVENT_TIME + 10*3600
    cur_density = 0.0207

    deact_rate = 0.533
    cur_activation = 0.063
    tau = 2.69
    plot_deact_function(xs, period_start, period_end, cur_density, cur_activation, deact_rate, tau, activity_list)
    plt.annotate(xy=[0.5, 0.045], s="Period I:\nβ={0}\nλ={1}\nτ={2}".format(deact_rate, cur_activation, tau), size=8)
    
    # Period II
    period_start = MAIN_EVENT_TIME + 10*3600
    period_end = MAIN_EVENT_TIME + 23*3600
    cur_density = 0.0236

    deact_rate = 0.197984
    cur_activation = 0.009019
    tau = 4.451927
    plot_deact_function(xs, period_start, period_end, cur_density, cur_activation, deact_rate, tau, activity_list)
    plt.annotate(xy=[10, 0.045], s="Period II:\nβ={0}\nλ={1}\nτ={2}".format(deact_rate, cur_activation, tau), size=8)

    # Period III
    period_start = MAIN_EVENT_TIME + 23*3600
    period_end = MAIN_EVENT_TIME + 27*3600
    cur_density = 0.00540

    deact_rate = 0.24
    cur_activation = 0.0085
    tau = 1.6
    plot_deact_function(xs, period_start, period_end, cur_density, cur_activation, deact_rate, tau, activity_list)
    plt.annotate(xy=[23.5, 0.045], s="Period III:\nβ={0}\nλ={1}\nτ={2}".format(deact_rate, cur_activation, tau), size=8)

    # Period IV
    period_start = MAIN_EVENT_TIME + 27*3600
    period_end = MAIN_EVENT_TIME + 34*3600
    cur_density = 0.00454

    deact_rate = 0.606195
    cur_activation = 0.005342
    tau = 10.86089
    plot_deact_function(xs, period_start, period_end, cur_density, cur_activation, deact_rate, tau, activity_list)
    plt.annotate(xy=[27.5, 0.045], s="Period IV:\nβ={0}\nλ={1}\nτ={2}".format(deact_rate, cur_activation, tau), size=8)

    # Period V
    period_start = MAIN_EVENT_TIME + 34*3600
    period_end = MAIN_EVENT_TIME + 50*3600
    cur_density = 0.00513

    deact_rate = 0.135945
    cur_activation = 0.002413
    tau = 3.700539
    plot_deact_function(xs, period_start, period_end, cur_density, cur_activation, deact_rate, tau, activity_list)
    plt.annotate(xy=[34.5, 0.045], s="Period V:\nβ={0}\nλ={1}\nτ={2}".format(deact_rate, cur_activation, tau), size=8)

    # Draw vertical lines
    plt.axvline(x=9.5, color="k", linestyle=":")
    plt.axvline(x=23, color="k", linestyle=":")
    plt.axvline(x=27, color="k", linestyle=":")
    plt.axvline(x=34, color="k", linestyle=":")



def plot_activity_density(activity_list):
    plt.figure()
    plot_active_user_density(activity_list)

    plot_deact_fit(activity_list)

    plt.xlabel("Time [hours]")
    plt.ylabel("Density of active users")
    plt.xlim(xmin=0, xmax=50)
    plt.ylim(ymin=0)

    plt.show()