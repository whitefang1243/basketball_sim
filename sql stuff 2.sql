SELECT * FROM test.course;


select sname, cname, grade from student join course left join grades on grades.cid= course.cid and student.sid = grades.sid;


explain analyze select sname, cname,
(CASE
	when grade is not null then grade
    when grade is null then "n/a"
END) as pct
from (select sid, cid, sname, cname from student join course) t left join grades on grades.cid = t.cid and grades.sid = t.sid;

explain analyze select sname, average, courseList
from (select avg(grade) as average, sid, group_concat(cname separator ', ') as courseList 
	from course, grades where course.cid = grades.cid group by sid) t, student 
where student.sid = t.sid;

select sname,student.sid, avg(grade) as average, group_concat(cname separator ', ') as courseList, count(course.cid) as numCourse, max(grade), min(grade) 
from student,course,grades 
where student.sid=grades.sid and course.cid=grades.cid and not exists (select 1 from grades, course where grades.cid = course.cid and cname = "English" and grades.sid = student.sid)
group by student.sid 
order by average desc;

select (1*false);

with
    best as (select sid, max(grade) as b from grades group by sid)
select grades.sid, cname, concat(grade, if(grade=b, "*", "")) as marks
from grades 
	join best on grades.sid=best.sid
    join course on grades.cid = course.cid;

explain with
    best as (select cid, max(grade) as b from grades group by cid)
select sname, cname, concat(grade, if(grade=b, "*", "")) as marks
from grades 
	join best on grades.cid=best.cid
    join course on grades.cid = course.cid
    join student on student.sid = grades.sid;

select * from course where cid = 3 for share;
update course set cname = "Chem" where cid = 4;

SELECT `count` FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="lock_deadlocks";

show processlist;
          
	
