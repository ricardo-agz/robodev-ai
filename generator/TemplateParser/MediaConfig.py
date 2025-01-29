class MediaConfig:
    """
      MediaConfig contains all the configurations needed to host images/media
      in the cloud.
      Attributes
      ----------
    """

    # TODO: add AWS specific credentials, firebase
    def __init__(self, database_type: str) -> None:
        self.database_type = database_type

    def get_database_type(self):
        return self.database_type
