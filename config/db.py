from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///userlogs.db")
meta = MetaData()
conn = engine.connect()
