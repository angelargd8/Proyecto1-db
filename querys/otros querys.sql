-------------otros -----------------------------
---------------------- 8 ------------------------

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

---------------------- 9 ------------------------

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


---------------------- 10 ------------------------

--top 10 mas limpios 
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

--top 10 mas sucios 

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



-----------------------------------------------------------------------------------------
--Numero de faltas, tarjetas rojas, amarillas, goles esperados y goles del equipo con más faltas de cada temporada-----------------------------------------------
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

-----------------------------------------------------------------------------------------
---top 10 equipos con resultados de haber ganado más partidos----------------------------

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

-----------------------------------------------------------------------------------------
--equipos que más han participado en las temporadas------
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

-----------------------------------------------------------------------------------------
--Comparación de los primeros 10 los equipos en casa y fuera--------
SELECT teams.name, ts.teamID,
COUNT(CASE WHEN ts.location = 'h' and result = 'W' THEN 1 END) as casa_gana, 
COUNT(CASE WHEN ts.location = 'a' and result = 'W' THEN 1 END) as visita_gana
FROM teamstats ts
join teams on ts.teamID = teams.teamID
GROUP BY ts.teamID, teams.name
ORDER BY casa_gana desc, visita_gana desc LIMIT 10;





-----------------------------------------------------------------------------------------
-- Los equipos que más han ganado y empatado de todas las ligas y las season, sin importar la diferencia de goles 
select t.name, g. leagueID ,count(*) as num_wins_empates from public.games g
join public.teamstats ts on (g gameID = ts.gameID)
join public.teams t on (t.teamid = ts.teamid)
where ts.result = 'W' or ts.result = 'D'
group by t.name, g. leagueID order by num_wins_empates desc


-----------------------------------------------------------------------------------------
-- De los equipos que mas goles tienen y cuantos partidos tienen ganado (se compara con el resultado anterior)

select t.name, count(*) as total_ganados, sum(ts.goals) as goles from public. teamstats ts
join public.teams t on (t. teamid = ts. teamid)
where ts.result = 'W'
group by t. name order by goles desc

-----------------------------------------------------------------------------------------
-- Los equipos que más partidos ganados tiene y cuantos goles
select t.name, count(*) as total_ganados, sum(ts goals) as goles from public.teamstats ts
join public.teams t on (t.teamid = ts.teamid)
where ts.result = 'W'
group by t. name order by total_ganados desc



-----------------------------------------------------------------------------------------
--  De los equipos que mas han ganado, sacar cuantos goles tienen en partidos empatados 


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
order by sum_goals desc


-- -----------------------------------------------------------------------------------------
-- La cuota mínima que la casa B365 da por ganar (mientras más baja, más probabilidades hay de ganar pero se gana menos dinero si se apuesta por ella y se acierta)


select t.name,
    MIN(CASE
            WHEN g.hometeamid = t.teamid THEN g.B365H
            WHEN g.awayteamid = t.teamid THEN g.B365A
            ELSE NULL
        END
    ) AS min_odds
from  public.teams t
join
    public.games g ON 
    (t.teamid = g.hometeamid OR t.teamid = g.awayteamid)
GROUP BY
    t.name
HAVING
    MIN(CASE
            WHEN g.hometeamid = t.teamid THEN g.B365H
            WHEN g.awayteamid = t.teamid THEN g.B365A
            ELSE NULL
        END
    ) != 0 
ORDER BY
    min_odds ASC;

-- -----------------------------------------------------------------------------------------
-- El promedio de goles según estén de home o away


SELECT
    t.name AS team_name,
    AVG(CASE WHEN g.hometeamid = t.teamid THEN g.homegoals ELSE null END) AS avg_goals_home,
    AVG(CASE WHEN g.awayteamid = t.teamid THEN g.awaygoals ELSE null END) AS avg_goals_away
FROM
    public.games g
JOIN
    public.teams t ON g.hometeamid = t.teamid OR g.awayteamid = t.teamid
GROUP BY
    t.name
order by avg_goals_home desc
