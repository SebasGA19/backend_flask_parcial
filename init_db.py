import hashlib
import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
urls = ['https://www.foodandwine.com/thmb/4qg95tjf0mgdHqez5OLLYc0PNT4=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/classic-cheese-pizza-FT-RECIPE0422-31a2c938fc2546c9a07b7011658cfd05.jpg','https://s7d1.scene7.com/is/image/mcdonalds/DC_201907_0005_BigMac_832x472:product-header-desktop?wid=830&hei=458&dpr=off','https://s7d1.scene7.com/is/image/mcdonalds/202002_0592_McDouble_Alt_832x472:product-header-desktop?wid=830&hei=458&dpr=off','https://www.burgerking.be/_nuxt/image/fad335.webp']
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('chorigue', hashlib.sha512(b"12345").hexdigest())
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('juanperez13', hashlib.sha512(b"123456").hexdigest())
            )

cur.execute("INSERT INTO products (name, store, image_url, rating) VALUES (?, ?, ?, ?)",
            ('Pizza', 'Dominos', f'{urls[0]}', '4.0')
            )

cur.execute("INSERT INTO products (name, store, image_url, rating) VALUES (?, ?, ?, ?)",
            ('Big Mac', 'McDonalds', f'{urls[1]}', '4.1')
            )

cur.execute("INSERT INTO products (name, store, image_url, rating) VALUES (?, ?, ?, ?)",
            ('MacDoucle', 'McDonalds', f'{urls[2]}', '4.3')
            )

cur.execute("INSERT INTO products (name, store, image_url, rating) VALUES (?, ?, ?, ?)",
            ('Whooper', 'Burguer King', f'{urls[3]}', '4.5')
            )

connection.commit()
connection.close()