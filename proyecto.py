from conexion import conexiones
import psycopg2

conexion= conexiones()
#uso de cursor
cursor= conexion.cursor()

#queries sql
#sql='SELECT shooterid FROM shots'
sql1 = '''select count(*), ts.season, t.name as teamName, l.name as leagueName from public.teams t
join public.teamstats ts on (t.teamid = ts.teamid )
join public.games g on (ts.gameID = g.gameID)
join public.leagues l on (g.leagueid = l.leagueid)
group by ts.season, t.name, l.name
'''

sql2 = '''

WITH TeamGoals AS (
select
    home.homeTeamID as team_id,
    home.name AS team_name,
	home.season,
	home.leagueID,
    
    home.goals_difference + away.goals_difference AS total_goals_difference
FROM(
select g.homeTeamID, t.name,g.season,  g.leagueID,SUM(g.homegoals-g.awaygoals) as goals_difference
from public.teams t
join public.games g on ( g.homeTeamID = t.teamid)
group by  g.homeTeamID, t.name, g.season,g.leagueID
order by goals_difference desc) as home
join (
select g.awayTeamID, t.name, g.season, g.leagueID,sum(g.awaygoals-g.homegoals) as goals_difference from  public.teams t
join public.games g on ( g.awayTeamID = t.teamid)
group by  g.awayTeamID, t.name, g.season,g.leagueID
order by goals_difference desc) as away 
on(home.homeTeamID = away.awayTeamID
    AND home.season = away.season)
ORDER BY
    total_goals_difference desc)
select 
    team_id,
    team_name,
    season,leagueID,
    total_goals_difference,
    RANK() OVER (PARTITION BY season, leagueID ORDER BY total_goals_difference DESC) AS ranking
FROM
    TeamGoals
ORDER BY
    total_goals_difference desc,
    ranking;'''


sql3 = '''select Goals.player_name, Goals.total_goals, shoots.left_foot_goals, shoots.right_foot_goals
, shoots.total_passes
from
(select a.playerID, p.name as player_name, count(*) AS total_goals
from Public."appearances" a
join public.players p on (a.playerid = p.playerid)
where  goals > 0
group by a.playerID, p.name
order by total_goals DESC ) as Goals
join
(
select shooterID, 
    SUM(CASE WHEN shotType = 'LeftFoot' THEN 1 ELSE 0 END) AS left_foot_goals,
    SUM(CASE WHEN shotType = 'RightFoot' THEN 1 ELSE 0 END) AS right_foot_goals, COUNT(*) AS total_passes
from Public."shots"
where  shotResult = 'Goal'
group by  shooterID) as shoots
on (Goals.playerID= shoots.shooterID)'''


sql4='''SELECT season, leagueID, homeTeamID, 
GREATEST(
    AVG(CASE WHEN B365D = 0 THEN 0 ELSE 1/B365D END), 
    AVG(CASE WHEN B365H = 0 THEN 0 ELSE 1/B365H END),
    AVG(CASE WHEN B365A = 0 THEN 0 ELSE 1/B365A END),

    AVG(CASE WHEN BWH = 0 THEN 0 ELSE 1/BWH END), 
    AVG(CASE WHEN BWD = 0 THEN 0 ELSE 1/BWD END),
    AVG(CASE WHEN BWA = 0 THEN 0 ELSE 1/BWA END),

    AVG(CASE WHEN IWH = 0 THEN 0 ELSE 1/IWH END), 
    AVG(CASE WHEN IWD = 0 THEN 0 ELSE 1/IWD END),
    AVG(CASE WHEN IWA = 0 THEN 0 ELSE 1/IWA END),

    AVG(CASE WHEN PSH = 0 THEN 0 ELSE 1/PSH END), 
    AVG(CASE WHEN PSD = 0 THEN  0 ELSE 1/PSD END),
    AVG(CASE WHEN PSA = 0 THEN 0 ELSE 1/PSA END),

    AVG(CASE WHEN WHH = 0 THEN 0 ELSE 1/WHH END), 
    AVG(CASE WHEN WHD = 0 THEN 0  ELSE 1/WHD END),
    AVG(CASE WHEN WHA = 0 THEN 0 ELSE 1/WHA END),

    AVG(CASE WHEN VCH = 0 THEN 0 ELSE 1/VCH END), 
    AVG(CASE WHEN VCD = 0 THEN 0 ELSE 1/VCD END),
    AVG(CASE WHEN VCA = 0 THEN 0 ELSE 1/VCA END),

    AVG(CASE WHEN PSCH = 0 THEN 0 ELSE 1/PSCH END), 
    AVG(CASE WHEN PSCD = 0 THEN 0 ELSE 1/PSCD END),
    AVG(CASE WHEN PSCA = 0 THEN 0 ELSE 1/PSCA END)
    )
    AS max_probabilidad 

FROM games

WHERE homeTeamID is not null and leagueID is not null and season is not null
and B365D is not null 
and B365H is not null 
and B365A is not null

and BWH is not null 
and BWD is not null 
and BWA is not null

and IWH is not null 
and IWD is not null 
and IWA is not null

and PSH is not null 
and PSD is not null 
and PSA is not null

and WHH is not null 
and WHD is not null 
and WHA is not null
      
and VCH is not null 
and VCD is not null 
and VCA is not null

and PSCH is not null 
and PSCD is not null 
and PSCA is not null

GROUP BY season,leagueID,homeTeamID
--ORDER BY max_probabilidad DESC;

UNION ALL 


SELECT season, leagueID, awayTeamID,  
GREATEST(
    AVG(CASE WHEN B365D = 0 THEN 0 ELSE 1/B365D END), 
    AVG(CASE WHEN B365H = 0 THEN 0 ELSE 1/B365H END),
    AVG(CASE WHEN B365A = 0 THEN 0 ELSE 1/B365A END),

    AVG(CASE WHEN BWH = 0 THEN 0 ELSE 1/BWH END), 
    AVG(CASE WHEN BWD = 0 THEN 0 ELSE 1/BWD END),
    AVG(CASE WHEN BWA = 0 THEN 0 ELSE 1/BWA END),

    AVG(CASE WHEN IWH = 0 THEN 0 ELSE 1/IWH END), 
    AVG(CASE WHEN IWD = 0 THEN 0 ELSE 1/IWD END),
    AVG(CASE WHEN IWA = 0 THEN 0 ELSE 1/IWA END),

    AVG(CASE WHEN PSH = 0 THEN 0 ELSE 1/PSH END), 
    AVG(CASE WHEN PSD = 0 THEN  0 ELSE 1/PSD END),
    AVG(CASE WHEN PSA = 0 THEN 0 ELSE 1/PSA END),

    AVG(CASE WHEN WHH = 0 THEN 0 ELSE 1/WHH END), 
    AVG(CASE WHEN WHD = 0 THEN 0  ELSE 1/WHD END),
    AVG(CASE WHEN WHA = 0 THEN 0 ELSE 1/WHA END),

    AVG(CASE WHEN VCH = 0 THEN 0 ELSE 1/VCH END), 
    AVG(CASE WHEN VCD = 0 THEN 0 ELSE 1/VCD END),
    AVG(CASE WHEN VCA = 0 THEN 0 ELSE 1/VCA END),

    AVG(CASE WHEN PSCH = 0 THEN 0 ELSE 1/PSCH END), 
    AVG(CASE WHEN PSCD = 0 THEN 0 ELSE 1/PSCD END),
    AVG(CASE WHEN PSCA = 0 THEN 0 ELSE 1/PSCA END)
    )
    AS max_probabilidad 

FROM games

WHERE awayTeamID is not null and leagueID is not null and season is not null
and B365D is not null 
and B365H is not null 
and B365A is not null

and BWH is not null 
and BWD is not null 
and BWA is not null

and IWH is not null 
and IWD is not null 
and IWA is not null

and PSH is not null 
and PSD is not null 
and PSA is not null

and WHH is not null 
and WHD is not null 
and WHA is not null
      
and VCH is not null 
and VCD is not null 
and VCA is not null

and PSCH is not null 
and PSCD is not null 
and PSCA is not null

GROUP BY season,leagueID,awayTeamID
ORDER BY max_probabilidad DESC LIMIT 1'''

sql5='''
SELECT teamid, name FROM public.teams WHERE teamid='161'
'''

sql8='''
WITH max_goals_por_season AS (
    SELECT season, MAX(goals) as max_goals
    FROM teamstats
    WHERE teamID is not null and season is not null and goals is not null
    GROUP BY season
)
SELECT ts.season, ts.teamID, ts.goals,  teams.name, ts.location, ts.yellowCards, ts.redCards, ts.result
from teamstats ts
join max_goals_por_season mgps on ts.season = mgps.season and ts.goals = mgps.max_goals
join teams on ts.teamID = teams.teamID
where ts.teamID is not null and ts.season is not null and ts.goals is not null;
'''

sql9='''
WITH max_probabilidad_por_season_home AS (
    SELECT season, MAX(homeProbability) as max_prob_home
    FROM games
    WHERE  season is not null and homeProbability is not null
    GROUP BY season
),
max_probabilidad_por_season_AWAY AS (
    SELECT season, MAX(awayProbability) as max_prob_AWAY
    FROM games
    WHERE  season is not null and awayProbability is not null
    GROUP BY season
)


SELECT g.season, g.leagueID,leagues.name, g.homeTeamID,
GREATEST(
    AVG(CASE WHEN B365D = 0 THEN 0 ELSE 1/B365D END), 
    AVG(CASE WHEN B365H = 0 THEN 0 ELSE 1/B365H END),
    AVG(CASE WHEN B365A = 0 THEN 0 ELSE 1/B365A END)
)
AS mayor_probabilidad

FROM games g

join leagues on g.leagueID = leagues.leagueID
join max_probabilidad_por_season_home mph on g.season = mph.season

WHERE g.leagueID is not null and g.season is not null
and g.B365D is not null 
and g.B365H is not null 
and g.B365A is not null

GROUP BY g.season, g.leagueID, leagues.name, g.homeTeamID

UNION ALL 


SELECT g.season, g.leagueID,leagues.name, g.awayTeamID,
GREATEST(
    AVG(CASE WHEN B365D = 0 THEN 0 ELSE 1/B365D END), 
    AVG(CASE WHEN B365H = 0 THEN 0 ELSE 1/B365H END),
    AVG(CASE WHEN B365A = 0 THEN 0 ELSE 1/B365A END)
)
AS mayor_probabilidad

FROM games g

join leagues on g.leagueID = leagues.leagueID
join max_probabilidad_por_season_AWAY mpA on g.season = mpA.season

WHERE g.leagueID is not null and g.season is not null
and g.B365D is not null 
and g.B365H is not null 
and g.B365A is not null

GROUP BY g.season, g.leagueID, leagues.name, g.awayTeamID

ORDER BY mayor_probabilidad DESC LIMIT 3;

'''

sql10_limpio='''
WITH mas_limpios as(
	SELECT teamID, MIN(fouls) as min_faltas, MIN(yellowCards) as min_amarillas, MIN(redCards)  as min_rojas
	from teamstats
	WHERE teamID is not null and fouls is not null and yellowCards is not null and redCards is not null
	GROUP BY teamID
)

SELECT ts.teamID, teams.name, ts.fouls, ts.yellowCards, ts.redCards
from teamstats ts
join teams on ts.teamID = teams.teamID
JOIN mas_limpios on ts.teamID = mas_limpios.teamID 
				and ts.fouls = mas_limpios.min_faltas 
				and ts.yellowCards = mas_limpios.min_amarillas
				and ts.redCards = mas_limpios.min_rojas
where ts.teamID is not null and ts.fouls is not null and ts.yellowCards is not null and ts.redCards is not null
ORDER BY  ts.fouls, ts.yellowCards, ts.redCards DESC LIMIT 10;

'''

sql10_sucios='''
WITH mas_sucios as(
	SELECT teamID, MAX(fouls) as max_faltas, MAX(yellowCards) as max_amarillas, MAX(redCards) as max_rojas
	from teamstats
	WHERE teamID is not null and fouls is not null and yellowCards is not null and redCards is not null
	GROUP BY teamID
)

SELECT ms.teamID, teams.name, ms.max_faltas, ms.max_amarillas, ms.max_rojas
from mas_sucios ms
join teams on ms.teamID = teams.teamID
ORDER BY   ms.max_rojas DESC , ms.max_amarillas DESC, ms.max_faltas DESC LIMIT 10;
'''

sql11='''
WITH min_goals_por_season AS (
    SELECT season, MIN(goals) as min_goals
    FROM teamstats
    WHERE teamID is not null and season is not null and goals is not null
    GROUP BY season
)
SELECT ts.season, ts.teamID, teams.name, ts.fouls, ts.yellowCards, ts.redCards, ts.xGoals, ts.goals, ts.result
from teamstats ts
join min_goals_por_season mgps on ts.season = mgps.season and ts.goals = mgps.min_goals
join teams on ts.teamID = teams.teamID
where ts.teamID is not null and ts.season is not null and ts.goals is not null LIMIT 10;
'''

sql12='''
WITH ganadores as(
    SELECT teamID, COUNT(result) as ganados
    from teamstats
    WHERE teamID is not null and result = 'W'
    GROUP BY teamID
)

SELECT teams.name, g.ganados
from ganadores g
join teams on g.teamID = teams.teamID
order by ganados desc LIMIT 10;
'''

sql13='''
WITH cant_temporadas as(
    SELECT teamID, 
	COUNT(season) as temporadas 
	from teamstats
    WHERE teamID is not null 
    GROUP BY teamID
)

SELECT g.teamID,teams.name, g.temporadas
from cant_temporadas g
join teams on g.teamID = teams.teamID
order by g.temporadas desc LIMIT 10;
'''

sql14='''
SELECT teams.name, ts.teamID,
COUNT(CASE WHEN ts.location = 'h' and result = 'W' THEN 1 END) as casa_gana, 
COUNT(CASE WHEN ts.location = 'a' and result = 'W' THEN 1 END) as visita_gana
FROM teamstats ts
join teams on ts.teamID = teams.teamID
GROUP BY ts.teamID, teams.name
ORDER BY casa_gana desc, visita_gana desc LIMIT 10;
'''

sql15 = '''select t.name, g. leagueID ,count(*) as num_wins_empates from public.games g
join public.teamstats ts on (g gameID = ts.gameID)
join public.teams t on (t.teamid = ts.teamid)
where ts.result = 'W' or ts.result = 'D'
group by t.name, g. leagueID order by num_wins_empates desc'''

sql16 = '''select t.name, count(*) as total_ganados, sum(ts.goals) as goles from public. teamstats ts
join public.teams t on (t. teamid = ts. teamid)
where ts.result = 'W'
group by t. name order by goles desc'''

sql17 = '''select t.name, count(*) as total_ganados, sum(ts goals) as goles from public.teamstats ts
join public.teams t on (t.teamid = ts.teamid)
where ts.result = 'W'
group by t. name order by total_ganados desc
'''

sql8 = '''
select empates.sum_goals, ganadores.name from 

(select  ts.teamID, t.name,
    sum(ts.goals) AS sum_goals,
    sum(ts.shots) AS sum_shots   
from Public."teamstats" ts
join public.teams t on (t.teamid = ts.teamid)
where result = 'D' 
group by ts.teamID, t.name
order by sum_goals desc) as empates

join 

(select ts.teamid, t.name,  sum(ts.goals) as goles, count(*) as total_ganados from
public.teamstats ts 
join public.teams t on (t.teamid = ts.teamid)
where ts.result = 'W'
group by t.name, ts.teamid
order by total_ganados desc) as ganadores

on (empates.teamID = ganadores.teamid)
group by ganadores.name, empates.sum_goals
order by sum_goals desc'''

#con lo que se ejecutan las consultas
print("\nejercicio 1")
cursor.execute(sql1)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 2")
cursor.execute(sql2)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 3")
cursor.execute(sql3)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 4")
cursor.execute(sql4)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 5")
cursor.execute(sql5)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 8")
cursor.execute(sql8)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 9")
cursor.execute(sql9)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 10 - mas limpios ")
cursor.execute(sql10_limpio)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 10 - mas sucios ")
cursor.execute(sql10_sucios)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 11: Numero de faltas, tarjetas rojas, amarillas, goles esperados y goles del equipo con más faltas de cada temporada")
cursor.execute(sql11)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 12: top 10 equipos con resultados de haber ganado más partidos")
cursor.execute(sql12)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 13: equipos que más han participado en las temporadas")
cursor.execute(sql13)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 14: Comparación de los primeros 10 los equipos en casa y fuera")
cursor.execute(sql14)
registro= cursor.fetchall() 
print(registro)
print("\nejercicio 15: equipos con más victorias y empates")
cursor.execute(sql15)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 16: equipos con más goles")
cursor.execute(sql16)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 17: Los equipos que más partidos ganados tiene y cuantos goles")
cursor.execute(sql17)
registro= cursor.fetchall()
print(registro)
print("\nejercicio 8")
cursor.execute(sql8)
registro= cursor.fetchall()
print(registro)

#mostrar el resultado

#cerrando la conexión a la base de datos
cursor.close()
conexion.close()
