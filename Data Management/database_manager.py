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
    activity = Column(String)
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

    def get_all_queries(self):
        session = self.Session()
        queries = session.query(Query).all()
        session.close()
        return queries

    def update_query(self, query_id, new_query=None, new_response=None, new_prediction=None):
        session = self.Session()
        query = session.query(Query).filter(Query.id == query_id).first()
        if query:
            if new_query:
                query.query = new_query
            if new_response:
                query.response = new_response
            if new_prediction:
                query.prediction = new_prediction
            session.commit()
            logging.info(f"Updated query with ID {query_id}")
            session.close()
            return True
        else:
            logging.warning(f"No query found with ID {query_id}")
            session.close()
            return False

    # New method to log user activity
    def log_user_activity(self, activity, start_time, end_time=None):
        session = self.Session()
        new_activity = UserActivity(activity=activity, start_time=start_time, end_time=end_time)
        session.add(new_activity)
        session.commit()
        logging.info("User activity logged successfully")
        session.close()

    # Placeholder for methods to retrieve user activities
    # def get_recent_activities(self):
    #     # Implement logic to fetch recent user activities
    #     pass

# Example usage
# db_manager = DatabaseManager('path_to_database')
# db_manager.add_query("Sample query", "Sample response")
# print(db_manager.get_all_queries())
