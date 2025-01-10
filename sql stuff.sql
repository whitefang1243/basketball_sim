SELECT * FROM test.bb2024;

select Team,  
SUM(CASE
    WHEN Score > OppScore THEN 1
    ELSE 0
END) W,
SUM(CASE
    WHEN Score < OppScore THEN 1
    ELSE 0
END) L
from bb2024 group by Team order by W desc, L asc;

select Team, W, L, ROUND(W/(W+L), 3) as 'pct', rank() over (order by W/(W+L) desc, W desc) as 'rank'
from (select Team,  
SUM(CASE
    WHEN Score > OppScore THEN 1
    ELSE 0
END) W,
SUM(CASE
    WHEN Score < OppScore THEN 1
    ELSE 0
END) L
from bb2024 group by Team) temp;


select Team, W, L, HW, HL, AW, AL, ROUND(W/(W+L), 3) as 'pct', ROUND(HW/(HW+HL), 3) as 'Hpct', ROUND(AW/(AW+AL), 3) as 'Apct', rank() over (order by W/(W+L) desc, W desc) as 'rank'
from (select Team,  
SUM(CASE
    WHEN Score > OppScore THEN 1
    ELSE 0
END) W,
SUM(CASE
    WHEN Score < OppScore THEN 1
    ELSE 0
END) L,
SUM(CASE
    WHEN Score > OppScore and HA = "Home" THEN 1
    WHEN Score < OppScore and HA = "Home" THEN 0
END) HW,
SUM(CASE
    WHEN Score > OppScore and HA = "Home" THEN 0
    WHEN Score < OppScore and HA = "Home" THEN 1
    ELSE 0
END) HL,
SUM(CASE
    WHEN Score > OppScore and HA = "@" THEN 1
    WHEN Score < OppScore and HA = "@" THEN 0
    ELSE 0
END) AW,
SUM(CASE
    WHEN Score > OppScore and HA = "@" THEN 0
    WHEN Score < OppScore and HA = "@" THEN 1
    ELSE 0
END) AL
from bb2024 group by Team) temp;

drop function if exists gameB;
DELIMITER $$
create function gameB (T varchar(10)) returns int DETERMINISTIC 
begin
    declare c int;
    declare leader varchar (10);
    declare retw int;
    declare retl int;
    declare lw int;
    declare ll int;
    drop temporary table if exists tt;
    create temporary table tt (select bbconf.Team, conf,  
SUM(CASE
    WHEN Score > OppScore THEN 1
    ELSE 0
END) W,
SUM(CASE
    WHEN Score < OppScore THEN 1
    ELSE 0
END) L
from bb2024 join bbconf on bbconf.Team=bb2024.Team group by Team);
    set c = (select conf from tt where Team = T limit 1);
    set lw = (select max(W) from tt where conf = c limit 1);
    set leader = (select Team from tt where W = lw limit 1);
    set lw = (select W from tt where Team = leader limit 1);
    set ll = (select L from tt where Team = leader limit 1);
    set retw = (select W from tt where Team = T limit 1);
    set retl = (select L from tt where Team = T limit 1);
    return ((retw-retl)-(lw-ll))/2;
end$$
DELIMITER ;

select Team, conf, W, L, ROUND(W/(W+L), 3) as 'pct', gameB(Team), rank() over (partition by conf order by W/(W+L) desc, W desc) as rk 
from (select bbconf.Team, conf,  
SUM(CASE
    WHEN Score > OppScore THEN 1
    ELSE 0
END) W,
SUM(CASE
    WHEN Score < OppScore THEN 1
    ELSE 0
END) L
from bb2024 join bbconf on bbconf.Team=bb2024.Team group by bbconf.Team) temp order by conf;