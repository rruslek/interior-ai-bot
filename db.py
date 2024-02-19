import sqlite3
import re
import datetime
def bd():
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS SDAKeys(key TEXT, tries INTEGER DEFAULT 0 NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS Users(user_id INTEGER NOT NULL PRIMARY KEY, '
				'credit INTEGER DEFAULT 3 NOT NULL,'
				'date_join TIMESTAMP,'
				'date_last TIMESTAMP)')


async def key_writer(link):
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	mass = []
	mass.append(link)
	cur.execute('INSERT INTO SDAKeys VALUES(?)', mass)
	con.commit()
	cur.close()


async def get_sdkey():
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute('SELECT key FROM SDAKeys where tries < 10')
	data = cur.fetchall()
	key = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	print(key)
	cur.close()
	return key


async def key_add_tries(key):
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute(f'UPDATE SDAKeys SET tries = tries + 1 where key=\'{key}\'')
	con.commit()
	cur.close()


async def add_user(id):
	date = datetime.datetime.now()
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?);", (id, 3, date, date))
	con.commit()
	cur.close()

async def set_lastdate(id):
	date = datetime.datetime.now()
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute(f'UPDATE Users SET date_last = (?) WHERE user_id = (?)', (date, id))
	con.commit()
	cur.close()


async def get_balance(id):
	con = sqlite3.connect("interiorAI.db")
	print(id)
	cur = con.cursor()
	cur.execute(f'SELECT credit FROM Users WHERE user_id = {id}')
	data = cur.fetchall()
	balance = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	print(balance)
	cur.close()
	return balance


async def change_balance(sum, id):
	con = sqlite3.connect("interiorAI.db")
	cur = con.cursor()
	cur.execute(f'UPDATE Users SET credit = credit {sum} WHERE user_id = \'{id}\'')
	con.commit()
	cur.close()


async def get_lastdate(id):
	con = sqlite3.connect("interiorAI.db")
	print(id)
	cur = con.cursor()
	cur.execute(f'SELECT date_last FROM Users WHERE user_id = {id}')
	data = cur.fetchall()
	last_date = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	print(last_date)
	cur.close()
	return last_date