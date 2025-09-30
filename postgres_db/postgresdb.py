import time
from config import config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String, unique=True, nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())


class Repository:
    def __init__(self):
        self.DB_URL = (f"postgresql://{config.DB_CONFIG['user']}:{config.DB_CONFIG['password']}"
                       f"@{config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG["dbname"]}")
        self.engine = create_engine(self.DB_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(bind=self.engine)
        print("✅ Таблицы созданы")


    def save_to_db(self, pictures):
        db = self.SessionLocal()
        try:
            for picture_data in pictures:
                picture = Picture(
                    img_url= picture_data["img_url"],
                    rating = picture_data["rating"],
                    date = picture_data["date"]
                )
                db.add(picture)
            db.commit()
            print(f"✅ Сохранено: {len(pictures)} изображений")
        except Exception as e:
            db.rollback()
            print(f"❌ Ошибка сохранения: {e}")
        finally:
            db.close()

    def get_best_pictures(self):
        db = self.SessionLocal()
        pictures = db.query(Picture).filter(Picture.rating > 150).order_by(Picture.rating.desc()).all()
        db.close()
        return [{"img_url": p.img_url, "rating": p.rating} for p in pictures]

    def get_good_pictures(self):
        db = self.SessionLocal()
        pictures = db.query(Picture).order_by(Picture.rating.desc()).all()
        db.close()
        return [{"img_url": p.img_url, "rating": p.rating} for p in pictures]

repository = Repository()


