from sqlalchemy import create_engine
from sqlalchemy import Table, Column,VARCHAR,INTEGER,Float,String, MetaData,ForeignKey,Date,Text,DECIMAL
from sqlalchemy.sql import exists
import os
class Database():
    engine = create_engine('sqlite:///{}/db/library.db'.format(os.getcwd()))
    meta = MetaData()


    library_admin = Table('library_admin',meta,
                          Column('userid',INTEGER,primary_key=True),
                          Column('username',VARCHAR(50)),
                          Column('password',VARCHAR(50)))

    library_publication = Table('library_publication',meta,
                           Column('pubid',INTEGER,primary_key=True),
                           Column('alias', String),
                           Column('ordinance', String),
                           Column('ordinanceno', INTEGER),
                           Column('title',String),
                           Column('author',String),
                           Column('subject',String),
                           Column('department',String),
                           Column('placeissued',String),
                           Column('dateissued',Date),
                           Column('daterecieved',Date),
                           Column('description',String),
                           Column('datearchived',Date))

    library_periodicals = Table('library_periodicals', meta,
                                Column('id', INTEGER, primary_key=True),
                                Column('alias',String),
                                Column('title', String),
                                Column('subject', String),
                                Column('author', String),
                                Column('volume', String),
                                Column('periodiclano', INTEGER),
                                Column('issn', String),
                                Column('noofpages',INTEGER),
                                Column('publicationdate', Date),
                                Column('description', String),
                                Column('datearchived',Date))

    library_localhistory = Table('library_localhistory', meta,
                                Column('id', INTEGER, primary_key=True),
                                Column('alias',String),
                                Column('source', String),
                                Column('pages', String),
                                Column('title', String),
                                Column('author', String),
                                Column('subject',String),
                                Column('description', String),
                                Column('datearchived',Date))

    library_realia = Table('library_realia',meta,
                           Column('id', INTEGER, primary_key=True),
                           Column('alias', String),
                           Column('title', String),
                           Column('subject', String),
                           Column('length', INTEGER),
                           Column('width', INTEGER),
                           Column('dimension', String),
                           Column('author', String),
                           Column('noofcopies', INTEGER),
                           Column('location', String),
                           Column('series',String),
                           Column('description', String),
                           Column('datearchived',Date))

    library_sharedrive = Table('library_sharedrive',meta,
                               Column('sdid',INTEGER,primary_key=True),
                               Column('sharedrive',VARCHAR(50)))

    meta.create_all(engine)

    conn = engine.connect()

    s = library_admin.select()
    s_value = conn.execute(s)
    z = 0
    for val in s_value:
        z += 1

    if z == 0:
        ins = library_admin.insert().values(username = 'admin',
                                            password = 'admin')
        result = conn.execute(ins)

    conn = engine.connect()
    s = library_sharedrive.select()
    s_value = conn.execute(s)
    x = 0
    for val in s_value:
        x += 1
    loc = os.getcwd() + r'\sharedrive\archive_directory'
    if x == 0:
        ins = library_sharedrive.insert().values(sharedrive = loc)
        result = conn.execute(ins)