class Config:
  pass

class ProductionConfig(Config):
  DEBUG = False

class DevConfig(Config):
  DEBUG = True