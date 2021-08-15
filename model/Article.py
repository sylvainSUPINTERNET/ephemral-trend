from app.main import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String(255))
    article_brand_name = db.Column(db.String(255))
    article_promo_percent = db.Column(db.String(255))
    article_promo_price = db.Column(db.String(255))
    article_real_price = db.Column(db.String(255))
    article_thumbnails_url = db.Column(db.Text())
    article_big_picture_urls = db.Column(db.Text())

    def __repr__(self):
        return '<Article %r>' % self.article_name
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}