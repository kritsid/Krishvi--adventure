from database import get_db
from flask import Flask,redirect,url_for,render_template,request,g,session
import pandas as pd

app=Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()

# def get_current_user():
#     res=None
#     if 'user' in session:
#         user = session['user']

#         cursor = get_db()
#         cursor.execute('select * from users where username = %s',(user, ))
#         res = cursor.fetchone()
#     return res



@app.route('/insert_data_from_csv_to_heroku_postgres_db',methods=['GET'])
def login():    
    df=pd.read_csv('data.csv')
    
    cursor = get_db()
    #cursor.execute('insert into voice_banking_users_db(id, first_name, last_name,email, gender, account_number, account_type, on_hold, balance ) values (%s, %s,%s,%s,%s,%s,%s,%s,%s)',(str(df.iloc[i,0]),df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],str(df.iloc[i,5]),df.iloc[i,6],str(df.iloc[i,7]),str(df.iloc[i,8])))
    cursor.execute('select* from voice_banking_users_db')
    users=cursor.fetchall()
    print(users)
    return 'Database deployment (creation and insertion of data given to us) done....'

if __name__ == '__main__':
    app.run(debug=True)