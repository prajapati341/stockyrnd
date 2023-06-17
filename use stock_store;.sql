use stock_store;

ALTER TABLE stock_data_interval ADD column id INT NOT NULL AUTO_INCREMENT primary key;

desc stock_data_interval;

select distinct company_name,company_code from stock_data;

select * from stock_data_interval;

desc stock_data;


select distinct company_name,company_code from stock_data where company_code='TATAMOTORS.NS'


select max(datetime) from stock_data_interval where company_code='TATAMOTORS.NS';


select  datetime,open,high,low,close,'Adj Close',volume,company_name,company_code from stock_data_interval 
where company_code='TATAMOTORS.NS'; limit 5;


DELETE n1 FROM 
            (
                select * FROM stock_data_interval
                WHERE datetime between '2023-02-09 00:00:00' and '2023-02-10 23:59:59'
                and  company_code='TATAMOTORS.NS'
            ) n1, 
            (
                select * FROM stock_data_interval
                WHERE datetime between '2023-02-09 00:00:00' and '2023-02-10 23:59:59'
                and  company_code='TATAMOTORS.NS'
            ) n2 
WHERE n1.id < n2.id AND 
n1.datetime = n2.datetime;

desc stock_data

select * from stock_data limit 10;

delete from stock_data;

create table stock_data_temp like stock_data;
delete from stock_data_temp
delete from stock_data

create table stock_data_interval_temp like stock_data_interval;

insert into stock_data_temp (Date,open,high,low,close,`Adj Close`,volume,company_name,company_code)
select distinct  Date,open,high,low,close,`Adj Close`,volume,company_name,company_code from stock_data;

insert into stock_data
select * from stock_data_temp



insert into stock_data_interval_temp (Datetime,open,high,low,close,`Adj Close`,volume,company_name,company_code)
select distinct  Datetime,open,high,low,close,`Adj Close`,volume,company_name,company_code from stock_data_interval;

select * from  stock_data_interval;
delete from stock_data_interval_temp
delete from stock_data_interval


select company_name,company_code,concat(date(max(date)),' 00:00:00') max_date,date_add(date(max(date)),interval 1 day) start_date,date(now()) end_date  from stock_data  group by company_name,company_code;



select distinct company_name,company_code,max(datetime) max_date  from stock_data_interval  
group by company_name,company_code;


delete from stock_data_interval
where datetime>='2023-02-10 00:00:00'



delete from stock_data
where date>='2023-02-10 00:00:00';


select * from stock_data_interval
where company_code='^NSEI';


select * from stock_data_interval
where company_code='^NSEI' limit 5
and datetime>='2023-02-13 12:00:00';




select distinct datetime,open,high,low,close,'Adj Close',volume,company_name,company_code from stock_data_interval 
where company_code='TATAMOTORS.NS'; limit 5;


delete from  stock_data_interval
where company_code='^NSEI'

select min(datetime) from stock_data_interval
where company_code='^NSEI'


select distinct company_name,company_code,max(Datetime) max_date from stock_data_interval where company_code='^NSEI'
group by company_name,company_code;




CREATE TABLE user_chart_img 
(
image_id int(10) NOT NULL auto_increment,
chart_image blob,
users_id int(50),
users_name varchar(100),
 PRIMARY KEY (`image_id`) 
 );


 select * from user_chart_img;


 select count(*) from stock_data_interval
where company_code='RTNINDIA.NS'
and datetime>='2023-02-23 00:00:00';


-- delete from stock_data_interval
-- where company_code='RTNINDIA.NS'
-- and datetime>='2023-02-23 00:00:00'


 select * from stock_data_interval
where company_code='RTNINDIA.NS'
and datetime;


select concat(date(date_add(now(),interval -2 day)),' 00:00:00');


select distinct date(datetime) from stock_data_interval  
            where company_code='^NSEI'
            and datetime>=concat(date(date_add(now(),interval -2 day)),' 00:00:00');
