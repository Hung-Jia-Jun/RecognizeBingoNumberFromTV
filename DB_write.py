from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine,DateTime
from sqlalchemy.orm import sessionmaker
import configparser
from datetime import datetime
# 宣告對映
Base = declarative_base()

class Bingo(Base):
	__tablename__ = 'Test_Bingo'
	gameID = Column(Integer, primary_key=True)
	numbers = Column(String(255))
	
	#此次賓果的數字數量有多少
	bingoPeriodsLength = Column(Integer)
	update_time = Column(DateTime)


class Database:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		_config = config['database']
		self.host = _config["host"]
		self.database = _config["database"]
		self.user = _config["user"]
		self.password = _config["password"]
		self.dbType = _config["dbType"]
		if self.dbType == "mysql+pymysql":
			self.connectStr = '{dbType}://{user}:{password}@{host}/{database}'.format(host = self.host,
																			database = self.database,
																			user = self.user,
																			password = self.password,
																			dbType = self.dbType)
			self.engine = create_engine(self.connectStr)
		else:
			#使用本機的local host sqlite db
			self.engine = create_engine('sqlite:///recognize_db.db')
		Base.metadata.bind = self.engine
		# 建立Session
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
	def updateDB(self,gameID,gameNumbers):
		bingoPeriodsLength = len(gameNumbers.split(","))
		# 查詢
		game = self.session.query(Bingo).filter(Bingo.gameID == gameID).first()
		if game == None:
			# 建立一對映類別的實例
			newBingo = Bingo(gameID=gameID,
							 numbers = gameNumbers,
							 update_time = datetime.now(),
							 bingoPeriodsLength = bingoPeriodsLength)
			# 新增
			self.session.add(newBingo)
			self.session.commit()    # 寫入。在commit()之前，也可rollback()
			return "Done"

		game.gameID = gameID
		game.numbers = gameNumbers
		game.bingoPeriodsLength = bingoPeriodsLength
		game.update_time = datetime.now()
		self.session.commit()    # 寫入。在commit()之前，也可rollback()
		return "Done"

if __name__ == "__main__":
	Database = Database()
	Database.updateDB(gameID=0,gameNumbers="12,11,17,12,11,17,20,45,67")