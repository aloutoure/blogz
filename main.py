from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:avery2015@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = 'mychildrenaremyworld2017'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    title_error = "Please fill in the title"
    content_error = "Pleae fill in the body"
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        if blog_title == '' and blog_content == '':
            return render_template('newpost.html', title_error=title_error, content_error=content_error)
        elif blog_title == '':
            return render_template('newpost.html', title_error=title_error, blog_content=blog_content)
        elif  blog_content == '':
            return render_template('newpost.html', content_error=content_error, blog_title=blog_title)
        else:
            new_post = Blog(blog_title, blog_content)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/single_entry?id=' + str(new_post.id))
    
    return render_template('newpost.html')

@app.route('/single_entry', methods=['GET'])
def single_entry():
    blog_id = int(request.args.get('id'))
    blog_post = Blog.query.get(blog_id)
    return render_template('single_entry.html', new_blog=blog_post)
    

@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/', methods=['GET'])
def index():

    return redirect('/blog')

if __name__ == '__main__':
    app.run()
