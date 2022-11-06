class Config:
  pass

class ProductionConfig(Config):
  DEBUG = False

class DevConfig(Config):
  DEBUG = True
  print("THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.")