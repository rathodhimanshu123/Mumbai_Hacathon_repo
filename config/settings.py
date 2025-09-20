import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GOOGLE_FIT_CLIENT_ID = os.getenv('GOOGLE_FIT_CLIENT_ID')
    GOOGLE_FIT_CLIENT_SECRET = os.getenv('GOOGLE_FIT_CLIENT_SECRET')
    GOOGLE_FIT_REDIRECT_URI = os.getenv('GOOGLE_FIT_REDIRECT_URI')
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}