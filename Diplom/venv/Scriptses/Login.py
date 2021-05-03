from Scriptses.DataBase import getUserByLogin
from Particle.header import header
from Particle.head import getHead
from flask import Flask, redirect, make_response, render_template, url_for
from Scriptses.Administate import administr
import json
import requests

def login(db, login, password, U_L):
    str_login = getHead("Вход")
    str_login += header(U_L)
    if U_L :
        str_login = administr(db, U_L)
        return str_login
    if login=="" and password=="" :
        str_login += """<div class="cb cb_gray"><h1>Вход в систему</h1>
			<form action="/login" method="POST" class="fm">
                <input type="text" class="cbi" name="userLogin"/></br>
                <input type="password" class="cbi" name="userPassw"/></br>
                <p></p>
				<table width="100%"><tr>
					<td width="50%"><input type="reset" class="b_hed" value="Очистить поля"/></td>
					<td width="50%"><input type="submit" class="b_hed" value="Войти"/></td>
				</tr></table>
            </form></div>"""
    else :
        user = getUserByLogin(db, login)
        if user==[] :
            str_login += """<div class="cb cb_red"><h1>Вход в систему</h1>
			<form action="/login" method="POST" class="fm">
				<h2> Пользователя """+login+""" нет</h2></br>
                <input type="text" class="cbi" name="userLogin" value='"""+login+"""'/>
                <input type="password" class="cbi" name="userPassw" value='"""+password+"""'/>
				<table width="100%"><tr>
					<td width="50%"><input type="reset" class="b_hed" value="Очистить поля"/></td>
					<td width="50%"><input type="submit" class="b_hed" value="Войти"/></td>
				</tr></table>
                </form></div>"""
        else:
            if password != user[0]["Password"] :
                str_login += """<div class="cb cb_red"><h1>Вход в систему</h1>
				<form action="/login" method="POST" class="fm">
					<h2>Неверный пароль</h2>
                    <input type="text" class="cbi" name="userLogin" value='"""+login+"""'/>
                    <input type="password" class="cbi" name="userPassw" value='"""+password+"""'/>
                    <table width="100%"><tr>
						<td width="50%"><input type="reset" class="b_hed" value="Очистить поля"/></td>
						<td width="50%"><input type="submit" class="b_hed" value="Войти"/></td>
					</tr></table>
                </form>"""
            else:
                #api_url = 'http://127.0.0.1:5000/admin'
                #create_row_data = {'userLogin': login, 'userPassw': password, 'Admine_Login': 'ABC'}
                #r = requests.post(url=api_url, json=create_row_data)
                #return redirect(url_for('admin'))
                lg = login
                str = administr(db, lg)
                str_login = make_response(str)
                str_login.set_cookie('USER_LOGIN', lg, max_age=60 * 60 * 24 * 365 * 2)
                #str_login += """</h1><form action="/admin" method="POST">
                #            <input type="hidden" name="userLogin" value='""" + login + """'/></br>
                #            <input type="hidden" name="userPassw" value='""" + password + """'/></br>
                #            <input type="submit" value="Страница администратора" name="Admine_Login"/>
                #        </form>"""
    return str_login

def logout():
    str = getHead("Выход")
    str += header("")
    str += """</h1><form action="admin" method="POST">
        <input type="text" name="userLogin" /></br>
        <input type="text" name="userPassw" /></br>
        <input type="submit" value="Войти" name="Admine_Login"/>
    </form>"""
    res = make_response(str)
    res.set_cookie('USER_LOGIN', login, max_age=0)
    return res