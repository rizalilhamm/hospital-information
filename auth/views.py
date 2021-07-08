from flask import Blueprint, request, redirect, url_for, flash, render_template

auth_dp = Blueprint('auth', __name__,
    template_folder='templates', static_folder='static')

from app import db, bcrypt
from models import User

def register(admin):
    if request.method == 'POST':
        firstname = request.form['username']
        lastname = request.form['lastname']
        age = request.form['age']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        arguments = all([firstname.strip(), lastname.strip(), age.strip(), email.strip(), username.strip(), password.strip()])
        if not arguments:
            flash('Semua parameters wajib diisi!')
            return redirect(url_for('auth.admin_register'))
        if password != confirm_password:
            flash('Password harus sama!')
            return redirect(url_for('auth.admin_register'))

        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar, silahkan, login')
            return redirect(url_for('auth.admin_login'))
        new_user = User(firstname=firstname, lastname=lastname, 
                        age=age, email=email, username=username, password=password)
        new_user.admin = admin
        db.session.add(new_user)
        db.session.commit()
        user_rule = 'User Biasa'
        if admin:
            user_rule = 'Admin'
        flash('Pendaftaran Berhasil sebagai {}'.format(user_rule))
        return redirect(url_for('auth.admin_register'))

@auth_dp.route('/admin/register', methods=['POST', 'GET'])
def admin_register():
    register(admin=True)
    return render_template('admin_register.html', title='Admin Register', user_type='ADMIN')

@auth_dp.route('/patient/register', methods=['POST', 'GET'])
def patient_register():
    register(admin=False)
    return render_template('patient_register.html')

@auth_dp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('Kamu berhasil login')
                return 'Ini halaman Home'
            flash('Password anda salah')
            return redirect(url_for('auth.login'))
        flash('Email tidak ditemukan')
        return redirect(url_for('auth.login'))

    return render_template('login.html')
