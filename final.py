import csv
import json
import sqlite3 as sqlite
import plotly as py
import get_data
import create_final_db
import plotly.graph_objs as go

# plot a pie chart of distribution of the user's privacy
def plot_players_privacy():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    values = []

    statement = 'SELECT Count(Id) FROM Players'
    statement += ' WHERE Length(TimeCreated) > 0 AND Length(Country) > 0'
    cur.execute(statement)
    result = cur.fetchall()
    values.append(result[0][0])

    statement = 'SELECT Count(Id) FROM Players'
    statement += ' WHERE Length(TimeCreated) > 0 AND Length(Country) = 0'
    cur.execute(statement)
    result = cur.fetchall()
    values.append(result[0][0])

    statement = 'SELECT Count(Id) FROM Players'
    statement += ' WHERE Length(Country) > 0 AND Length(TimeCreated) = 0'
    cur.execute(statement)
    result = cur.fetchall()
    values.append(result[0][0])

    statement = 'SELECT Count(Id) FROM Players'
    statement += ' WHERE Length(Country) = 0 AND Length(TimeCreated) = 0'
    cur.execute(statement)
    result = cur.fetchall()
    values.append(result[0][0])

    conn.close()

    labels = ['Public', 'Only have time create','Only Have time created and country','Private']
    trace = go.Pie(labels=labels, values=values)
    # py.iplot([trace], filename='plot_players_privacy')
    div = py.offline.plot([trace], show_link=False, output_type="div", include_plotlyjs=True)
    py.offline.plot([trace], filename='plot_players_privacy.html', auto_open=True)
    return div


# plot a bar chart of distribution of when the users are created
def plot_players_time():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    values = []

    for year in range(2002, 2018):
        statement = 'SELECT Count(Id) FROM Players'
        statement += ' WHERE TimeCreated LIKE "%'+str(year)+'"'
        cur.execute(statement)
        result = cur.fetchall()
        values.append(result[0][0])

    conn.close()

    labels = list(range(2002, 2018))
    trace = go.Bar(x=labels, y=values)
    # py.iplot([trace], filename='plot_players_time')
    div = py.offline.plot([trace], show_link=False, output_type="div", include_plotlyjs=True)
    py.offline.plot([trace], filename='plot_players_time.html', auto_open=True)
    return div

# plot a bar chart of distribution of what countries the users are in
def plot_players_country():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    labels = []
    values = []

    statement = 'SELECT country, Count(Id) FROM Players'
    statement += '\nGROUP BY Country'
    statement += '\nORDER BY Count(Id) ASC'
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        if (row[0]):
            labels.append(row[0])
        else:
            labels.append("unknown")
        values.append(row[1])

    conn.close()

    
    trace = go.Bar(x=labels, y=values)
    # py.iplot([trace], filename='plot_players_country')
    div = py.offline.plot([trace], show_link=False, output_type="div", include_plotlyjs=True)
    py.offline.plot([trace], filename='plot_players_country.html', auto_open=True)
    return div

# Select a user. 
# Plot a chart according to the user's input of a player id
# params: the id in the Players Table
def plot_friends(PlayerId):
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    statement = 'SELECT SteamId FROM Players'
    statement += ' WHERE Id = ' + str(PlayerId)
    cur.execute(statement)
    result = cur.fetchall()
    SteamId = result[0][0]
    conn.close()
    # get_data.add_friend_list(SteamId)
    # create_final_db.create_final_db()
    # create_final_db.populate_final_db()

    conn = sqlite.connect('yanxia_507_final.sqlite')
    cur = conn.cursor()

    labels = []
    values = []
    val_lab ={}

    statement = 'SELECT friend1.Country,COUNT(friend1.Id) FROM Friends AS F'
    statement += '\nINNER JOIN Players AS friend1'
    statement += '\n    ON friend1.Id = F.steamfriend1'
    statement += '\nINNER JOIN Players AS friend2'
    statement += '\n    ON friend2.Id = F.steamfriend2'
    statement += '\nWHERE F.steamfriend2=' + str(PlayerId)
    statement += '\nGROUP BY friend1.Country'
    statement += '\nORDER BY Count(friend1.Id) ASC'
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        if (row[0]):
            val_lab[row[0]] = row[1]
        else:
            val_lab["unknown"] = row[1]

    statement = 'SELECT friend2.Country,COUNT(friend2.Id) FROM Friends AS F'
    statement += '\nINNER JOIN Players AS friend1'
    statement += '\n    ON friend1.Id = F.steamfriend1'
    statement += '\nINNER JOIN Players AS friend2'
    statement += '\n    ON friend2.Id = F.steamfriend2'
    statement += '\nWHERE F.steamfriend1=' + str(PlayerId)
    statement += '\nGROUP BY friend2.Country'
    statement += '\nORDER BY Count(friend2.Id) ASC'
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        if (row[0]):
            if (row[0] in val_lab):
                val_lab[row[0]] += row[1]
            else:
                val_lab[row[0]] = row[1]
        else:
            if ("unknown" in val_lab):
                val_lab["unknown"] += row[1]
            else:
                val_lab["unknown"] = row[1]

    conn.close()

    for key in val_lab:
        labels.append(key)
        values.append(val_lab[key])

    trace = go.Bar(x=labels, y=values)
    # py.iplot([trace], filename='plot_players_time')
    div = py.offline.plot([trace], show_link=False, output_type="div", include_plotlyjs=True)
    py.offline.plot([trace], filename='plot_friends.html', auto_open=True)
    return div


# return the number of players in the database
def get_number():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return
    statement = 'SELECT Count(Id) FROM Players'
    cur.execute(statement)
    result = cur.fetchall()
    num = result[0][0]
    conn.close()
    # print("The number of total players in the database is "+str(num))
    return num

def get_game_number():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return
    statement = 'SELECT Count(Id) FROM Games'
    cur.execute(statement)
    result = cur.fetchall()
    num = result[0][0]
    conn.close()
    # print("The number of total players in the database is "+str(num))
    return num



def load_help_text():
    with open('help.txt') as f:
        return f.read()


def process_command(response):
    command = response.split(" ")
    if (command[0] == "player"):
        if (command[1] == "privacy"):
            plot_players_privacy()
            return True
        elif (command[1] == "timecreated"):
            plot_players_time()
            return True
        elif (command[1] == "country"):
            plot_players_country()
            return True
        else:
            return False
    elif (command[0] == "friend"):
        try:
            plot_friends(int(command[1]))
            return True
        except:
            return False
    elif (response == "number"):
        num = get_number()
        print("The number of total players in the database is "+str(num))
        return True
    else:
        return False

def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        results = process_command(response)
        if (results):
            pass
        elif (not response):
            print()
        elif (response == 'exit'):
            print("bye")
        else:
            print ("Command not recognized: " + response)
        if response == 'help':
            print(help_text)
            continue   

if __name__=="__main__":
    interactive_prompt()