from app.main import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String(255))
    article_brand_name = db.Column(db.String(255))
    article_promo_percent = db.Column(db.String(255))
    article_promo_price = db.Column(db.String(255))
    article_real_price = db.Column(db.String(255))

    def __repr__(self):
        return '<Article %r>' % self.article_name