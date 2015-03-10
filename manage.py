# coding: utf-8
import HTMLParser
import traceback
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db, Blog, Post, GrabLog
from application.utils.blog import grab_by_feed


# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# db migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """Run app."""
    app.run(port=PORT)


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server
    import formic

    server = Server(app)

    # css
    for filepath in formic.FileSet(include="application/static/css/**/*.css"):
        server.watch(filepath)
    # html
    for filepath in formic.FileSet(include="application/templates/css/**/*.html"):
        server.watch(filepath)
    # js
    for filepath in formic.FileSet(include="application/static/js/**/*.js"):
        server.watch(filepath)
    # image
    for filepath in formic.FileSet(include="application/static/image/**/*.*"):
        server.watch(filepath)

    server.serve(port=PORT)


@manager.command
def createdb():
    """Create database."""
    db.create_all()


@manager.command
def grab_feed():
    """通过feed爬取博文"""
    with app.app_context():
        for blog in Blog.query:
            grab_by_feed(blog)


@manager.command
def grab_spider():
    """通过spider爬取博文"""
    from spiders import grab_by_spider, spiders

    with app.app_context():
        for spider in spiders:
            grab_by_spider(spider)


@manager.command
def grab():
    """爬取博文"""
    import logging
    from spiders import grab_by_spider, spiders

    logging.basicConfig(filename='grab.log', level=logging.DEBUG)

    with app.app_context():
        new_posts_count = 0

        # 通过feed抓取blog
        for blog in Blog.query:
            if blog.feed and blog.is_approved:
                try:
                    new_posts_count += grab_by_feed(blog)
                except Exception, e:
                    log = GrabLog(message=e, details=traceback.format_exc(), blog_id=blog.id)
                    db.session.add(log)
                    db.session.commit()

        # 通过spider抓取blog
        for spider in spiders:
            try:
                new_posts_count += grab_by_spider(spider)
            except Exception, e:
                blog = Blog.query.filter(Blog.url == spider.url).first_or_404()
                log = GrabLog(message=e, details=traceback.format_exc(), blog_id=blog.id)
                db.session.add(log)
                db.session.commit()


@manager.command
def remote_grab():
    from celery_proj.tasks import grab

    grab.delay()


@manager.command
def test_grab(id):
    blog = Blog.query.get_or_404(id)
    grab_by_feed(blog)


# @manager.command
# def remote_analyse():
# from celery_proj.tasks import analyse
#
# analyse.delay()


@manager.command
def process_posts():
    """生成pure_content, keywords"""
    with app.app_context():
        for post in Post.query:
            print(post.title)
            post.update()
            db.session.add(post)
        db.session.commit()


@manager.command
def process_published():
    """不存在published_at的post，使用updated_at替代"""
    with app.app_context():
        for post in Post.query:
            print(post.title)
            if not post.published_at:
                post.published_at = post.updated_at
                db.session.add(post)
        db.session.commit()


@manager.command
def unescape_title():
    html_parser = HTMLParser.HTMLParser()
    with app.app_context():
        for post in Post.query:
            print(post.title)
            post.title = html_parser.unescape(post.title)
            db.session.add(post)
        db.session.commit()


if __name__ == "__main__":
    manager.run()
