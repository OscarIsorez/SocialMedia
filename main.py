from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.filemanager import MDFileManager

from kivy.uix.button import Button
from kivymd.toast import toast

from icecream import ic

from database import Database

import os


KV = """
BoxLayout:
    orientation: 'vertical'

    MDScreenManager:
        SignupScreen:
        LoginScreen:
        MainScreen: 


<SignupScreen>:
    name: 'signup'

    profilename: nom_field
    email: email_field
    password: password_field
    
    BoxLayout:

        orientation: 'vertical'
        MDTextField:
            max_text_length: 20
            hint_text: "Nom"
            id: nom_field
            size_hint: None, None
            size: 200, 40
            pos_hint: {"center_x": 0.5}
            
            
        MDTextField:
            max_text_length: 30
            hint_text: "Adresse e-mail"
            id: email_field
            size_hint: None, None
            size: 200, 40
            pos_hint: {"center_x": 0.5}
        MDTextField:
            max_text_length: 20
            hint_text: "Mot de passe"
            id: password_field
            size_hint: None, None
            size: 200, 40
            pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: "SIGN UP"
            on_release:  root.SignupButton()
        MDRaisedButton:
            text: "Déjà inscrit ? Connectez-vous"
            on_release:
                root.manager.current = 'login'
                root.clear()
<MainScreen>:
    name: 'main'

    MDBottomNavigation:

        radius: [25, 25, 25, 25]
        pos_hint: {'center_x': .5, 'center_y': .52}


        MDBottomNavigationItem:
            name: 'screen 1'
            text: "Page 1"
            icon: 'greenhouse'
            on_tab_release: root.on_enter_tab1()

            ScrollView:
                GridLayout:
                    id:grid
                    cols: 1
                    spacing: 10
                    size_hint_y: None
                    height: self.minimum_height

        MDBottomNavigationItem:
            name: 'screen 2'
            text: "Page 2"
            icon: 'format-list-bulleted'

            ScrollView:
                MDList:
                    id:list
                    cols: 1
                    spacing: 10
                    size_hint_y: None
                    height: self.minimum_height
                 
              
        MDBottomNavigationItem:
            name: 'screen 3'
            text: "Page 3"
            icon: 'plus-box'
            MDFloatLayout:
                MDLabel:    
                    text: "Ajouter une photo"
                    theme_text_color: "Secondary"
                    halign: 'center'
                    pos_hint: {"center_x": .5, "center_y": .6}
                MDRoundFlatIconButton:
                    text: "Open manager"
                    icon: "folder"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.file_manager_open()

                MDLabel:
                    text:"Ajouter une description"
                    theme_text_color: "Secondary"
                    halign: 'center'
                    pos_hint: {"center_x": .5, "center_y": .3}
                MDTextField:
                    hint_text: "Description"
                    id: description_field
                    size_hint: None, None
                    size: 200, 40
                    pos_hint: {"center_x": 0.5, "center_y": .2}

                MDRaisedButton:
                    text: "Ajouter"
                    pos_hint: {"center_x": .5, "center_y": .1}
                    on_release: 
                        root.add_smart_tile(root.path, description_field.text)
                        root.clear()
    
        MDBottomNavigationItem:
            name: 'screen 4'
            text: "Page 4"
            icon: 'face-man-shimmer'
            on_tab_release: root.on_enter_tab4()
            background_color: (1, 0, 1, .5)
            
            BoxLayout:
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: 1, 0, 1, 1  # Couleur du contour (violet dans cet exemple)
                    Line:
                        width: 1  # Ajustez la valeur pour l'épaisseur du contour
                        rectangle: self.x, self.y, self.width, self.height
                MDLabel:
                    id:displayInfos
                    text: "Bienvenue"
                    theme_text_color: "Secondary"  
                    # size_hint: None, None
                    # size: dp(200), dp(100)
                    halign: 'center'
                    valign: 'middle'
            MDRaisedButton:
                text: "Logout"
                pos_hint: {"center_x": .5, "center_y": .1}
                on_release:
                    root.manager.current = 'login' 
                    root.clear()
    


                
<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            hint_text: "Adresse e-mail"
            id: login_email_field
            size_hint: None, None
            size: 200, 40
            pos_hint: {"center_x": 0.5}
        MDTextField:
            hint_text: "Mot de passe"
            id: login_password_field
            size_hint: None, None
            size: 200, 40
            pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: "LOGIN"
            on_release:  root.LoginButton()
        MDRaisedButton:
            text: "Create Account"
            on_release:  
                root.manager.current = 'signup'
                root.clear()
"""


class LoginScreen(Screen):
    def LoginButton(self):
        app = MDApp.get_running_app()

        app.db.show_users_db()
        if app.db.validate_infos(
            self.ids.login_email_field.text, self.ids.login_password_field.text
        ):
            app.current_user = app.db.select_user_by_mail(
                self.ids.login_email_field.text
            )
            self.manager.current = "main"
            self.manager.get_screen("main").on_enter_tab1()
            self.manager.get_screen("main").on_enter_tab2()
            self.manager.get_screen("main").on_enter_tab4()

            toast("Connexion réussie !")

            ic(app.current_user)
            self.clear()

        else:
            toast("Identifiants incorrects !")

    def clear(self):
        self.ids.login_email_field.text = ""
        self.ids.login_password_field.text = ""


class SignupScreen(Screen):
    profilename = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def afficher_infos(self):
        ic(self.profilename.text)
        ic(self.email.text)
        ic(self.password.text)

    def SignupButton(self):
        app = MDApp.get_running_app()
        # on ajoute les infos dans la base de données
        if (
            self.profilename.text == ""
            or self.email.text == ""
            or self.password.text == ""
        ):
            toast("Veuillez remplir tous les champs")
        else:
            app.db.insert_user(
                self.profilename.text, self.email.text, self.password.text
            )

            self.afficher_infos()

            self.clear()

            self.manager.current = "login"

    def add_user(self):
        self.app = MDApp.get_running_app()
        self.app.db.insert_user(
            self.profilename.text, self.email.text, self.password.text
        )

    def clear(self):
        self.ids.nom_field.text = ""
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    profilename = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def on_enter(self):
        grid = self.ids.grid
        grid.clear_widgets()
        grid.height = self.height

    def on_enter_tab1(self):
        # on affiche les posts de tous les utilisateurs
        app = MDApp.get_running_app()
        grid = self.ids.grid
        grid.clear_widgets()
        grid.height = self.height
        posts = app.db.select_all_posts()
        ic(posts)
        for post in posts:
            self.add_smart_tile(post[3], post[2])

    def on_enter_tab2(self):
        # on affiche la liste de tous les utilisateurs, leur nom et leur adresse e-mail
        app = MDApp.get_running_app()
        list = self.ids.list
        list.clear_widgets()
        list.height = self.height
        users = app.db.select_all_users()
        ic(users)

    def clear(self):
        self.ids.description_field.text = ""
        self.path = ""
        self.desc = ""

    def add_smart_tile(self, path, desc):
        smart_tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(1, 1, 1, 0.2),
            source=path,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=("350", "350"),
        )

        icon_button = MDIconButton(
            icon="heart-outline",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5},
        )
        icon_button.bind(
            on_release=lambda instance: setattr(
                icon_button,
                "icon",
                "heart" if icon_button.icon == "heart-outline" else "heart-outline",
            )
        )

        label = MDLabel(text=desc, bold=True, color=(1, 1, 1, 1))

        smart_tile.add_widget(icon_button)
        smart_tile.add_widget(label)

        self.ids.grid.add_widget(smart_tile)
        self.app = MDApp.get_running_app()
        # si le les champs sont vides on affiche un message d'erreur
        if self.ids.description_field.text == "" or self.path == "":
            toast("Veuillez remplir tous les champs")
        else:
            self.app.db.insert_post(self.app.current_user[0], desc, path)
        toast("Post ajouté !")

    def on_enter_tab4(self):
        app = MDApp.get_running_app()
        self.user_infos = [
            app.current_user[1],
            app.current_user[2],
            app.current_user[3],
        ]
        ic(self.user_infos)
        self.ids.displayInfos.text = (
            "Bienvenue, "
            + self.user_infos[0]
            + " !"
            + "\n"
            + "Adresse e-mail : "
            + self.user_infos[1]
            + "\n"
            + "Mot de passe : "
            + self.user_infos[2]
        )  # on affiche le nom de l'utilisateur connecté
        self.ids.displayInfos.font_style = "H5"
        self.ids.displayInfos.halign = "center"

    def file_manager_open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path):
        self.path = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def clear(self):
        self.ids.description_field.text = ""
        self.path = ""
        self.desc = ""
        self.ids.displayInfos.text = ""
        self.on_enter_tab4()


class MainsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database("database.db")
        self.db.create_tables()

        self.current_user = None

    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(SignupScreen(name="signup"))
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(MainScreen(name="main"))

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_stop(self):
        self.db.close()


if __name__ == "__main__":
    MainsApp().run()
