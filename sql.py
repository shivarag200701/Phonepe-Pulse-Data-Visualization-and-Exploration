from phone_pe import *
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    port='3306',
    database='phonepe'
)
cursor = cnx.cursor()

#agg_trans
cursor.execute("""create table agg_trans (Transaction_method varchar(100),Transaction_count int,Transaction_amounts double,State varchar(100), Year int, Quarter int)""")
for i,row in aggregated_transaction.iterrows():
    sql = "INSERT INTO agg_trans VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    # the connection is not auto committed by default, so we must commit to save our changes
    cnx.commit()

#agg_user

cursor.execute("create table agg_user (brand varchar(100),Count int,Percentage double,State varchar(100), Year int, Quarter int )")
for i,row in aggregated_users.iterrows():
    sql = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

#map_trans
cursor.execute("create table map_trans ( District varchar(100),Count int,Amount double,State varchar(100), Year int, Quarter int  )")
for i,row in map_transaction.iterrows():
    sql = "INSERT INTO map_trans VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

#map_user
cursor.execute("create table map_user (District varchar(100),Registered_user int,App_opens int,State varchar(100), Year int, Quarter int)")

for i,row in map_user.iterrows():
    sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

#top_trans
cursor.execute("create table top_trans (Pincode int,transaction_count int,transaction_amount double,State varchar(100), Year int, Quarter int )")

for i,row in pin_tran.iterrows():
    sql = "INSERT INTO top_trans VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

#top_user
cursor.execute("create table top_user (Pincode int,Registered_users int,State varchar(100), Year int, Quarter int )")

for i,row in pin_users.iterrows():
    sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()