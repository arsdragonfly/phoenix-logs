# -*- coding: utf-8 -*-
from log_count_and_max import LogCountAndMax

class MostRiichi(LogCountAndMax):
    def ParseLog(self, log, log_id):
        round_ends = log.findall('AGARI') + log.findall('RYUUKYOKU')
        most = 0
        for end in round_ends:
            honba = int(end.attrib["ba"].split(",")[1])
            most = max(most, honba)

        self.Count(most, log_id)
        
    def GetName(self):
        return "Riichi Sticks In Pot"