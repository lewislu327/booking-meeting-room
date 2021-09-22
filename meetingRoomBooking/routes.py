from flask import render_template, url_for, flash, redirect, request, abort
from meetingRoomBooking import app, db, bcrypt
from meetingRoomBooking.forms import RegistrationForm, LoginForm, PostForm
from meetingRoomBooking.models import User, Room
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date

@app.route("/")
@app.route("/home")
@login_required
def home():
    today = date.today()
    rooms = Room.query.filter(Room.date == today).order_by(
        Room.start_at.asc()).all()
    searchDate = request.args.get('date')
    if searchDate:
        rooms = Room.query.filter(Room.date == searchDate).all()
        return render_template('home.html', rooms=rooms, date=searchDate)
    return render_template('home.html', rooms=rooms, date=today)

@app.route('/total')
@login_required
def total():
    rooms = Room.query.order_by(Room.date.desc()).all()
    return render_template('home.html', rooms=rooms)

@app.route("/users")
@login_required
def admin_users():
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('您的帳戶已成功建立！', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('登入失敗，請再重新嘗試', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = PostForm()
    if form.validate_on_submit():
        booked = Room.query.filter_by(
            start_at=form.start_at.data, 
            end_at=form.end_at.data, 
            roomName=form.roomName.data,
            date=form.date.data).first()
        if booked:
            flash('此時段或會議室已被預約，請調整時段或會議室', 'danger')
            return redirect(url_for('new'))
        
        if form.start_at.data == form.end_at.data:
            flash("會議開始時間與結束時間不能相同", 'danger') 
            return redirect(url_for('new'))

        room = Room(date=form.date.data, roomName=form.roomName.data,
                    start_at=form.start_at.data, end_at=form.end_at.data, roomUser=current_user)
        db.session.add(room)
        db.session.commit()
        flash('已成功預約會議室！', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', form=form, legend='Booking meeting room', submit='Create')

@app.route('/edit/<int:room_id>', methods=['GET','POST'])
@login_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if room.roomUser != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        room.date = form.date.data
        room.roomName = form.roomName.data
        room.start_at = form.start_at.data
        room.end_at = form.end_at.data
        db.session.commit()
        flash('預約資訊已成功更新', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.date.data = room.date
        form.roomName.data = room.roomName
        form.start_at.data = room.start_at
        form.end_at.data = room.end_at
    return render_template('create.html', form=form, legend='Update booking time and room', submit='Update')


@app.route('/delete/<int:room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if room.roomUser != current_user:
        abort(403)
    db.session.delete(room)
    db.session.commit()
    flash('預約時段已成功刪除', 'success')
    return redirect(url_for('home'))
