from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SECRET_KEY'] = 'preetandpaya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_APP_NAME'] = 'GKUIZ'
app.config['USER_SEND_PASSWORD_CHANGED_EMAIL'] = False
app.config['USER_SEND_REGISTERED_EMAIL'] = False
app.config['USER_SEND_USERNAME_CHANGED_EMAIL'] = False
app.config['USER_ENABLE_CONFIRM_EMAIL'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
photos = UploadSet('photos',IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	active = db.Column(db.Boolean(), nullable=False, server_default='0')	
	Sports_score = db.Column(db.Integer, nullable=False, default=0)
	cricket_score = db.Column(db.Integer, nullable=False, default=0)
	football_score = db.Column(db.Integer, nullable=False, default=0)
	Movies_score = db.Column(db.Integer, nullable=False, default=0)
	bollywood_score = db.Column(db.Integer, nullable=False, default=0)
	hollywood_score = db.Column(db.Integer, nullable=False, default=0)
	Current_affairs_score = db.Column(db.Integer, nullable=False, default=0)
	technology_score = db.Column(db.Integer, nullable=False, default=0)
	politics_score = db.Column(db.Integer, nullable=False, default=0)
	Literature_score = db.Column(db.Integer, nullable=False, default=0)
	english_score = db.Column(db.Integer, nullable=False, default=0)
	hindi_score = db.Column(db.Integer, nullable=False, default=0)
	History_score = db.Column(db.Integer, nullable=False, default=0)
	foreign_score = db.Column(db.Integer, nullable=False, default=0)
	indian_score = db.Column(db.Integer, nullable=False, default=0)
	Science_score = db.Column(db.Integer, nullable=False, default=0)
	chemistry_score = db.Column(db.Integer, nullable=False, default=0)
	physics_score = db.Column(db.Integer, nullable=False, default=0)
	email = db.Column(db.String(255), nullable=False, unique=True)
	bio = db.Column(db.String(500))
	dob = db.Column(db.String(11), server_default='-----------')
	role = db.Column(db.Boolean(), default=False)

class Questions(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(300), nullable=False, unique=True)
	option1 = db.Column(db.String(40), nullable=False)
	option2 = db.Column(db.String(40), nullable=False)
	option3 = db.Column(db.String(40), nullable=False)
	option4 = db.Column(db.String(40), nullable=False)
	ans1 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans2 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans3 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans4 = db.Column(db.Boolean(), nullable=False, server_default='0')
	QuizCategory = db.Column(db.String(50), nullable=False)
	Type = db.Column(db.String(50), nullable=False)

class States(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	category = db.Column(db.String(50), nullable=False, server_default='tech')
	maincategory = db.Column(db.String(50), nullable=False, server_default='Movies')
	mainflag = db.Column(db.Boolean(), nullable=False, server_default='0')
	partialscore = db.Column(db.String(10), nullable=False, server_default='0')
	numofinc = db.Column(db.Integer, nullable=False, default=0)
	fifty50 = db.Column(db.Boolean, nullable=False, server_default='0')
	onecorrect = db.Column(db.Boolean, nullable=False, server_default='0')
	q50 = db.Column(db.Integer, nullable=False, default=0)
	for i in range(10):
		for j in range(4):
			locals()['Q{}A{}'.format(i, j)] = db.Column(db.Boolean(), nullable=False, server_default='0')
		locals()['Q{}'.format(i)] = db.Column(db.Boolean(), nullable=False, server_default='0') 

class MyModelView(ModelView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:
				return True
			return False
		return False

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:	
				return True
			return False
		return False

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Questions, db.session))
admin.add_view(MyModelView(States, db.session))

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

def init_db():
	db.init_app(app)
	db.drop_all()
	db.create_all()

def sortscore(category):
	result1 = db.engine.execute('SELECT username FROM User')
	resultSports = db.engine.execute('SELECT Sports_score FROM User')
	resultMovies = db.engine.execute('SELECT Movies_score FROM User')
	resultLiterature = db.engine.execute('SELECT Literature_score FROM User')
	resultCurrentaffairs = db.engine.execute('SELECT Current_affairs_score FROM User')
	resultHistory = db.engine.execute('SELECT History_score FROM User')
	resultScience = db.engine.execute('SELECT Science_score FROM User')
	dictionary={}
	name=[]
	for i in result1:
		name.append(i[0])

	score=[]	
	if category == 'globalrank':
		for i in resultSports:
			score.append(i[0])

		j=0
		for i in resultMovies:
			score[j]+=i[0]
			j+=1
		j=0
		for i in resultLiterature:
			score[j]+=i[0]
			j+=1
		j=0
		for i in resultCurrentaffairs:
			score[j]+=i[0]
			j+=1
		j=0
		for i in resultHistory:
			score[j]+=i[0]
			j+=1
		j=0
		for i in resultScience:
			score[j]+=i[0]
			j+=1
		for i in range(len(name)):
			dictionary[name[i]] = score[i]

		sorted_tuple = sorted(dictionary.items(), key=lambda x: (x[1], x[0]), reverse=True)
		return sorted_tuple
	
	else:
		for i in locals()['result' + str(category)]:
			score.append(i[0])

		for i in range(len(name)):
			dictionary[name[i]] = score[i]

		sorted_tuple = sorted(dictionary.items(), key=lambda x: (x[1], x[0]), reverse=True)
		return sorted_tuple

def scoreupdate(scoredata):
	row = States.query.filter_by(username=current_user.username).first()
	if row != None:
		row.mainflag = False
	row = User.query.filter_by(username=current_user.username).first()
	if scoredata['maincategory'] == 'Sports':
		row.Sports_score += scoredata['score']
		if scoredata['subcategory'] == 'cricket':
			row.cricket_score += scoredata['score']
		else:
			row.football_score += scoredata['score']
	elif scoredata['maincategory'] == 'Movies':
		row.Movies_score += scoredata['score']
		if scoredata['subcategory'] == 'bollywood':
			row.bollywood_score += scoredata['score']
		else:
			row.hollywood_score += scoredata['score']
	elif scoredata['maincategory'] == 'CurrentAffairs':
		row.Current_affairs_score += scoredata['score']
		if scoredata['subcategory'] == 'tech':
			row.technology_score += scoredata['score']
		else:
			row.politics_score += scoredata['score']
	elif scoredata['maincategory'] == 'Literature':
		row.Literature_score += scoredata['score']
		if scoredata['subcategory'] == 'hindi':
			row.hindi_score += scoredata['score']
		else:
			row.english_score += scoredata['score']
	elif scoredata['maincategory'] == 'History':
		row.History_score += scoredata['score']
		if scoredata['subcategory'] == 'indian':
			row.indian_score += scoredata['score']
		else:
			row.foreign_score += scoredata['score']
	elif scoredata['maincategory'] == 'Science':
		row.Science_score += scoredata['score']
		if scoredata['subcategory'] == 'physics':
			row.physics_score += scoredata['score']
		else:
			row.chemistry_score += scoredata['score']
	db.session.commit()

def addstate(data):
	if not States.query.filter_by(username=current_user.username).first():
		new_user_state = States(username=current_user.username)
		db.session.add(new_user_state)
		db.session.commit()
	user_data = States.query.filter_by(username=current_user.username).first()
	for key, value in data.items():
		setattr(user_data, key, value)
		db.session.commit()
	user_data.mainflag=1
	db.session.commit()

def getdetails(username):
	rank = 0
	sorted_tuple = sortscore('globalrank')
	for i in sorted_tuple:
		rank = rank + 1	
		if i[0] == username:
			score = i[1]
			break
	
	return score, rank

def generateplay(category):
	result = db.engine.execute("SELECT * FROM Questions WHERE QuizCategory = '" + str(category) + "';")
	arr = []
	for i in result:
		arr.append(i)
	return arr

def update(request):
	newdob = request.form['newdob']
	newbio = request.form['newbio']
	if newdob!=None:
		current_user.dob=newdob
	if newbio!=None:
		current_user.bio=newbio
	db.session.commit() 
