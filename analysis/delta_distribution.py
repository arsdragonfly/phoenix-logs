# -*- coding: utf-8 -*-

from log_counter import LogCounter

class DeltaDistribution(LogCounter):
    def ParseLog(self, log, log_id):
        wins = log.findall('AGARI')
        double_ron = False

        for win in wins:
            if double_ron == True:
                double_ron == False
                continue
            
            for score in get_scores(win):
                self.Count(score)

            if win.attrib['who'] != win.attrib['fromWho']:
                next_element = win.getnext()
                if next_element is not None and next_element.tag == "AGARI":
                    double_ron = True
        
        draws = log.findall('RYUUKYOKU')

        for draw in draws:
            for score in get_scores(draw):
                self.Count(score)

    def GetName(self):
        return "Delta Distribution"

def get_scores(game):
    return [int(score) for score in game.attrib['sc'].split(',')[1::2]]