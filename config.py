from datetime import datetime
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///uai_odonto.db'
    SECRET_KEY = 'uai-odonto-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # True para debug, False para produção
