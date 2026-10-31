
from .database import Base, engine
from . import models

# Create all database tables
Base.metadata.create_all(bind=engine)

print("QueueLess database tables created successfully!")
