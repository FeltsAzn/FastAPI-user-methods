# from sqlalchemy import Table, Column, MetaData, Integer, String, Identity, create_engine, select
# from conf_db import postgresql as settings
#
#
# def connecting(user, password, host, db_name):
#     try:
#         engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{db_name}', echo=True)
#         connect = engine.connect()
#         metadata = MetaData(engine)
#     except Exception as _ex:
#         raise _ex
#     else:
#         print('Connection succesfully')
#         return connect, metadata
# #
#
#   # метаданные дял создания различных таблиц
# # metadata.create_all(engine)
#
# conn, meta = connecting(
#     user=settings['user'],
#     password=settings['password'],
#     host=settings['host'],
#     db_name=settings['db_name']
# )
#
# cards_table = Table('test_db', meta, autoload=True)
# # update_query = cards_table.insert().values(id=1,
# #                                            deck_name='SQL',
# #                                            question='Виды склейки таблиц',
# #                                            answer='Left, Right, Cross, inner'
# #                                            )
# # conn.execute(update_query)
#
# s = select(cards_table)
# result = conn.execute(s)
#
# for row in result.fetchall():
#     print(row)
#
# conn.close()

from sqlalchemy import Column, Integer, String, FLOAT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# создание подключения к таблице
engine = create_engine(f'postgresql+psycopg2://postgres:felts@localhost/postgres', echo=True)
Base = declarative_base() # класс, на основе которого мы связываем классы питона и таблицы в бд


class Book(Base):
    __tablename__ = 'books'  # прямой указатель на таблицу в бд

    book_id = Column(Integer, primary_key=True, autoincrement=True)  # заполняемое поле в таблице
    title = Column(String(250), nullable=False)  # заполняемое поле в таблице
    price = Column(FLOAT)  # заполняемое поле в таблице
    amount = Column(Integer)  # заполняемое поле в таблице
    author_id = Column(Integer, ForeignKey('authors.author_id'))  # заполняемое поле в таблице с внешним ключом
    Author = relationship('Author')  # связь между двумя таблицами


class Author(Base):
    __tablename__ = 'authors'  # прямой указатель на таблицу в бд

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String(250), nullable=False)
    book = relationship('Book')


try:
    """Конструкция для добавления новых таблиц в базу данных на основе классов,
    что созданы."""
    Base.metadata.create_all(engine)
except Exception as _ex:
    raise _ex
else:
    print('Succesfully')


session = sessionmaker(bind=engine) # Сессия для реализации CRUD методов в базе
s = session()

author_add = Author(author_name='Достоевский')  # берём наш класс, который проинициализирован и
# связан с таблицей authors и добавляем нужные поля

s.add(author_add)  # добавляем добавленный столбец в нашу сессию
s.commit()  # Коммитим для сохранения

author_add = Author(author_name='Булгаков')
s.add(author_add)
s.commit()


s.add_all([
    Book(title='Мастер и Маргарита', price='1254', amount='15', author_id=2),
    Book(title='Преступление и наказание', price='1034.5', amount='6', author_id=1),
    Book(title='Белая гвардия', price='895', amount='8', author_id=2)
])
# Сразу добавляем список позиций, который хотим вставить в тиблицу Book.
# Для этого используем проинициализированный
# класс, что связан с нашей таблицей books в базе данных

s.commit()