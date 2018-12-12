from flask import Flask, render_template, request, redirect
import final
import sqlite3 as sqlite

app = Flask(__name__)

@app.route("/")
def index():
    pnum = final.get_number()
    gnum = final.get_game_number()
    return render_template("index.html", pnum=pnum, gnum = gnum)

@app.route("/postuser", methods=["POST"])
def postuser():
    pid = request.form["pid"]
    return redirect("/user/"+str(pid))

@app.route("/postgame", methods=["POST"])
def postgame():
    gid = request.form["gid"]
    return redirect("/game/"+str(gid))

@app.route('/user/<id>')
def get_users(id):
    ## get game list and play time of the user
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    statement = 'SELECT Name FROM Players'
    statement += ' WHERE Id = ' + str(id)
    cur.execute(statement)
    result = cur.fetchall()
    name = result[0][0]

    games=[]
    statement = 'SELECT g.Name, g.Id, g.AppId, GP.playtime_forever FROM Game_Player AS GP'
    statement += '\nINNER JOIN Games AS g'
    statement += '\n    ON g.Id = GP.AppId'
    statement += '\nWHERE GP.OwnerId = ' + str(id)
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        games.append({'name':row[0],'id':row[1],'appid':row[2],'time':row[3]})

    conn.close()

    return render_template("user.html", name=name, games=games)

@app.route('/game/<id>')
def get_games(id):
    ## get user list and play time of the user
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    statement = 'SELECT Name, AppId FROM Games'
    statement += ' WHERE Id = ' + str(id)
    cur.execute(statement)
    result = cur.fetchall()
    name = result[0][0]
    appid = result[0][1]

    users=[]
    statement = 'SELECT p.Name, p.Id, p.SteamId, p.Url, GP.playtime_forever FROM Game_Player AS GP'
    statement += '\nINNER JOIN Players AS p'
    statement += '\n    ON p.Id = GP.OwnerId'
    statement += '\nWHERE GP.AppId = ' + str(id)
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        users.append({'name':row[0],'id':row[1],'steamid':row[2],'url':row[3],'time':row[4]})

    conn.close()

    return render_template("game.html", name=name, appid=appid, users=users)

if __name__=="__main__":
    app.run(debug=True)