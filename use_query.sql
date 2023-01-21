use stock_store;

create table login_table
(
    id int not null primary key auto_increment,
    username VARCHAR(20) not null unique,
    password varchar(20),
    create_at datetime default current_timestamp
);