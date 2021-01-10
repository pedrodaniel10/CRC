# CRC - 2019/2020 - Project 2
Complex Network's project.

## Requirements
- GNU/Linux
- Python 3+
- igraph 0.7+
- pycairo

## How to run
To run the analysis of the 5 datasets:

```bash
    python3 ./main.py <dataset>
```

The name of the datasets can not be changed. It must be named in the following manner:
- higgs-social_network.edgelist
- higgs-retweet_network.edgelist
- higgs-reply_network.edgelist
- higgs-mention_network.edgelist
- higgs-activity_time.txt

It is worth noting that the weights in higgs-reply_network.edgelist were removed from dataset.

To run the coreness plot:
```bash
    python3 ./coreness.py
```
It expects that the file __**higgs-social_network.edgelist**__ is in the same directory where the program is executed.