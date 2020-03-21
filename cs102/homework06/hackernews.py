from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, Session
from bayes import NaiveBayesClassifier, clean


@route("/news")
def news_list():
    s = Session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = Session()
    x = request.query.label
    y = request.query.id
    s.query(News).filter_by(id=y).update({'label': x})
    s.commit()
    redirect("/news")


@route("/update")
def update_news(url="https://news.ycombinator.com/newest", n=1, k=0):
    news_old, url = get_news(url, n, stop=n - 1)
    s = Session()
    for i in news_old:
        try:
            a = s.query(News.title).filter(News.title == i['title'])[2]
            print(a)
        except:
            news = News(title=i['title'],
                        author=i['author'],
                        url=i['url'],
                        comments=i['comments'],
                        points=i['points'])
            s.add(news)
            s.commit()
            k += 1
            print(k)
    if k < 30:
        update_news(url, n+1, k)
    else:
        redirect("/news")
        return
    redirect("/news")


@route("/recommendations")
def classify_news():
    s = Session()
    none_news = []
    rows = s.query(News).filter(News.label == None).all()
    learn_news = s.query(News).filter(News.label != None).all()
    X, y = [], []
    for news in learn_news:
        X.append(news.title)
        y.append(news.label)
    X = [clean(x).lower() for x in X]
    model = NaiveBayesClassifier(alpha=1)
    model.fit(X, y)
    for news in rows:
        none_news.append(news.title)
    predict_labels = model.predict(none_news)
    for news, label in zip(rows, predict_labels):
        news.label = label
    classified_news = sorted(rows, key=lambda news: news.label)
    return template('./classify.tpl', rows=classified_news)



if __name__ == "__main__":
    run(host="localhost", port=8080)
