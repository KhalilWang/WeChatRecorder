create table student(
    sid text primary key NOT NULL,
    sname text NOT NULL,
    cid text
);

create table class(
    cid text primary key NOT NULL,
    tid text NOT NULL,
    cname text NOT NULL
);

create table teacher(
    tid text primary key NOT NULL
);

create table srecord(
    sid text,
    media_id text primary key NOT NULL
);

create table trecord(
    media_id text primary key NOT NULL,
    trid text UNIQUE NOT NULL
);

create table homework_content(
    hid text,
    trid text
);

create table homework(
    cid text NOT NULL,
    hid text primary key NOT NULL,
    hname text
);
