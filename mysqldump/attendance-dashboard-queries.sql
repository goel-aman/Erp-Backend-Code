create table present_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as present_days from student_attendance_map where status='P' group by 1,2 order by 1,2);

create table working_table as (select student_class_map_id,concat(year(attendance_date),month(attendance_date)) as month_name,count(*) as working_days from student_attendance_map group by 1,2 order by 1,2);

create table attendance_records select wt.student_class_map_id,wt.month_name,pt.present_days,wt.working_days from present_table pt join working_table wt on pt.student_class_map_id=wt.student_class_map_id and wt.month_name=pt.month_name;

create table cumulative_attendance_records select ar.student_class_map_id,ar.month_name,sum(at.present_days),sum(at.working_days) from attendance_records ar join attendance_records at on ar.student_class_map_id=at.student_class_map_id and ar.month_name>=at.month_name group by 1,2;

#student-attendance-for-each-month
select month_name,(car.cumulative_present/car.cumulative_working)*100 as attendance_percent from student_class_mapping scm join cumulative_attendance_records car on scm.id=car.student_class_map_id where scm.student_id=253;

#best-performer-student_class_map_id

select car.student_class_map_id from student_class_mapping scm join cumulative_attendance_records car on scm.id=car.student_class_map_id where scm.class_id in (select class_id from student_class_mapping where student_id=253) and car.month_name in (select max(month_name) from cumulative_attendance_records) order by cumulative_present desc limit 1;

select month_name,(cumulative_present/cumulative_working)*100 as attendance_percent from cumulative_attendance_records where student_class_map_id in (7);

#worst-performer-student_class_map_id

select car.student_class_map_id from student_class_mapping scm join cumulative_attendance_records car on scm.id=car.student_class_map_id where scm.class_id in (select class_id from student_class_mapping where student_id=253) and car.month_name in (select max(month_name) from cumulative_attendance_records) order by cumulative_present limit 1;

select month_name,(cumulative_present/cumulative_working)*100 as attendance_percent from cumulative_attendance_records where student_class_map_id in (1);

#avg-class-performance -teacher-view

select month_name,avg((cumulative_present/cumulative_working)*100) as attendance_percent from student_class_mapping scm join cumulative_attendance_records car on scm.id=car.student_class_map_id where scm.class_id in (select class_id from student_class_mapping where class_id=1) group by 1;



