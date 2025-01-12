import basketball_test
import mysql.connector
import numpy as np

YEAR = 2025                 #year we are loading/updating
CURRENT = 2025              #current year

teams = ['ATL', 'BOS', 'CHO', 'CHI','CLE','DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP',
         'NYK', 'BRK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Aa531491",
  database = "test"
)

mycursor = mydb.cursor()

#we need to check if the table for this season exists already
sql = "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'test') AND (TABLE_NAME = 'bb" + str(YEAR) + "')"
mycursor.execute(sql)
for x in mycursor:
    print(x[0])
    if x[0]>0:
        if YEAR!=CURRENT:                                   #if a table for this season exists, and the season is not the active season, check if it is populated
            sql = "SELECT COUNT(*) FROM bb" + str(YEAR)      #jank, but idk how to fix this
            mycursor.execute(sql)
            count = mycursor.fetchone()[0]
            if count>0:                                     #if populated, kill the program 
                print("Season has already been loaded, terminating program")    #TODO:  add a way to override this whole check
                exit()
    else:                                                   #if table does not exist, create table based on bb2025 (current season)
        sql = "CREATE TABLE bb" + str(YEAR) + " LIKE bb2025"
        mycursor.execute(sql)
        mydb.commit()

#blank the table before loading new stuff
sql = "DROP TABLE IF EXISTS bb"+str(YEAR) + "_old"
mycursor.execute(sql)

sql = "CREATE TABLE bb" + str(YEAR) + "_old LIKE bb" + str(YEAR)
mycursor.execute(sql)

sql = "INSERT INTO bb" + str(YEAR) + "_old SELECT * FROM bb" + str(YEAR)
mycursor.execute(sql)
mydb.commit()


arr = basketball_test.main(YEAR, True)                   #we do the scrape before the delete just in case
sql = "DELETE FROM `bb" + str(YEAR) + "`"
mycursor.execute(sql)
mydb.commit()

for i in range(0, len(arr)):
    streak = 0                          #aka: how to quantify how terrible the white sox are
    for j in range(0, len(arr[i])):
        #print(arr[i][j])
        sql = "INSERT INTO `bb" + str(YEAR) + "` (Date, Time, HA, Opp, OT, Score, OppScore, Notes, gameNo, Team, Streak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if np.isnan(arr[i][j][7]):
            val = (arr[i][j][0], arr[i][j][1], arr[i][j][3], arr[i][j][4], arr[i][j][6], 0, 0, arr[i][j][14], j, arr[i][j][-1], 0)     
        else:
            if j==0:
                streak = 1 
            else:                               #streak is done by comparing current result to the previous one
                if arr[i][j][7]>arr[i][j][8]:   #once again, we need to check score manually bc results column is weird
                    if arr[i][j-1][7]>arr[i][j-1][8]:
                        streak += 1
                    else:
                        streak = 1
                if arr[i][j][7]<arr[i][j][8]:
                    if arr[i][j-1][7]<arr[i][j-1][8]:
                        streak += 1
                    else:
                        streak = 1
            val = (arr[i][j][0], arr[i][j][1], arr[i][j][3], arr[i][j][4], arr[i][j][6], int(arr[i][j][7]), int(arr[i][j][8]), arr[i][j][14], j, arr[i][j][-1], streak)
        mycursor.execute(sql, val)
        mydb.commit()

#this is just here to verify if everything is correct
for i in range(0, len(teams)):
    sql = "SELECT COUNT(*) FROM `bb" + str(YEAR) + "` WHERE (Team=%s or Opp=%s) and HA='@'"
    val = (teams[i], teams[i])
    mycursor.execute(sql, val)
    for x in mycursor:
        print(teams[i], x)