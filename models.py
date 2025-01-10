import json

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

engine = create_engine('postgresql://himanshumishra:himanshumishra@localhost:5432/key_features_poc')
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class KeyFeatures(Base):
    __tablename__ = 'key_features'

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    brand_name = Column(String, nullable=False)
    key_features = Column(JSON, nullable=True)

    @staticmethod
    def add_key_features_entry(model_id, model_name, brand_name, key_features):
        with Session() as session:
            new_key_features_entry = KeyFeatures(
                id=model_id,
                model_name=model_name,
                brand_name=brand_name,
                key_features=key_features
            )
            session.add(new_key_features_entry)
            session.commit()

    @staticmethod
    def update_key_features_to_json():
        with Session() as session:
            key_features_entries = session.query(KeyFeatures).all()[1:]
            for entry in key_features_entries:
                if entry.key_features:
                    entry.key_features = json.loads(entry.key_features)
            session.commit()



def create_key_features_table(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    KeyFeatures.update_key_features_to_json()
