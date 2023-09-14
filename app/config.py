# config.py

class Config:
    # Other configuration settings...

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:ISDS4125@plnru2.c3omnzoqavtp.us-east-2.rds.amazonaws.com:1433/PLNRU'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable SQLAlchemy's modification tracking feature

    SECRET_KEY = 'f73b6595e38ca270c86a88b80392023e'
