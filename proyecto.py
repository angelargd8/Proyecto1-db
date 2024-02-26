from conexion import conexiones
import psycopg2

conexion= conexiones()
#uso de cursor
cursor= conexion.cursor()

#queries sql
#sql='SELECT shooterid FROM shots'
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

#con lo que se ejecutan las consultas
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
#mostrar el resultado

#cerrando la conexión a la base de datos
cursor.close()
conexion.close()
