import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from FM import app, db, bcrypt
from FM.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddManagerForm, AddPlayerForm, AddStadiumForm, UpdatePlayerForm, UpdateManagerForm
from FM.models import Club, Manager, Player, Stadium
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        club=Club.query.filter_by(id=current_user.id).first_or_404()
        page=request.args.get('page',1, type=int)
        players=Player.query.filter_by(plays_for=club)\
                    .paginate(page=page,per_page=7)
        return render_template('home.html',club=club,players=players)
    else:
        page=request.args.get('page',1, type=int)
        details=Club.query.paginate(page=page,per_page=7 )
        return render_template('home.html',details=details)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        club = Club(clubn=form.club.data, password=hashed_password)
        db.session.add(club)
        db.session.commit()
        flash('The club has been succesfully added!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            club= Club.query.filter_by(clubn=form.club.data).first()
            if club and bcrypt.check_password_hash(club.password, form.password.data):
                login_user(club, remember=form.remember.data)
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Club name and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
        random_hex=secrets.token_hex(8)
        _, f_ext= os.path.splitext(form_picture.filename)
        picture_fn = random_hex+ f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)

        output_size=(125,125)
        i=Image.open(form_picture)
        i.thumbnail=(output_size)

        i.save(picture_path)

        return picture_fn

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.clubn=form.club.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.club.data=current_user.clubn
    image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/manager/add",methods=['GET', 'POST'])
@login_required
def manager_add():
    form=AddManagerForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
        manager= Manager(name=form.name.data, desc=form.desc.data,image_file=picture_file, manages=current_user)
        db.session.add(manager)
        db.session.commit()
        flash('The manager has been added', 'success')
        return redirect(url_for('home'))
    return render_template('manager.html', title='Manager',form=form,legend="Manager")


@app.route("/<int:club_id>/managers")
def club_manager(club_id):
    page=request.args.get('page',1, type=int)
    club=Club.query.filter_by(id=club_id).first_or_404()
    manager=Manager.query.filter_by(manages=club)\
                .paginate(page=page,per_page=5)
    return render_template('club_manager.html',club=club,manager=manager)

@app.route("/manager/<int:manager_id>/delete",methods=['POST'])
@login_required
def delete_manager(manager_id):
    manager =Manager.query.get_or_404(manager_id)
    if manager.manages != current_user:
        abort(403)
    db.session.delete(manager)
    db.session.commit()
    flash('The manager has been removed!','success')
    return redirect(url_for('home'))


@app.route("/player/add",methods=['GET','POST'])
@login_required
def player_add():
    form=AddPlayerForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
        player=Player(name=form.name.data, age=form.age.data,image_file=picture_file, country=form.country.data, position=form.position.data, plays_for=current_user)
        db.session.add(player)
        db.session.commit()
        flash('The player has been added', 'success')
        return redirect(url_for('home'))
    return render_template('player.html', title='Player',form=form,legend="Player")


@app.route("/player/<int:player_id>/delete",methods=['POST'])
@login_required
def remove_player(player_id):
    player =Player.query.get_or_404(player_id)
    if player.plays_for != current_user:
        abort(403)
    db.session.delete(player)
    db.session.commit()
    flash('The player has been removed!','success')
    return redirect(url_for('home'))


@app.route("/stadium/add",methods=['GET','POST'])
@login_required
def add_stadium():
    form=AddStadiumForm()
    if form.validate_on_submit():
        stadium=Stadium(name=form.name.data, city=form.city.data, belongs_to=current_user)
        db.session.add(stadium)
        db.session.commit()
        flash('The stadium has been added', 'success')
        return redirect(url_for('home'))
    return render_template('stadium.html', title='stadium',form=form,legend="Stadium")

@app.route("/<int:club_id>/Stadium")
def stadium(club_id):
    page=request.args.get('page',1, type=int)
    club=Club.query.filter_by(id=club_id).first_or_404()
    stadium=Stadium.query.filter_by(belongs_to=club)\
                .paginate(page=page,per_page=10)
    return render_template('std.html',club=club,stadium=stadium)

@app.route("/update_player",methods=['GET','POST'])
@login_required
def update_player():
    form=UpdatePlayerForm()
    if form.validate_on_submit():
        player =Player.query.filter_by(name=form.name.data).first()
        if player is None:
            flash('Player does not exist', 'danger')
            return redirect(url_for('update_player'))
        player.age=form.age.data
        player.country=form.country.data
        player.position=form.position.data
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            player.image_file=picture_file
        db.session.commit()
        flash('Player details has been updated!', 'success')
        return redirect(url_for('update_player'))
    return render_template('playerupdt.html', title='P_Update',form=form)

@app.route("/update_manager",methods=['GET','POST'])
@login_required
def update_manager():
    form=UpdateManagerForm()
    if form.validate_on_submit():
        manager =Manager.query.filter_by(name=form.name.data).first()
        if manager is None:
            flash('Manager does not exist', 'danger')
            return redirect(url_for('update_manager'))
        manager.desc=form.desc.data
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            manager.image_file=picture_file
        db.session.commit()
        flash('Manager details has been updated!', 'success')
        return redirect(url_for('update_manager'))
    return render_template('manupdt.html', title='M_Update',form=form)
