# -*- coding: utf-8 -*-
# This script is for running multiple analyses at once,
# to avoid reading the db and decompressing each log multiple times.

import bz2
import sqlite3
from lxml import etree
from tqdm import tqdm
from call_rate_by_round import CallRateByRound
from dealin_rate_by_round import DealInRateByRound
from value_by_round import ValueByRound
from yaku_by_round import YakuByRound
from riichi_by_round import RiichiByRound
from end_results import EndResults
from delta_distribution import DeltaDistribution

analyzers = [DeltaDistribution()]
allowed_types = [
    "169",  # 4p houou hanchan
    # "225",  # 4p houou tonpuusen
    # "185",  # 3p houou
]

with sqlite3.connect('../db/2018.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM logs')
    rowcount = cursor.fetchone()[0]
    cursor.execute(
        'SELECT log_content, log_id FROM logs WHERE log_content != ""')

    for i in tqdm(range(rowcount), ncols=80, ascii=True):
        log = cursor.fetchone()
        if log is None:
            break

        content = bz2.decompress(log[0])
        xml = etree.XML(content, etree.XMLParser(
            recover=True)).getroottree().getroot()
        # print(etree.tostring(xml, pretty_print=True).decode('unicode-escape'))
        # break

        game_type = xml.find("GO").attrib["type"]

        if game_type in allowed_types:
            for analyzer in analyzers:
                analyzer.ParseLog(xml, log[1])

for analyzer in analyzers:
    print("==========")
    analyzer.PrintResults()
