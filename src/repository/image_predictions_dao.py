from database import Database


class ImagePredictionsDAO:
    def __init__(self, db: Database):
        self.db = db

    def init_table(self):
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS image_predictions (
                filename TEXT NOT NULL PRIMARY KEY,
                is_male BOOLEAN NOT NULL
            )
            '''
        )

    def insert_image_predictions(
            self,
            image_name: str,
            is_male: bool,
    ):
        self.db.execute(
            '''
            INSERT INTO image_predictions (image_name, is_male) VALUES 
                (%s, %s)
            ''',
            args=(image_name, is_male)
        )
