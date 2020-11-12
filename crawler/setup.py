import db_manager


db_url = 'postgresql://david.szabo@127.0.0.1/sbahn'
conn = db_manager.connect(db_url)

cur = conn.cursor()
db_manager.create_departure_table(cur)

conn.commit()