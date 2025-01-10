import csv
import predict
import team
import copy
import mysql.connector
import datetime

#connecting to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aa531491",
    database = "test"
)

YEAR = 2017

mycursor = mydb.cursor()
def importGames():
    #we need to check if the table for this season exists
    sql = "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'test') AND (TABLE_NAME = 'bb" + str(YEAR) + "')"
    mycursor.execute(sql)
    for x in mycursor:
        print(x[0])
        if x[0]==0:
            print("Season has not been imported or cannot be found; terminating program")
            exit()
    mycursor.execute("SELECT * FROM bb" + str(YEAR))
    myresult = mycursor.fetchall()
    return myresult

def initializeTeams():
    teamDict = dict([])
    teamDict["ATL"] = team.Team("ATL", 0, 0, 0, 0, 0, 0, 1, "Atlanta Hawks")
    teamDict["BOS"] = team.Team("BOS", 0, 0, 0, 0, 0, 0, 0, "Boston Celtics")
    teamDict["CHO"] = team.Team("CHO", 0, 0, 0, 0, 0, 0, 0, "Charlotte Hornets")
    teamDict["CHI"] = team.Team("CHI", 0, 0, 0, 0, 0, 0, 2, "Chicago Bulls")
    teamDict["CLE"] = team.Team("CLE", 0, 0, 0, 0, 0, 0, 1, "Cleveland Cavaliers")
    teamDict["DAL"] = team.Team("DAL", 0, 0, 0, 0, 0, 1, 2, "Dallas Mavericks")
    teamDict["DEN"] = team.Team("DEN", 0, 0, 0, 0, 0, 1, 0, "Denver Nuggets")
    teamDict["DET"] = team.Team("DET", 0, 0, 0, 0, 0, 0, 0, "Detroit Pistons")
    teamDict["GSW"] = team.Team("GSW", 0, 0, 0, 0, 0, 1, 2, "Golden State Warriors")
    teamDict["HOU"] = team.Team("HOU", 0, 0, 0, 0, 0, 1, 2, "Houston Rockets")
    teamDict["IND"] = team.Team("IND", 0, 0, 0, 0, 0, 0, 1, "Indiana Pacers")
    teamDict["LAC"] = team.Team("LAC", 0, 0, 0, 0, 0, 1, 1, "Los Angeles Clippers")
    teamDict["LAL"] = team.Team("LAL", 0, 0, 0, 0, 0, 1, 0, "Los Angeles Lakers")
    teamDict["MEM"] = team.Team("MEM", 0, 0, 0, 0, 0, 1, 1, "Memphis Grizzlies")
    teamDict["MIA"] = team.Team("MIA", 0, 0, 0, 0, 0, 0, 1, "Miami Heat")
    teamDict["MIL"] = team.Team("MIL", 0, 0, 0, 0, 0, 0, 0, "Milwaukee Bucks")
    teamDict["MIN"] = team.Team("MIN", 0, 0, 0, 0, 0, 1, 1, "Minnesota Timberwolves")
    teamDict["NOP"] = team.Team("NOP", 0, 0, 0, 0, 0, 1, 1, "New Orleans Pelicans")
    teamDict["NYK"] = team.Team("NYK", 0, 0, 0, 0, 0, 0, 0, "New York Knicks")
    teamDict["BRK"] = team.Team("BRK", 0, 0, 0, 0, 0, 0, 2, "Brooklyn Nets")
    teamDict["OKC"] = team.Team("OKC", 0, 0, 0, 0, 0, 1, 1, "Oklahoma City Thunder")
    teamDict["ORL"] = team.Team("ORL", 0, 0, 0, 0, 0, 0, 0, "Orlando Magic")
    teamDict["PHI"] = team.Team("PHI", 0, 0, 0, 0, 0, 0, 2, "Philadelphia 76ers")
    teamDict["PHO"] = team.Team("PHO", 0, 0, 0, 0, 0, 1, 2, "Phoenix Suns")
    teamDict["POR"] = team.Team("POR", 0, 0, 0, 0, 0, 1, 2, "Portland Trailblazers")
    teamDict["SAC"] = team.Team("SAC", 0, 0, 0, 0, 0, 1, 2, "Sacramento Kings")
    teamDict["SAS"] = team.Team("SAS", 0, 0, 0, 0, 0, 1, 0, "San Antonio Spurs")
    teamDict["TOR"] = team.Team("TOR", 0, 0, 0, 0, 0, 0, 1, "Toronto Raptors")
    teamDict["UTA"] = team.Team("UTA", 0, 0, 0, 0, 0, 1, 0, "Utah Jazz")
    teamDict["WAS"] = team.Team("WAS", 0, 0, 0, 0, 0, 0, 0, "Washington Wizards")
    
    teamDict["Atlanta Hawks"] = teamDict["ATL"]
    teamDict["Boston Celtics"] = teamDict["BOS"]
    teamDict["Charlotte Hornets"] = teamDict["CHO"]
    teamDict["Chicago Bulls"] = teamDict["CHI"]
    teamDict["Cleveland Cavaliers"] = teamDict["CLE"]
    teamDict["Dallas Mavericks"] = teamDict["DAL"]
    teamDict["Denver Nuggets"] = teamDict["DEN"]
    teamDict["Detroit Pistons"] = teamDict["DET"]
    teamDict["Golden State Warriors"] = teamDict["GSW"]
    teamDict["Houston Rockets"] = teamDict["HOU"]
    teamDict["Indiana Pacers"] = teamDict["IND"]
    teamDict["Los Angeles Clippers"] = teamDict["LAC"]
    teamDict["Los Angeles Lakers"] = teamDict["LAL"]
    teamDict["Memphis Grizzlies"] = teamDict["MEM"]
    teamDict["Miami Heat"] = teamDict["MIA"]
    teamDict["Milwaukee Bucks"] = teamDict["MIL"]
    teamDict["Minnesota Timberwolves"] = teamDict["MIN"]
    teamDict["New Orleans Pelicans"] = teamDict["NOP"]
    teamDict["New York Knicks"] = teamDict["NYK"]
    teamDict["Brooklyn Nets"] = teamDict["BRK"]
    teamDict["Oklahoma City Thunder"] = teamDict["OKC"]
    teamDict["Orlando Magic"] = teamDict["ORL"]
    teamDict["Philadelphia 76ers"] = teamDict["PHI"]
    teamDict["Phoenix Suns"] = teamDict["PHO"]
    teamDict["Portland Trail Blazers"] = teamDict["POR"]
    teamDict["Sacramento Kings"] = teamDict["SAC"]
    teamDict["San Antonio Spurs"] = teamDict["SAS"]
    teamDict["Toronto Raptors"] = teamDict["TOR"]
    teamDict["Utah Jazz"] = teamDict["UTA"]
    teamDict["Washington Wizards"] = teamDict["WAS"] 
    
    #printResults(list(teamDict.values()))
    
    return teamDict


def handleSchedule(games,tDict, unfinished):
    print(datetime.datetime.now().strftime('\nStandings estimations as of %m/%d/%Y \n'))
    for i in range(0, len(games)):      #go through all games
        if games[i][2]!='@':           #to avoid double counting, we only look at away games ("@" is shorter than "Home")
            continue
        if games[i][6]==games[i][5]:    #append uncompleted games to the list of games to be sim
            unfinished.append(games[i])
            continue

        #otherwise, we record the result of each game and the runs for each team
        teamA = games[i][-2]
        teamB = games[i][3]
        AScore = int(games[i][5])
        BScore = int(games[i][6])

        #we gotta check score directly instead of the "results" column, bc W/L symbols are weird and I don't want to clean it
        if AScore>BScore:
            tDict[teamA].wins+=1
            tDict[teamB].losses+=1
        elif AScore<BScore:
            tDict[teamB].wins+=1
            tDict[teamA].losses+=1
        #update runs scored/surrendered
        tDict[teamA].GF+=AScore
        tDict[teamB].GF+=BScore
        tDict[teamA].GA+=BScore
        tDict[teamB].GA+=AScore
        
        tDict[teamA].awayGF+=AScore
        tDict[teamB].homeGF+=BScore
        tDict[teamA].awayGA+=BScore
        tDict[teamB].homeGA+=AScore
        
        
        #update function lets us consolidate the update of certain counting stats (eg. total games played, points scored)
        tDict[teamA].update(False)
        tDict[teamB].update(True)

def handleScheduleWithDate(games,tDict, unfinished, date):
    print(date.strftime('\nStandings estimations after %m/%d/%Y \n'))
    for i in range(0, len(games)):      #go through all games
        if games[i][2]!='@':           #to avoid double counting, we only look at away games ("@" is shorter than "Home")
            continue
        if games[i][6]==games[i][5] or games[i][0]>date:    #also check for games after specified date
            unfinished.append(games[i])
            continue

        #otherwise, we record the result of each game and the runs for each team
        teamA = games[i][-2]            #away
        teamB = games[i][3]             #home
        AScore = int(games[i][5])
        BScore = int(games[i][6])

        #we gotta check score directly instead of the "results" column, bc W/L symbols are weird and I don't want to clean it
        if AScore>BScore:
            tDict[teamA].wins+=1
            tDict[teamB].losses+=1
        elif AScore<BScore:
            tDict[teamB].wins+=1
            tDict[teamA].losses+=1
        #update runs scored/surrendered
        tDict[teamA].GF+=AScore
        tDict[teamB].GF+=BScore
        tDict[teamA].GA+=BScore
        tDict[teamB].GA+=AScore
        
        tDict[teamA].awayGF+=AScore
        tDict[teamB].homeGF+=BScore
        tDict[teamA].awayGA+=BScore
        tDict[teamB].homeGA+=AScore
        
        
        #update function lets us consolidate the update of certain counting stats (eg. total games played, points scored)
        tDict[teamA].update(False)
        tDict[teamB].update(True)   


#simulate one game
def oneGame(games, tDict, n, a, b, debug):
    handleSchedule(games,tDict, [])     #we don't need the unfinished games thing, so just leave it like this

    winLoss = [0,0]
    avgRuns = [0,0]
    allGames = [[],[]]

    #this section is largely the same as the runSim function, but we actually care about the runs scored by each side
    for i in range(0, n):
        nameA = a
        nameB = b
        teamA = tDict[nameA]
        teamB = tDict[nameB]
        while True:
            #result = predict.h2hRuns(teamA, teamB)
            result = predict.h2hHFA(teamA, teamB)
            if result[0]!=result[1]:
                break
        allGames[0].append(result[0])
        allGames[1].append(result[1])
        if result[0]>result[1]:
            winLoss[0]+=1
        else:
            winLoss[-1]+=1
        avgRuns[0]+=result[0]
        avgRuns[1]+=result[1]

    #average runs per game
    avgRuns[0] = avgRuns[0]/n
    avgRuns[1] = avgRuns[1]/n
    allGames[0].sort()
    allGames[1].sort()
    print(allGames[0][len(allGames[0])//2], allGames[1][len(allGames[1])//2])
    print(winLoss)
    print(avgRuns)
    
    if not debug:               #debug variable determines if we run verification or not
        return
    
    print("Verification")       #make sure the result makes sense by testing it against itself essentially
    
    res = [0,0]
    for i in range(0, n):
        nameA = a
        nameB = b
        teamA = tDict[nameA]
        teamB = tDict[nameB]
        while True:
            result = predict.h2hV2(teamA, teamB)
            if result==1:
                res[0]+=1
                break
            elif result==-1:
                res[1]+=1
                break
    print(res)
    return [avgRuns, winLoss]
    
#testing home field advantage
def checkHome(startYear, endYear):
    points = [0,0]
    wins = [0,0]
    counter = 0
    for i in range(startYear, endYear+1):
        #we need to check if the table for this season exists
        sql = "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'test') AND (TABLE_NAME = 'bb" + str(i) + "')"
        mycursor.execute(sql)
        for x in mycursor:
            print(x[0])
            if x[0]==0:
                print("Season has not been imported or cannot be found; terminating program")
                exit()
        mycursor.execute("SELECT * FROM bb" + str(i))
        games = mycursor.fetchall()
        for j in range(0, len(games)):
            if games[j][2]!='@':           #to avoid double counting, we only look at away games ("@" is shorter than "Home")
                continue
    
            #otherwise, we record the result of each game and the runs for each team
            teamA = games[j][-2]
            teamB = games[j][3]
            AScore = int(games[j][5])
            BScore = int(games[j][6])
            points[1] += BScore
            points[0] += AScore
            if AScore > BScore:
                wins[0]+=1
            else:
                wins[1]+=1
            counter+=1
    print(points)
    print(points[0]/counter, points[1]/counter)
    print(wins)
    print(wins[0]/counter, wins[1]/counter)

#returns games on a specific date
def getGamesOnDate(date):
    command = "SELECT * FROM bb" + str(YEAR) + " WHERE Date = '" + date + "'"
    mycursor.execute(command)
    return mycursor.fetchall()    

#we have a small penalty for teams playing b2b road games
def checkB2B(date, currTeam):
    check = date - datetime.timedelta(days = 1)
    command = "SELECT count(*) FROM bb" + str(YEAR) + " WHERE Date = '" + check.strftime("%Y-%m-%d") + "' and Team = '" + currTeam + "' and HA = '@'"
    mycursor.execute(command)
    for x in mycursor:
        if x[0]>0:
            command = "SELECT * FROM bb" + str(YEAR) + " WHERE Date = '" + check.strftime("%Y-%m-%d") + "' and Team = '" + currTeam + "' and HA = '@'"
            mycursor.execute(command)
            myresult = mycursor.fetchall()
            return myresult
        return False

#test accuracy of predictions using a given set of dates
def backtest(games, tDict, dates, n):
    avgSpread = 0
    avgRealSpread = 0
    totalGames = 0
    hitChance = 0
    for date in dates:
        toSim = getGamesOnDate(date.strftime("%Y-%m-%d"))
        handleScheduleWithDate(games, tDict, [], date)
        for curr in toSim:
            if curr[2] == "@":
                continue
            a = curr[-2]                        #home
            b = curr[3]                         #away
            winLoss = [0,0]
            avgRuns = [0,0]
            allGames = [[],[]]

            nameA = a
            nameB = b
            teamA = tDict[nameA]
            teamB = tDict[nameB]            

            isB2B = checkB2B(date, teamB.name)

            #this section is largely the same as the runSim function, but we actually care about the runs scored by each side
            for i in range(0, n):
                while True:
                    if isB2B==False:
                        result = predict.h2hHFA(teamB, teamA, False)
                    else:
                        result = predict.h2hHFA(teamB, teamA, True)                        
                    if result[0]!=result[1]:
                        break
                allGames[0].append(result[0])
                allGames[1].append(result[1])
                if result[0]>result[1]:
                    winLoss[0]+=1
                else:
                    winLoss[-1]+=1
                avgRuns[0]+=result[0]
                avgRuns[1]+=result[1]
        
            #average runs per game
            avgRuns[0] = avgRuns[0]/n
            avgRuns[1] = avgRuns[1]/n
            allGames[0].sort()
            allGames[1].sort()
            print(tDict[b].alias,"-", tDict[a].alias)
            print(allGames[0][len(allGames[0])//2], allGames[1][len(allGames[1])//2])
            print(winLoss)
            print(avgRuns)            
            
            totalGames+=1
            print("Real Result: ", curr[6], curr[5])
            avgSpread += allGames[0][len(allGames[0])//2] - allGames[1][len(allGames[1])//2]
            avgRealSpread += curr[6] - curr[5]
            if ((curr[6] - curr[5]) * (allGames[0][len(allGames[0])//2] - allGames[1][len(allGames[1])//2])) > 0:
                hitChance+=1
            print("")
    
    print("Average Spread: ", avgSpread/totalGames)
    print("Average Real Spread: ", avgRealSpread/totalGames)
    print("Success Rate: ", hitChance/totalGames)
    print("Games Played: ", totalGames)

#oneGame(importGames(), initializeTeams(), 500, "TOR", "NOP", False)
#debugging/test stuff, can safely ignore
dateArr = []
for i in range(1, 32):
    dateArr.append(datetime.datetime(YEAR-1, 12, i, 0, 0))
for i in range(1, 32):
    dateArr.append(datetime.datetime(YEAR, 1, i, 0, 0))
for i in range(1, 29):
    dateArr.append(datetime.datetime(YEAR, 1, i, 0, 0))
backtest(importGames(), initializeTeams(), dateArr, 300)
#end of debugging stuff
#checkHome(2022,2024)

#test effects of b2b road games
def b2b(games, tDict, dates):
    allGames = [0,0]
    totalGames = 0
    wins = 0
    
    nonB2B = [0,0]
    nWins = 0
    for date in dates:
        toSim = getGamesOnDate(date.strftime("%Y-%m-%d"))
        for i in range (0, len(toSim)):
            curr = toSim[i]
            if curr[2] != "@":
                continue
            previous = checkB2B(date, curr[-2])
            if previous!=False:
                allGames[0] += curr[6]
                allGames[1] += curr[5]
                totalGames += 1
                if curr[6] > curr[5]:
                    wins += 1
                nonB2B[0] += previous[0][6]
                nonB2B[1] += previous[0][5]
                if previous[0][6] > previous[0][5]:
                    nWins += 1
                print(previous[0][5], previous[0][6])
                print(curr[5], curr[6])
                print ("\n")
                
    print("Average Real Spread: ", (allGames[1]-allGames[0])/totalGames)
    print("Average Score: ", allGames[1]/totalGames, allGames[0]/totalGames)
    print("Home Win Rate: ", wins/totalGames)
    print("Average Previous Spread: ", (nonB2B[1]-nonB2B[0])/totalGames)
    print("Average Score: ", nonB2B[1]/totalGames, nonB2B[0]/totalGames)
    print("Previous Home Win Rate: ", nWins/totalGames)    
    
    
#b2b(importGames(), initializeTeams(), dateArr)