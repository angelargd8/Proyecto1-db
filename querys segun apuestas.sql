-------------querys segun apuestas---------------
---------------------- 4 ------------------------
SELECT season, leagueID, homeTeamID,  
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
ORDER BY max_probabilidad DESC LIMIT 1;


---------------------- 5 ------------------------
SELECT teamid, name
FROM public.teams WHERE teamid='161';
