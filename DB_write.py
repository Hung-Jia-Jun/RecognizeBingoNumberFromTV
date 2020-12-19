from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine,DateTime,Date
from sqlalchemy.orm import sessionmaker
import configparser
from datetime import datetime
import time
# 宣告對映
Base = declarative_base()

class Bingo(Base):
	__tablename__ = 'Test_Bingo'
	id = Column(Integer, primary_key=True)
	#開獎期數
	Bingo_Period = Column(Integer)
	#開獎號碼由小到大排序
	Bingo_Num = Column(String(255))
	#台彩開獎順序
	Bingo_Draw_Order_Num = Column(String(255))
	#記載年月日
	DrawDate = Column(Date)
	#記載時跟分
	DrawDT = Column(String(255))
	#固定寫入開獎號碼的第20個數字
	Bingo_Super_Num = Column(Integer)
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
		game = self.session.query(Bingo).filter(Bingo.Bingo_Period == gameID).first()
		
		Bingo_Num_li = sorted([int(x) for x in gameNumbers.split(",")])
		Bingo_Num_str = [str(x) for x in Bingo_Num_li]
		#由小到大排序數字
		Bingo_Num = ','.join(Bingo_Num_str)
		#取得現在時間
		now = time.localtime(time.time())
		DrawDate = datetime.now().date()
		DrawDT = "{mm}:{ss}".format(mm=now[3],ss=now[4])
		if game == None:
			#開獎期數 : Bingo_Period
			#開獎號碼由小到大排序 : Bingo_Num
			#台彩開獎順序 : Bingo_Draw_Order_Num
			#記載年月日 : DrawDate
			#記載時跟分 : DrawDT
			#固定寫入開獎號碼的第20個數字 : Bingo_Super_Num
			# 建立一對映類別的實例
			newBingo = Bingo(Bingo_Period=gameID,
							 Bingo_Num = Bingo_Num,
							 Bingo_Draw_Order_Num = gameNumbers,
							 DrawDate = DrawDate,
							 DrawDT = DrawDT,
							 Bingo_Super_Num = gameNumbers.split(",")[-1])
			# 新增
			self.session.add(newBingo)
			self.session.commit()    # 寫入。在commit()之前，也可rollback()
			return "Done"

		game.Bingo_Period = gameID
		game.Bingo_Num = Bingo_Nu
		game.Bingo_Draw_Order_Num = gameNumbers
		game.DrawDate = DrawDate
		game.DrawDT = DrawDT
		game.Bingo_Super_Num = gameNumbers.split(",")[-1]
		self.session.commit()    # 寫入。在commit()之前，也可rollback()
		return "Done"

if __name__ == "__main__":
	Database = Database()
	Database.updateDB(gameID=0,gameNumbers="19,13,17,12,11,17,20,45,67")