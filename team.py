class Team:
    def __init__(self, name, wins, ties, losses, GF, GA):
        self.name = name
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.GA = GA
        self.GF = GF
        self.games = wins + losses + ties
        self.points = wins*3 + ties
        self.position = 0
        self.UCL = 0
        self.rel = 0
        self.best = 31
        self.worst = 0
        self.tWins = 0
        self.tLoss = 0
        
    def __init__(self, name, wins, ties, losses, GF, GA, league, division, alias):
        self.name = name
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.GA = GA
        self.GF = GF
        self.games = wins + losses + ties
        self.points = wins*3 + ties
        self.position = 0
        self.best = 31
        self.worst = 0
        self.tWins = 0
        self.tLoss = 0  
        self.league = league
        self.division = division
        self.winDiv = 0
        self.WC = 0
        self.alias = alias
        self.homeGF = 0
        self.awayGF = 0
        self.homeGA = 0
        self.awayGA = 0
        self.homeGames = 0
        
    def __str__(self):
        return self.name + " " + str(self.points)
    
    def update(self, isHome):
        self.games = self.wins + self.losses + self.ties
        if isHome:
            self.homeGames+=1
        self.points = self.wins*3 + self.ties        
    
    
    
    