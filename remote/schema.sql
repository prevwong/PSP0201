drop table if exists users;
create table users (
    id integer primary key autoincrement,
    name varchar(200) not null,
    password varchar(200) not null,
    description varchar(200) not null,
    exp int DEFAULT 0,
    weekly_exp int DEFAULT 0,
    level int DEFAULT 1
);