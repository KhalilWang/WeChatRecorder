create table student(
    sname text primary key NOT NULL,
    cid text
);

create table class(
    cid text primary key NOT NULL,
    tid text,
    cname text
);

create table teacher(
    tid text primary key NOT NULL,
    tname text
);

create table record(
    sname text NOT NULL,
    rid text NOT NULL primary key,
    rtime text NOT NULL
);
