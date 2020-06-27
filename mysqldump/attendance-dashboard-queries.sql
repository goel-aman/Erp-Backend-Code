create table present_table_final as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as present_days from student_attendance_map where status='P' group by 1,2 order by 1,2);

create table working_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as working_days from student_attendance_map group by 1,2 order by 1,2);

create table temp as (select student_class_map_id, month_name from working_table)

create table absent_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as absent_days from student_attendance_map where status='A' group by 1,2 order by 1,2)

create table absent_table_final as (select t.student_class_map_id, t.month_name, att.absent_days from temp t left OUTER join absent_table att on t.student_class_map_id=att.student_class_map_id and t.month_name=att.month_name order by 1,2)

update absent_table_final set absent_days=0 where absent_days is null

create table late_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as late_days from student_attendance_map where status='L' group by 1,2 order by 1,2)

create table late_table_final as (select t.student_class_map_id, t.month_name, att.late_days from temp t left OUTER join late_table att on t.student_class_map_id=att.student_class_map_id and t.month_name=att.month_name order by 1,2)

update late_table_final set absent_days=0 where late_days is null

create table attendance_records_final select wt.student_class_map_id,wt.month_name,pt.present_days,at.absent_days,lt.late_days,wt.working_days from present_table_final pt join working_table wt on pt.student_class_map_id=wt.student_class_map_id and wt.month_name=pt.month_name join absent_table_final at on pt.student_class_map_id=at.student_class_map_id and at.month_name=pt.month_name join late_table_final lt on pt.student_class_map_id=lt.student_class_map_id and lt.month_name=pt.month_name

create table cumulative_attendance_records_final select ar.student_class_map_id,ar.month_name,sum(at.present_days) as cumulative_present,sum(at.absent_days) as cumulative_absent,sum(at.late_days) as cumulative_late,sum(at.working_days) as cumulative_working from attendance_records_final ar join attendance_records_final at on ar.student_class_map_id=at.student_class_map_id and ar.month_name>=at.month_name group by 1,2;

drop table temp

drop table absent_table

drop table late_table

update absent_table_final set absent_days=0 where absent_days is null

create table late_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as late_days from student_attendance_map where status='L' group by 1,2 order by 1,2)

create table late_table_final as (select t.student_class_map_id, t.month_name, att.late_days from temp t left OUTER join late_table att on t.student_class_map_id=att.student_class_map_id and t.month_name=att.month_name order by 1,2)

update late_table_final set absent_days=0 where late_days is null

create table attendance_records_final select wt.student_class_map_id,wt.month_name,pt.present_days,at.absent_days,lt.late_days,wt.working_days from present_table_final pt join working_table wt on pt.student_class_map_id=wt.student_class_map_id and wt.month_name=pt.month_name join absent_table_final at on pt.student_class_map_id=at.student_class_map_id and at.month_name=pt.month_name join late_table_final lt on pt.student_class_map_id=lt.student_class_map_id and lt.month_name=pt.month_name

create table cumulative_attendance_records_final select ar.student_class_map_id,ar.month_name,sum(at.present_days) as cumulative_present,sum(at.absent_days) as cumulative_absent,sum(at.late_days) as cumulative_late,sum(at.working_days) as cumulative_working from attendance_records_final ar join attendance_records_final at on ar.student_class_map_id=at.student_class_map_id and ar.month_name>=at.month_name group by 1,2;

drop table temp

drop table absent_table

drop table late_table




