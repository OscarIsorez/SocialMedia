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

        # liked est une liste au format json de user_id séparés par des virgules (ex: "[1,2,3]")
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                description TEXT,
                path TEXT,
                liked TEXT,
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

    def insert_post(self, user_id, description, path, liked):
        self.cur.execute(
            "INSERT INTO posts (user_id, description, path, liked) VALUES (?, ?, ?, ?)",
            (user_id, description, path, liked),
        )
        self.conn.commit()

    def update_post(self, post_id, description, path, liked):
        self.cur.execute(
            "UPDATE posts SET description = ?, path = ?, liked = ? WHERE id = ?",
            (description, path, liked, post_id),
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

    def select_post_by_id(self, post_id):
        self.cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return self.cur.fetchone()

    def select_post_by_path_and_description(self, path, description):
        self.cur.execute(
            "SELECT * FROM posts WHERE path = ? AND description = ?",
            (path, description),
        )
        return self.cur.fetchone()

    def select_all_posts(self):
        self.cur.execute("SELECT * FROM posts")
        return self.cur.fetchall()

    def select_all_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def update_likes_for_post(self, post_id, liked):
        self.cur.execute(
            "UPDATE posts SET liked = ? WHERE id = ?",
            (liked, post_id),
        )
        self.conn.commit()

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

    def suppr_post_by_id(self, post_id):
        self.cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
