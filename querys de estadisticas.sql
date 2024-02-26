
-- 1. La cantidad de juegos jugados en cada temporada por cada equipo, de cada liga (tome
-- en cuenta que cada equipo puede jugar como visitante o como anfitrión.)


select count(*), ts.season, t.name as teamName, l.name as leagueName from public.teams t
join public.teamstats ts on (t.teamid = ts.teamid )
join public.games g on (ts.gameID = g.gameID)
join public.leagues l on (g.leagueid = l.leagueid)
group by ts.season, t.name, l.name



-- 2.  ¿Quién es el mejor equipo de todas las ligas y de todas las temporadas según las
-- estadísticas de diferencia de goles?
-- Hint: Obtenga la cantidad de goles a favor, goles en contra y la diferencia entre las dos
-- anteriores, esto por cada temporada y por cada equipo de cada liga.
-- Utilizando este mismo query, obtenga el ranking de los equipos por temporada y por
-- liga, ordenados por ese ranking de manera descendente por diferencia (utilice la función
-- Rank () over patition), para obtener el equipo ganador.


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
    ranking;
	
-- El mejor equipo de todas las temporadas y todas las ligas es Barcelona con 89 goles de diferencia a su favor 

-- 3. ¿Quiénes son los jugadores que han realizado mayor cantidad de goles a través de todas
-- las temporadas? ¿Cuáles son los jugadores con mayor cantidad de pases izquierdos y
-- pases derechos que han hecho goles? (Compare contra los resultados del inciso 2 y
-- determine de manera textual si dichos jugadores pertenecen a los equipos del inciso
-- anterior).


select Goals.player_name, Goals.total_goals, shoots.left_foot_goals, shoots.right_foot_goals
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
on (Goals.playerID= shoots.shooterID)






	


