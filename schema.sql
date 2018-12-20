create table if not exists Links (
    short text primary key,
    full text,
    visits integer default 0,
    accessed datetime,
    created datetime default current_timestamp
)
