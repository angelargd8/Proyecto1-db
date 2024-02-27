from conexion import conexiones
import psycopg2
import io

conexion= conexiones()
#uso de cursor
cursor= conexion.cursor()

def creacion_tablas():
    sql='''
    CREATE TABLE Public."appearances"(
	gameID int,
	playerID varchar(10),
	goals int,
	ownGoals int,
	shots int,
	xGoals float,
	xGoalsChain float,
	xGoalsBuildup float,
	assists int,
	keyPasses int,
	xAssists float,
	position varchar(20),
	positionOrder int,
	yellowCard int,
	redCard int,
	time int,
	substituteIn varchar(10),
	substituteOut varchar(10),
	leagueID int
    );

    CREATE TABLE Public."games"(
    gameID int,
    leagueID int,
    season int,
    date varchar(20),
    homeTeamID int,
    awayTeamID int,
    homeGoals int,
    awayGoals int,
    homeProbability float,
    drawProbability float,
    awayProbability float,
    homeGoalsHalfTime int,
    awayGoalsHalfTime int,
    B365H float,
    B365D float,
    B365A float,
    BWH float,
    BWD float,
    BWA float,
    IWH float,
    IWD float,
    IWA float,
    PSH float,
    PSD float,
    PSA float,
    WHH float,
    WHD float,
    WHA float,
    VCH float,
    VCD float,
    VCA float,
    PSCH float,
    PSCD float,
    PSCA float
    );

    CREATE TABLE Public."leagues"(
    leagueID int,
    name varchar(20),
    understatNotation varchar(20)
    );

    CREATE TABLE Public."players"(
    playerID varchar(10),
    name varchar(50)
    );

    CREATE TABLE Public."shots" (
    gameID int,
    shooterID varchar(10),
    assisterID varchar(10),
    minute int,
    situation varchar(20),
    lastAction varchar(20),
    shotType varchar(20),
    shotResult varchar(20),
    xGoal float,
    positionX float,
    positionY float
    );

    CREATE TABLE Public."teams"(
    teamID int,
    name varchar(50)
    );

    CREATE TABLE Public."teamstats" (
    gameID int,
    teamID int,
    season int,
    date varchar(20),
    location varchar(10),
    goals int,
    xGoals float,
    shots int,
    shotsOnTarget int,
    deep int,
    ppda float,
    fouls int,
    corners int,
    yellowCards int,
    redCards int,
    result varchar(10)
    );

    '''
    
    cursor.execute(sql)
    print("\n tablas creadas")

def relaciones():
    sql2='''

    ALTER TABLE leagues ADD PRIMARY KEY (leagueID);
    ALTER TABLE players ADD PRIMARY KEY (playerID);
    ALTER TABLE teams ADD PRIMARY KEY (teamID);
    ALTER TABLE games ADD PRIMARY KEY (gameID);



    ALTER TABLE teamstats ADD FOREIGN KEY (gameID) REFERENCES games(gameID); 
    ALTER TABLE teamstats ADD FOREIGN KEY (teamID) REFERENCES teams(teamID);

    ALTER TABLE shots ADD FOREIGN KEY (gameID) REFERENCES games(gameID); 
    ALTER TABLE shots ADD FOREIGN KEY (shooterID) REFERENCES players(playerID); 
   
    ALTER TABLE games ADD FOREIGN KEY (leagueID) REFERENCES leagues(leagueID); 

    ALTER TABLE appearances ADD FOREIGN KEY (gameID) REFERENCES games(gameID); 
    ALTER TABLE appearances ADD FOREIGN KEY (playerID) REFERENCES players(playerID); 
    ALTER TABLE appearances ADD FOREIGN KEY (leagueID) REFERENCES leagues(leagueID); 
    '''
    cursor.execute(sql2)
    print("\n relaciones creadas")


#persistencia de archivos
def appearances():
    with open('.\\archivos\\appearances.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'appearances', sep=',')

def games():
    with open('.\\archivos\\games.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'games', sep=',')


def leagues():
    with open('.\\archivos\\leagues.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'leagues', sep=',')


def players():
    with open('.\\archivos\\players.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'players', sep=',')

def shots():
    with open('.\\archivos\\shots.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'shots', sep=',')


def teams():
    with open('.\\archivos\\teams.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'teams', sep=',')


def teamstats():
    with open('.\\archivos\\teamstats.csv','r') as f:
        next(f)
        data = f.read().replace('"', '')  #Eliminar las comillas
        data_io = io.StringIO(data)  #Crea un objeto StringIO
        cursor.copy_from(data_io, 'teamstats', sep=',')



creacion_tablas()
teams()
players()
leagues()
appearances()
games()
shots()
teamstats()

relaciones()


conexion.commit()
cursor.close()
conexion.close()