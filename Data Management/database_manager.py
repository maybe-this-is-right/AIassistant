# database_manager.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import logging

logging.basicConfig(filename='database_manager.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

Base = declarative_base()

class Query(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    query = Column(String)
    response = Column(String)
    prediction = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class UserActivity(Base):
    __tablename__ = 'user_activities'
    id = Column(Integer, primary_key=True)
    activity_type = Column(String)
    activity_description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)

class DatabaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logging.info("Database Manager initialized with SQLAlchemy")

    def add_query(self, query, response, prediction=None):
        session = self.Session()
        new_query = Query(query=query, response=response, prediction=prediction, timestamp=datetime.datetime.utcnow())
        session.add(new_query)
        session.commit()
        logging.info("Query added successfully")
        session.close()

    def log_user_activity(self, activity_type, activity_description, start_time, end_time=None):
        session = self.Session()
        new_activity = UserActivity(activity_type=activity_type, 
                                    activity_description=activity_description,
                                    start_time=start_time, 
                                    end_time=end_time)
        session.add(new_activity)
        session.commit()
        logging.info("User activity logged successfully")
        session.close()

    def get_all_user_activities(self):
        session = self.Session()
        activities = session.query(UserActivity).all()
        session.close()
        return activities

class TimeManagementLogs(Base):
    __tablename__ = 'time_management_logs'
    id = Column(Integer, primary_key=True)
    logon_time = Column(DateTime)
    logoff_time = Column(DateTime)
    duration = Column(Integer)  # Duration in minutes

class MoodLogs(Base):
    __tablename__ = 'mood_logs'
    id = Column(Integer, primary_key=True)
    mood_rating = Column(Float)
    specific_emotions = Column(String)
    triggers = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)

class DatabaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_time_management_log(self, logon_time, logoff_time, duration):
        session = self.Session()
        try:
            new_log = TimeManagementLogs(logon_time=logon_time, logoff_time=logoff_time, duration=duration)
            session.add(new_log)
            session.commit()
        except Exception as e:
            logging.error(f"Error adding time management log: {e}")
        finally:
            session.close()

    def add_mood_log(self, mood_rating, specific_emotions, triggers):
        session = self.Session()
        try:
            new_log = MoodLogs(mood_rating=mood_rating, specific_emotions=specific_emotions, triggers=triggers)
            session.add(new_log)
            session.commit()
        except Exception as e:
            logging.error(f"Error adding mood log: {e}")
        finally:
            session.close()