import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Créez la table des utilisateurs s'ils n'existent pas
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                email TEXT
            )
        """
        )
        self.conn.commit()

        # Créez la table des posts s'ils n'existent pas
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                description TEXT,
                path TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )
        self.conn.commit()

    def insert_user(self, username, password, email):
        self.cur.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email),
        )
        self.conn.commit()

    def insert_post(self, user_id, description, path):
        self.cur.execute(
            "INSERT INTO posts (user_id, description, path) VALUES (?, ?, ?)",
            (user_id, description, path),
        )
        self.conn.commit()

    def select_user_by_mail(self, mail):
        self.cur.execute("SELECT * FROM users WHERE email = ?", (mail,))
        return self.cur.fetchone()

    def select_user(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cur.fetchone()

    def select_user_by_id(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.cur.fetchone()

    def select_posts_by_user(self, user_id):
        self.cur.execute("SELECT * FROM posts WHERE user_id = ?", (user_id,))
        return self.cur.fetchall()

    def select_all_posts(self):
        self.cur.execute("SELECT * FROM posts")
        return self.cur.fetchall()

    def select_all_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def validate_infos(self, mail, password):
        # si les paramètres correspondent bien à un utilisateur existant
        user = self.select_user_by_mail(mail)
        if user is None:
            return False
        if user[2] != password:
            return False
        return True

    def show_users_db(self):
        # on affiche la table users en console
        self.cur.execute("SELECT * FROM users")
        print(self.cur.fetchall())

    def show_posts_db(self):
        # on affiche la table posts en console
        self.cur.execute("SELECT * FROM posts")
        print(self.cur.fetchall())

    def show_all_db(self):
        # on affiche les deux tables en console
        self.show_users_db()
        self.show_posts_db()

    def suppr_all_users(self):
        self.cur.execute("DELETE FROM users")
        self.conn.commit()

    def suppr_all_posts(self):
        self.cur.execute("DELETE FROM posts")
        self.conn.commit()
