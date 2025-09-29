-- init.sql
    CREATE TABLE IF NOT EXISTS pictures(
    id SERIAL PRIMARY KEY,
    img_url VARCHAR(500) UNIQUE NOT NULL,
    rating INTEGER NOT NULL,
    date VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pictures_rating ON pictures(rating DESC);
CREATE INDEX IF NOT EXISTS idx_pictures_created_at ON pictures(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pictures_url ON pictures(img_url);

COMMENT ON TABLE pictures IS 'Таблица для хранения картинок с JoyReactor';
COMMENT ON COLUMN pictures.img_url IS 'URL изображения';
COMMENT ON COLUMN pictures.rating IS 'Рейтинг картинки';
COMMENT ON COLUMN pictures.date IS 'Дата публикации';
COMMENT ON COLUMN pictures.created_at IS 'Время добавления в базу';


DO $$
BEGIN
    RAISE NOTICE 'Таблица pictures успешно создана или уже существует';
END $$;