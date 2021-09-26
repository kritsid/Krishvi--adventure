-- create table voice_banking_users(
--     id integer primary key,
--     first_name varchar(100) not null,
--     last_name varchar(100) not null,
--     email varchar(100) not null,
--     gender varchar(50) not null,
--     account_number numeric not null,
--     account_type varchar(100) not null,
--     on_hold varchar(100) not null,
--     balance  numeric not null
-- );


-- 'insert into voice_banking_users_db(id, first_name, last_name,email, gender, account_number, account_type, on_hold, balance ) values (%s, %s,%s,%s,%s,%s,%s,%s,%s)',(str(df.iloc[i,0]),df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],str(df.iloc[i,5]),df.iloc[i,6],str(df.iloc[i,7]),str(df.iloc[i,8]))
