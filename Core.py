import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import Flask, render_template, request, redirect
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from models import *
import json

@app.route('/home')
def index():
	return render_template('home.html')

@app.route('/')
@login_required
def profile():
	return render_template('dashboard.html', currentuser=current_user.username)

@app.route('/leaderboard/<category>')
@login_required
def leaderboard(category):
	stuple=sortscore(category)
	return render_template('leaderboard.html', stuple=stuple, cat=category, currentuser=current_user.username)

@app.route('/recievefromjs', methods=['POST', 'GET'])
@login_required
def recieve():
	data = request.get_json(force=True)
	addstate(data)	
	return "Great"

@app.route('/resume')
@login_required
def resume():
	Data = States.query.filter_by(username=current_user.username).first()
	if Data == None or Data.mainflag == 0:
		return "You have no saved games"
	else:
		Dict={}
		Dict['category'] = Data.category
		Dict['maincategory'] = Data.maincategory
		Dict['numofinc'] = Data.numofinc
		Dict['partialscore'] = Data.partialscore
		Dict['fifty50'] = Data.fifty50
		Dict['onecorrect'] = Data.onecorrect
		Dict['q50'] = Data.q50
		for i in range(10):
			Dict['Q' + str(i)] = Data.__dict__['Q' + str(i)]
			for j in range(4):
				Dict['Q' + str(i) + 'O' + str(j)] = Data.__dict__['Q' + str(i) + 'A' + str(j)]
		listoftuples = generateplay(Dict['category'])
		dlist = [list(elem) for elem in listoftuples]
		return render_template('resume.html', data=Dict, array=dlist, currentuser=current_user.username)

@app.route('/profile/<user>')
@login_required
def userprofile(user):
	row = User.query.filter_by(username=user).first()
	score, rank=getdetails(user)
	return render_template(
		'userprofile.html', username=user, rank=rank, score=score, 
		bio=row.bio, mail=row.email, ide=row.id, dob=row.dob,
		sports=row.Sports_score, movies=row.Movies_score,
		history=row.History_score, science=row.Science_score,
		literature=row.Literature_score, currentaffairs=row.Current_affairs_score,
		currentuser=current_user.username
		)

@app.route('/edit_profile')
@login_required
def edit_profile():
	return render_template('edit_profile.html', bio=current_user.bio, dob=current_user.dob, currentuser=current_user.username)

@app.route('/submit_profile', methods=['POST'])
@login_required
def submit_profile():
	update(request)
	return redirect('/')

@app.route('/updatescore', methods=['GET', 'POST'])
@login_required
def updatescore():
	scoredata = request.get_json(force=True)
	scoreupdate(scoredata)
	return ""

@app.route('/quiz/<category>')
@login_required
def subcategory(category):
	row = User.query.filter_by(username=current_user.username).first()
	if category == "Sports":
		return render_template('sports.html', currentuser=current_user.username, cricket=row.cricket_score, football=row.football_score)
	elif category == "Movies":
		return render_template('movies.html', currentuser=current_user.username, bollywood=row.bollywood_score, hollywood=row.hollywood_score)
	elif category == "CurrentAffairs":
		return render_template('currentaffairs.html', currentuser=current_user.username, politics=row.politics_score, technology=row.technology_score)
	elif category == "History":
		return render_template('history.html', currentuser=current_user.username, indian=row.indian_score, foreign=row.foreign_score)
	elif category == "Science":
		return render_template('science.html', currentuser=current_user.username, physics=row.physics_score, chemistry=row.chemistry_score)
	elif category == "Literature":
		return render_template('literature.html', currentuser=current_user.username, hindi=row.hindi_score, english=row.english_score)
	else:
		redirect('/pui')

@app.route('/quiz/<category>/<subcategory>')
@login_required
def play(category, subcategory):
	listoftuples = generateplay(subcategory)
	dlist = [list(elem) for elem in listoftuples]
	return render_template('play.html', array=dlist, category=subcategory, maincategory=category, currentuser=current_user.username)	

@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		os.rename('./static/img/'+ str(filename),
				  './static/img/' + str(current_user.id) + ".jpg")
		return redirect('/')
	else: 
		return 'please select a file'

@app.errorhandler(404)
def custom404(error):
	return render_template('custom404.html')

if __name__ == '__main__':
	if User.query.filter_by(username="Admin").first(): 
		pass
	else:
		db.session.add(
			User(username="Admin", password="$2b$12$fjywq4d3jXU0y3JI3Z8RHuqaKEaRutaPrfwQE25cja1h3AE6qGbda",
				email='admin@gkuiz.com', role=True, active=True)
			)
		db.session.commit()
	app.run(debug=True)
