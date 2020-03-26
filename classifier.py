import psycopg2
import random
import config as conf

def showResults(conn):
	# create a cursor
	cur = conn.cursor()

	# execute a statement
	print('*'*10+'Show Results'+'*'*10)
	query = 'SELECT * FROM statistics'
	
	cur.execute(query)

	rows = cur.fetchall()

	for i in range(len(rows)):

		if rows[i][2] >= rows[i][3] and rows[i][2] >=rows[i][4]:
			print(f'{rows[i][0]}: {rows[i][1]} ->Positivo')
		elif rows[i][3] >= rows[i][2] and rows[i][3] >=rows[i][4]:
			print(f'{rows[i][0]}: {rows[i][1]} ->Neutral')
		else:
			print(f'{rows[i][0]}: {rows[i][1]} ->Negativo')

	cur.close()

def calcStatics(conn):
	# create a cursor
	cur = conn.cursor()

	# execute a statement
	print('*'*10+'Statistics'+'*'*10)
	query = 'SELECT id_comment, id_sentiment, count(*) FROM votes'
	query +=' GROUP BY id_comment, id_sentiment'
	query +=' ORDER BY id_comment'
	
	cur.execute(query)

	rows = cur.fetchall()

	for i in range(len(rows)):
		#r1 = random.randint(0, len(rows)) 
		print(f'{i} : {rows[i][0]}\t{rows[i][1]}\t{rows[i][2]}\n')

		queryU = 'UPDATE statistics SET '
		if rows[i][1] == 1:
			queryU += 'pos = '+str(rows[i][2])
		elif rows[i][1] == 2:
			queryU += 'neu = '+str(rows[i][2])
		else:
			queryU += 'neg = '+str(rows[i][2])
					
		queryU += ' WHERE id = '+str(rows[i][0])
		#print(queryU)

		cur.execute(queryU)

	conn.commit()

	cur.close()


def votes(conn):
# create a cursor
	cur = conn.cursor()

	# execute a statement
	print('*'*10+'Votes'+'*'*10)
	cur.execute('SELECT * FROM comments')

	# display the PostgreSQL database server version
	#db_version = cur.fetchone()
	#print(db_version)
	rows = cur.fetchall()


	for i in range(len(rows)):
		#r1 = random.randint(0, len(rows)) 
		print(f'\n{i+1} : {rows[i][1]}')
		while True:
			opc = input('Ingrese el número (1-Positivo, 2-Neutral, 3-Negativo) para el tweet arriba: ')

			if opc in ['1','2','3']:
				break
			else:
				print('Debe ingresar solo uno de los 3 números (1-Positivo, 2-Neutral, 3-Negativo)\n')

		query = 'INSERT INTO votes(id_comment, id_sentiment) VALUES ('+str(i+1)+','+opc+')'
		#print(query)

		cur.execute(query)

	conn.commit()

	cur.close()

def closeDB(conn):
	conn.close()
	print('Database connection closed.')

def connectDB():

	conn = None
	try:
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(host=conf.host,database=conf.database, user=conf.user, password=conf.password)

		
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	return conn

if __name__ == '__main__':
	print('Hello world!')
	conn = connectDB()

	if conn is not None:
		votes(conn)
		calcStatics(conn)
		showResults(conn)
		closeDB(conn)
	else:
		print('Connection failed!')