# Phoenix Logs Analyzer

Tools to download and analyze phoenix replays from tenhou.net.

In order to work with these replays, you need to first download the IDs for each replay you want to analyze, then fetch the corresponding replays from tenhou.net.
For a whole year's amount of replays, the first step usually takes a few minutes, and the second step a few hours.

# Installation

Install [Anaconda](https://www.anaconda.com/) first if you don't have Anaconda/Miniconda already installed.
Then, run the following command to fetch IDs of replays from 2018.

`$ anaconda-project run`

# Download log IDs

To download log IDs for 2009 (keep in mind that phoenix games started only since 2009).

`$ python main.py -a id -y 2009`

To download games from January 1 of current year to (current day - 7 days), specify `-s` flag:

`python main.py -a id -s`

As of early August 2019, the archive of game IDs for 2018 was still not available. To bypass this problem, use both -s and -y:

`python main.py -a id -s -y 2018`

To download log IDs from last 7 days:

`python main.py -a id`

# Download log content

To download log content for existing IDs:

`python main.py -a content -y 2009 -l 50 -t 3`

Where `-l` specifies how many game logs to download and `-t` specifies the number of threads.

# Data consistency checking

The log content often can't be properly downloaded due to various reasons, such as connection issues or tenhou server problems. Tenhou server sometimes return the log content for the wrong game.
And sometimes tenhou return for log A content from log B and it causes same log content for different log ids in our db.

To fix these issues:

`python debug.py -y 2009`

The command will detect and mark all broken log IDs for the given year. You may then re-run the command for downloading log content.

# Unofficial Tenhou XML documentation

- [Part 1](https://blog.kobalab.net/entry/20170225/1488036549)
- [Part 2](https://blog.kobalab.net/entry/20170228/1488294993)
