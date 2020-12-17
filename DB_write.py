from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine,DateTime
from sqlalchemy.orm import sessionmaker
import configparser

class Bingo(Base):
	__tablename__ = 'Test_Bingo'
	gameID = Column(Integer, primary_key=True)
	num_0 = Column(Integer)
	num_1 = Column(Integer)
	num_2 = Column(Integer)
	num_3 = Column(Integer)
	num_4 = Column(Integer)
	num_5 = Column(Integer)
	num_6 = Column(Integer)
	num_7 = Column(Integer)
	num_8 = Column(Integer)
	num_9 = Column(Integer)
	num_10 = Column(Integer)
	num_11 = Column(Integer)
	num_12 = Column(Integer)
	num_13 = Column(Integer)
	num_14 = Column(Integer)
	num_15 = Column(Integer)
	num_16 = Column(Integer)
	num_17 = Column(Integer)
	num_18 = Column(Integer)
	num_19 = Column(Integer)
	num_20 = Column(Integer)
	update_time = Column(DateTime)


class Database():
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		_config = config['database']
		self.host = _config["host"]
		self.database = _config["database"]
		self.user = _config["user"]
		self.password = _config["password"]
		self.dbType = _config["dbType"]

		# 宣告對映
		Base = declarative_base()

		# self.connectStr = '{dbType}://{user}:{password}@{host}/{database}'.format(host = host,
		#                                                                 database =database,
		#                                                                 user = user,
		#                                                                 password=password,
		#                                                                 dbType = 'mysql+pymysql')
		# self.engine = create_engine(self.connectStr)

		self.engine = create_engine('sqlite:///recognize_db.db')
		Base.metadata.bind = self.engine
		# 建立Session
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
	def updateDB(self,gameID,gameNumbers):
		for number in gameNumbers:
			pass
		# 建立一對映類別的實例
		# newBingo = Bingo(gameID='0')
		# # 新增
		# self.session.add(newBingo)
		# self.session.commit()    # 寫入。在commit()之前，也可rollback()

		# 查詢
		game = self.session.query(Bingo).first()
		game.num_0 = 22
		self.session.commit()    # 寫入。在commit()之前，也可rollback()

		print(game.gameID)
		print(game.num_0)
