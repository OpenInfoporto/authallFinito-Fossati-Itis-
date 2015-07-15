from flask import Flask, jsonify, g
from flask_restful import reqparse, abort, Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
import time
import datetime
import sqlite3
import datetime as dt
from dateutil.relativedelta import relativedelta
import datetime
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPBasicAuth()
api = Api(app)

today = None




# controlli 

def abort_if_user_doesnt_exist(idUtente):
    utente = query_db('SELECT COUNT (*) FROM utenti WHERE idUtente = ?',[idUtente], True)
    print utente
    if utente[0] < 1:
        abort(404, message="user {} doesn't exist")

def abort_if_client_doesnt_exist(idCliente):
    cliente = query_db('SELECT COUNT (*) FROM clienti WHERE idCliente = ?',[idCliente], True)
    print cliente
    if cliente[0] < 1:
        abort(404, message="client {} doesn't exist")

def abort_if_comm_doesnt_exist(idCom):
    commesse = query_db('SELECT COUNT (*) FROM commesse WHERE idCom = ?',[idCom], True)
    print commesse
    if commesse[0] < 1:
        abort(404, message="order {} doesn't exist")

def abort_if_rend_doesnt_exist(idRend):
    rendicontazioni = query_db('SELECT COUNT (*) FROM rendicontazioni WHERE idRend = ?',[idRend], True)
    print rendicontazioni
    if rendicontazioni[0] < 1:
        abort(404, message="reporting {} doesn't exist")

def abort_if_segn_doesnt_exist(idSegn):
    segnalazioni = query_db('SELECT COUNT (*) FROM segnalazioni WHERE idSegn = ?',[idSegn], True)
    print segnalazioni
    if segnalazioni[0] < 1:
        abort(404, message="signal {} doesn't exist")




#database 

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('pass', type=str)
parser.add_argument('rag', type=str)
parser.add_argument('cod', type=str)
parser.add_argument('num', type=str)
parser.add_argument('codice', type=str)
parser.add_argument('idC', type=str)
parser.add_argument('idS', type=str)
parser.add_argument('no', type=str)
parser.add_argument('idU', type=str)
parser.add_argument('tit', type=str)
parser.add_argument('nome', type=str)
parser.add_argument('cogn', type=str)
parser.add_argument('em', type=str)
parser.add_argument('descr', type=str)
parser.add_argument('pri', type=str)
parser.add_argument('st', type=str) 
parser.add_argument('day', type=str)
parser.add_argument('month', type=str) 
parser.add_argument('year', type=str) 
parser.add_argument('timestamp', type=str) 

DATABASE = 'databaseTest.db'

def connect_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
        cur = get_db().cursor()
        cur.execute(query, args)
        get_db().commit()
        if cur.lastrowid is not None:
            return cur.lastrowid
        return 'ok'

@auth.get_password
def get_pw(username):
    user = query_db('SELECT password FROM utenti WHERE user=?',[username], True)
    return user['password'] if user else None










#inserimento utenti


class UsersList(Resource):
    @auth.login_required
    def get(self):
        utenti = list()

        for user in query_db('SELECT * FROM utenti'):
            #todo
            utenti.append({ "idUtente" : user["idUtente"],
            "user" : user["user"], 
            "password" : user["password"], 
            "nome" : user["nome"],
            "cognome" : user["cognome"],
            "email" : user["email"]
            })

        return jsonify(users = utenti)

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        username = args['user']
        password = args['pass']
        nome = args['nome']
        cognome = args['cogn']
        email = args['em']


        idUser = execute_db('INSERT INTO utenti (user, password, nome, cognome, email) VALUES (?, ?, ?, ?, ?)', [username, password, nome, cognome, email])
        return idUser, 201














#selezione da utenti


class User(Resource):
    def get(self, idUtente):
        abort_if_user_doesnt_exist(idUtente)
        utente = query_db('SELECT * FROM utenti WHERE idUtente = ?',[idUtente], True)
        #return utente['user'], 201
        return jsonify( idUtente = utente["idUtente"],
                       user = utente["user"],
                       password = utente["password"],
                       nome = utente["nome"],
                       cognome = utente["cognome"],
                       email = utente["email"])

    def put(self, idUtente):
        abort_if_user_doesnt_exist(idUtente)
        args = parser.parse_args()
        username = args['user']
        password = args['pass']
        nome = args['nome']
        cognome = args['cogn']
        email = args['em']

        return execute_db("UPDATE utenti SET user=?, password=?, nome=?, cognome=?, email=? WHERE idUtente=?", [username, password, nome, cognome, email, idUtente]),202

    def delete(self, idUtente):
        abort_if_user_doesnt_exist(idUtente)

        return execute_db("DELETE FROM utenti WHERE idUtente = ?",[idUtente]),204
















#inserimento clienti 

class ClientsList(Resource):
    @auth.login_required
    def get(self):
        clienti = list()

        for client in query_db('SELECT * FROM clienti'):
            #todo
            clienti.append({ "idCliente" : client["idCliente"],
            "ragione_sociale" : client["ragione_sociale"], 
            "cod_fiscale"  : client["cod_fiscale"], 
            "n_telefono" : client["n_telefono"],
            "email" : client["email"]
            })

        return jsonify(clienti = clienti)

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        rs = args['rag']
        cf = args['cod'] 
        nt = args['num']
        email = args['em']

        idCliente= execute_db('INSERT INTO clienti (ragione_sociale, cod_fiscale, n_telefono, email) VALUES (?, ?, ?, ?)', [rs, cf, nt, email])
        return idCliente, 201













#selezione da clienti

class Client(Resource):
    def get(self, idCliente):
        abort_if_client_doesnt_exist(idCliente)
        cliente = query_db('SELECT * FROM clienti WHERE idCliente = ?',[idCliente], True)
        #return cliente['user'], 201
        return jsonify( idCliente = cliente["idCliente"],
                        ragione_sociale = cliente["ragione_sociale"],
                        cod_fiscale  = cliente["cod_fiscale"], 
                        n_telefono = cliente["n_telefono"],
                        email = cliente["email"]
                       )

    def put(self, idCliente):
        abort_if_client_doesnt_exist(idCliente)
        args = parser.parse_args()
        rs = args['rag']
        cf = args['cod']
        nt = args['num']
        email = args['em']

        return execute_db("UPDATE clienti SET ragione_sociale=?, cod_fiscale=?, n_telefono=?, email=? WHERE idCliente=?",[rs,cf,nt,email,idCliente]),202

    def delete(self, idCliente):
        abort_if_client_doesnt_exist(idCliente)
        return execute_db("DELETE FROM clienti WHERE idCliente = ?",[idCliente]),204











#inserisce commissioni

class ComList(Resource):

    @auth.login_required
    def get(self):
        commesse = list()
        for comm in query_db('SELECT * FROM commesse'):
            #todo
            commesse.append({ "idCom" : comm["idCom"], 
            "codice"  : comm["codice"], 
            "idCliente" : comm["idCliente"],
            "titolo"  : comm["titolo"], 
            "descrizione" : comm["descrizione"]
            })

        return jsonify(commesse = commesse)

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        cod = args['codice']
        idCliente = args['idC']
        titolo = args ['tit']
        descr = args['descr']

        idCom= execute_db('INSERT INTO commesse (codice, idCliente, titolo, descrizione) VALUES (?, ?, ?, ?)', [cod,idCliente,titolo,descr])
        return idCom, 201












#seleziona commissioni

class Com(Resource):

    def get(self, idCom):
        abort_if_comm_doesnt_exist(idCom)
        commesse = query_db('SELECT * FROM commesse WHERE idCom = ?',[idCom], True)
        #return cliente['user'], 201
        return jsonify( idCom = commesse["idCom"],
                       codice = commesse["codice"],
                       idCliente = commesse["idCliente"],
                       titolo = commesse["titolo"],
                       descrizione = commesse["descrizione"])


    def put(self, idCom):
        abort_if_comm_doesnt_exist(idCom)
        args = parser.parse_args()
        codice = args['codice']
        idCliente = args['idC']        
        titolo = args ['tit']
        descrizione = args['descr']

        return execute_db("UPDATE commesse SET codice = ?, idCliente = ?, titolo = ?, descrizione = ? WHERE idCom=?",[codice,idCliente,titolo,descrizione,idCom]),202


    def delete(self, idCom):
        abort_if_comm_doesnt_exist(idCom)
        return execute_db("DELETE FROM commesse WHERE idCom = ?",[idCom]),204














#inserisce rendicontazioni

class RendList(Resource):

    @auth.login_required
    def get(self):
        rendicontazioni = list()

        for rendicontazione in query_db('SELECT * FROM rendicontazioni'):
            #todo
            rendicontazioni.append({ "idRend" : rendicontazione["idRend"],
            "idSegn" : rendicontazione["idSegn"], 
            "n_ore"  : rendicontazione["n_ore"], 
            "idUtente" : rendicontazione["idUtente"],
            "timestamp" : rendicontazione["timestamp"]
            })

        return jsonify(rendicontazioni = rendicontazioni)

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        idSegn = args['idS']
        n_ore = args['no'] 
        idUtente = args['idU']
        timestamp = args['timestamp']

        idRend= execute_db('INSERT INTO rendicontazioni (idSegn, n_ore, timestamp, idUtente) VALUES (?, ?, ?, ?)', [idSegn, n_ore, time, idUtente])
        return idRend, 201











#modifica rendicontazioni

class Rend(Resource):
    def get(self, idRend):
        abort_if_rend_doesnt_exist(idRend)
        rendicontazione = query_db('SELECT * FROM rendicontazioni WHERE idRend = ?',[idRend], True)
        #return rendicontazione['user'], 201
        return jsonify( idRend = rendicontazione["idRend"],
                        idSegn = rendicontazione["idSegn"],
                        n_ore = rendicontazione["n_ore"],
                        idUtente = rendicontazione["idUtente"],
                        timestamp = rendicontazione["timestamp"])

    def put(self, idRend):
        abort_if_rend_doesnt_exist(idRend)
        args = parser.parse_args()
        idSegn = args['idS']
        n_ore = args['no'] 
        idUtente = args['idU']
        timestamp = args['timestamp']

        return execute_db("UPDATE rendicontazioni SET idSegn=?, n_ore=?, timestamp=?, idUtente=? WHERE idRend=?",[idSegn,n_ore,timestamp,idUtente,idRend]),202

    def delete(self, idRend):
        abort_if_rend_doesnt_exist(idRend)
        return execute_db("DELETE FROM rendicontazioni WHERE idRend = ?",[idRend]),204













#inserisce segnalazioni

class SegnList(Resource):

    @auth.login_required
    def get(self):
        segnalazioni = list()

        for segnalazione in query_db('SELECT * FROM segnalazioni'):
            #todo
            segnalazioni.append({ "idSegn" : segnalazione["idSegn"], 
            "titolo"  : segnalazione["titolo"], 
            "idCom" : segnalazione["idCom"],
            "descrizione" : segnalazione["descrizione"],
            "priorita" : segnalazione["priorita"],
            "stato" : segnalazione["stato"],
            "idUtente" : segnalazione["idUtente"]
            })

        return jsonify(segnalazioni = segnalazioni)

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        tito = args['tit'] 
        idCo = args['idC']
        descr = args['descr']
        priorita = args['pri']
        stato = args['st']
        idUtente = args['idU']

        idSegn= execute_db('INSERT INTO segnalazioni (titolo, idCom, descrizione, priorita, stato, idUtente) VALUES (?, ?, ?, ?, ?, ?)', [tito, idCo, descr, priorita, stato, idUtente])
        return idSegn, 201

















#modifica segnalazioni

class Segn(Resource):
    def get(self, idSegn):
        abort_if_segn_doesnt_exist(idSegn)
        segnalazione = query_db('SELECT * FROM segnalazioni WHERE idSegn = ?',[idSegn], True)
        #return cliente['user'], 201
        return jsonify( idSegn = segnalazione["idSegn"],
                       titolo = segnalazione["titolo"],
                       idCom = segnalazione["idCom"],
                       descrizione = segnalazione["descrizione"],
                       priorita = segnalazione["priorita"],
                       stato = segnalazione["stato"],
                       idUtente = segnalazione["idUtente"])

    def put(self, idSegn):
        abort_if_segn_doesnt_exist(idSegn)
        args = parser.parse_args()
        tito = args['tit'] 
        idCo = args['idC']
        descr = args['descr']
        priorita = args['pri']
        stato = args['st']
        idUtente = args['idU']

        return execute_db("UPDATE segnalazioni SET titolo=?, idCom=?, descrizione=?, priorita=?, stato=?, idUtente=? WHERE idSegn=?",[tito,idCo,descr,priorita,stato,idUtente,idSegn]),202

    def delete(self, idSegn):
        abort_if_segn_doesnt_exist(idSegn)
        return execute_db("DELETE FROM segnalazioni WHERE idSegn = ?",[idSegn]),204












#ritorna dati utente delle segnalazioni

class SegnUtente(Resource):
    def get(self,idUtente):
        abort_if_user_doesnt_exist(idUtente)
        segnutente = query_db('SELECT * FROM segnalazioni LEFT JOIN utenti WHERE utenti.idUtente = ?', [idUtente], True)
        #import pdb; pdb.set_trace() IN CASO DI ERRORI! 
        return jsonify( idSegn = segnutente["idSegn"],
                        titolo = segnutente["titolo"],
                        idCom = segnutente["idCom"],
                        descrizione = segnutente["descrizione"],
                        priorita = segnutente["priorita"],
                        stato = segnutente["stato"],
                        idUtente = segnutente["idUtente"],
                        user = segnutente["user"],
                        password = segnutente["password"],
                        nome = segnutente["nome"],
                        cognome = segnutente["cognome"],
                        email = segnutente["email"])















#ritorna segnalazione dell'utente

class MyTickets(Resource):

    @auth.login_required
    def get(self):

        segnalazioni = list()

        for segnalazione in query_db('SELECT * FROM segnalazioni NATURAL JOIN utenti WHERE user = ?', [auth.username()]):
            segnalazioni.append({ "idSegn" : segnalazione["idSegn"], 
            "titolo"  : segnalazione["titolo"], 
            "idCom" : segnalazione["idCom"],
            "descrizione" : segnalazione["descrizione"],
            "priorita" : segnalazione["priorita"],
            "stato" : segnalazione["stato"],
            "idUtente" : segnalazione["idUtente"]
            })

        return jsonify(segnalazioni = segnalazioni)












#ritorna le commesse dell' utente

class MyComm(Resource):

    @auth.login_required
    def get(self):

        commesse = list()

        for comm in query_db('SELECT * FROM utenti JOIN segnalazioni ON utenti.idUtente = segnalazioni.idUtente JOIN commesse ON segnalazioni.idCom = commesse.idCom WHERE user = ?', [auth.username()]):
            commesse.append({"idUtente" : comm["idUtente"],
            "idCom" : comm["idCom"], 
            "codice"  : comm["codice"], 
            "idCliente" : comm["idCliente"],
            "titolo"  : comm["titolo"], 
            "descrizione" : comm["descrizione"]
            })

        return jsonify(commesse = commesse)

#conteggio ore (da finire)

class MyHour(Resource):

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        day = args['day']
        month = args['month']
        year = args['year']
        stringtime = year+'-'+month+'-'+day
        today = datetime.datetime.strptime(stringtime, '%Y-%m-%d')
        ore = list()
        #timestamp = int(time.time())
        daystart = today.replace(hour=00, minute=00, second=0)
        timestart = int(time.mktime(daystart.timetuple()))
        daystop = today.replace(hour=23, minute=59, second=59)
        timestop = int(time.mktime(daystop.timetuple()))
    	rv = query_db('SELECT SUM(n_ore) FROM rendicontazioni NATURAL JOIN utenti WHERE user = ? AND timestamp BETWEEN ? AND ?', [auth.username(), timestart, timestop], True)
    	print rv

    	sommaOre = rv[0]

    	if sommaOre is None:
            sommaOre = 0

        return jsonify(ore = {
            'oreGiornaliere': sommaOre
        })

class MyWeekHour (Resource) :
        
    @auth.login_required
    def post(self):
        #today = dt.date.today()
        args = parser.parse_args()
        day = args['day']
        month = args['month']
        year = args['year']
        stringtime = year+'-'+month+'-'+day
        today = datetime.datetime.strptime(stringtime, '%Y-%m-%d')
        print today
        start = today-timedelta(days = (today.weekday()))
        print today.weekday()
        print start
        timestart = int(time.mktime(start.timetuple()))
        weekFinish = start + relativedelta(days=6)
        print weekFinish
        timestop = int(time.mktime(weekFinish.timetuple()))
        rv = query_db('SELECT SUM(n_ore) FROM rendicontazioni NATURAL JOIN utenti WHERE user = ? AND timestamp BETWEEN ? AND ?', [auth.username(), timestart, timestop ], True)
        sommaOre = rv[0]
        if sommaOre is None:
            sommaOre = 0
        return jsonify(ore = {
        'oreSettimanali': sommaOre
        })


class mese(Resource):

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        day = args['day']
        month = args['month']
        year = args['year']
        stringtime = year+'-'+month+'-'+day
        today = datetime.datetime.strptime(stringtime, '%Y-%m-%d')
        #today = dt.date.today()
        month=today.month
        if ((month==1)|(month==4)|(month==6)|(month==9)|(month==11)):
            daysmonth=29
        elif ((month==1)|(month==3)|(month==5)|(month==7)|(month==8)|(month==10)|(month==12)):
            daysmonth=30
        elif (month==2):
            daysmonth=27
        first_day_this_month = dt.date(day=1, month=today.month, year=today.year)
        print first_day_this_month
        timestart = int(time.mktime(first_day_this_month.timetuple()))
        last_day_last_month = (first_day_this_month + timedelta(daysmonth))
        print last_day_last_month
        timestop = int(time.mktime(last_day_last_month.timetuple()))
        rv = query_db('SELECT SUM(n_ore) FROM rendicontazioni NATURAL JOIN utenti WHERE user = ? AND timestamp BETWEEN ? AND ?', [auth.username(), timestart, timestop], True)

        sommaOre = rv[0]

        if sommaOre is None: sommaOre = 0

        return jsonify(ore = {
            'oremensili': sommaOre
        })        

                        
                            






## Actually setup the Api resource routing here
api.add_resource(UsersList, '/utenti')
api.add_resource(ClientsList, '/clienti')
api.add_resource(User, '/utenti/<idUtente>')
api.add_resource(Client, '/clienti/<idCliente>')
api.add_resource(ComList, '/commesse')
api.add_resource(Com, '/commesse/<idCom>')
api.add_resource(RendList, '/rend')
api.add_resource(Rend, '/rend/<idRend>')
api.add_resource(SegnList, '/segn')
api.add_resource(Segn, '/segn/<idSegn>')
api.add_resource(SegnUtente, '/segn/utente/<idUtente>')
api.add_resource(MyTickets, '/miesegnalazioni')
api.add_resource(MyComm, '/miecommesse')
api.add_resource(MyHour, '/mieore') 
api.add_resource(MyWeekHour, '/mieoresettimana')
api.add_resource(mese, '/mieoremese')   

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
