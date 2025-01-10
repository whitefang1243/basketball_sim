import basketball_scraper
import numpy as np
import time

DELAY = 10

teams = ['ATL', 'BOS', 'CHO', 'CHI','CLE','DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP',
         'NYK', 'BRK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

s = basketball_scraper.TeamScraper()
s.set_season(2025)
data = s.scrape('LAC')
print(data)


def main(year, flag):
    
    s = basketball_scraper.TeamScraper()
    s.set_season(year)
    data = s.scrape('ATL')
    data = data.assign(Team = ['ATL' for x in range(data.shape[0])])
    print(data.head())
    arr = data.to_numpy()
    #arr=np.delete(arr, -1, axis = 1)
    arr = [arr.tolist()]
    print(arr)
    for i in range(1, len(teams)):
        time.sleep(DELAY)
        data = s.scrape(teams[i])
        data = data.assign(Team = [teams[i] for x in range(data.shape[0])])        
        print(data.head())
        arr2 = data.to_numpy()
        #arr2=np.delete(arr2, -1, axis = 1)
        arr2 = arr2.tolist()
        arr.append(arr2)
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            #arr[i][j][0] = arr[i][j][0].strftime('%Y-%m-%d')
            if arr[i][j][0] is None :
                print(i)
    #ret_arr and any related code is for debugging purposes; will be removed in the future
    ret_arr = []
    for i in range(0, len(arr)):
        ret_arr.append([])
        for j in range(0, len(arr[i])):
            if arr[i][j][3]=='@':
                ret_arr[-1].append(arr[i][j])
    print(len(arr[1]))
    print(len(ret_arr[1]))
    if flag:                #debug purposes
        return arr
    return ret_arr
#main(2025, True)