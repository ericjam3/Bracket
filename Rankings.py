from math import *
import math

class Rankings:

    def __init__(self):
        infile = open("results.txt", "r")
        lineNum = 0
        self.players = {}

        for item in infile:
            line = item[0:-1]
            if lineNum == 0:
                self.numPlayers = int(line)
                count = int(line)
                self.table = []
                for i in range(self.numPlayers):
                    row = [0] * self.numPlayers
                    self.table.append(row)
                lineNum = 1
            elif lineNum == 1:
                count -= 1
                if count == 0:
                    lineNum = 2

                players = line.split("  ")
                id = int(players[1]) - 1
                self.players[id] = {}
                self.players[id]["name"] = players[0]
                self.players[id]["wins"] = 0.0
                self.players[id]["totals"] = 0.0
                self.players[id]["losses"] = 0.0
                self.players[id]["nlosses"] = 0.0
                self.players[id]["nwins"] = 0.0
                self.players[id]["score"] = 1.0 / self.numPlayers
                self.players[id]["newscore"] = 1.0 / self.numPlayers
            elif lineNum == 2:
                results = line.split(",")
                win = int(results[0]) - 1
                loss = int(results[1]) - 1
                self.table[win][loss] += 1
                self.players[win]["wins"] += 1
                self.players[loss]["losses"] += 1
                self.players[loss]["totals"] += 1


        infile.close()

    def save(self):
        outfile = open("results.txt", "w")
        print_var = str(self.numPlayers) + "\n"
        for key, value in self.players.iteritems():
            print_var += str(int(key) + 1)  + "  " + str(value) + "\n"

        for row in range(self.numPlayers):
            for col in range(self.numPlayers):
                count = self.table[row][col]
                for i in range(count):
                    print_var += str(row + 1) + "," + str(col + 1) + ",0,0\n"
        outfile.write(print_var)
        outfile.close()

    def pagerank(self):
        for col in range(self.numPlayers):
            loss = False
            for row in range(self.numPlayers):
                if self.table[row][col] != 0:
                    loss = True
            if loss == False:
                print "here"
                for row in range(self.numPlayers):
                    if row != col:
                        self.table[row][col] = 1
                        self.players[row]["wins"] += 1
                        self.players[col]["losses"] += 1

        for count in range(10):
            for row in range(self.numPlayers):
                score = 0
                for col in range(self.numPlayers):
                    score += self.table[row][col] * self.players[col]["score"] / self.players[col]["totals"]

                self.players[row]["newscore"] = score

            for key, value in self.players.iteritems():
                value["score"] = value["newscore"]

        max = 0
        for key, value in self.players.iteritems():
            if value["wins"] + value["losses"] > max:
                max = value["wins"] + value["losses"]

        rankDict = {}
        for key, value in self.players.iteritems():
            rankDict[value["name"]] = value["score"] * (max / (value["wins"] + value["losses"]))
            if rankDict[value["name"]] < .001:
                rankDict[value["name"]] = math.pow(rankDict[value["name"]], .2)

        return rankDict

    def hits(self):
        for count in range(1):
            for row in range(self.numPlayers):
                scorewins = 0
                scorelosses = 0
                for col in range(self.numPlayers):
                    if self.players[col]["losses"] > 0:
                        scorewins += self.table[row][col]/self.players[col]["losses"]
                    if self.players[col]["wins"] > 0:
                        scorelosses += self.table[col][row]/self.players[col]["wins"]

                self.players[row]["nwins"] = scorewins
                self.players[row]["nlosses"] = scorelosses

            for key, value in self.players.iteritems():
                value["wins"] = value["nwins"]
                value["losses"] = value["nlosses"]

        den = 0
        for key, value in self.players.iteritems():
            den += value["wins"]

        rankDict = {}
        tot = 0
        for key, value in self.players.iteritems():
            rankDict[value["name"]] = (value["wins"] - value["losses"]) / den
            tot += rankDict[value["name"]]

        return rankDict


if __name__ == "__main__":
    obj = Rankings()
    pageDict = obj.pagerank()
    hitsDict = obj.hits()

    rankDict = {}
    for key in pageDict:
        rankDict[key] = pageDict[key] + (1 * hitsDict[key])
        #rankDict[key] = hitsDict[key]
        #rankDict[key] = pageDict[key]

    print_var = ""
    rank = len(rankDict)
    for key, value in sorted(rankDict.iteritems(), key=lambda (v, k): (k, v)):
        print_var = str(rank).ljust(6) + str(key).ljust(20) + str(round(value,3)).ljust(10) + "\n" + print_var
        rank -= 1

    print "RANK".ljust(6) + "NAME".ljust(20) + "RATING".ljust(10)
    print print_var
