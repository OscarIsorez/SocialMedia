from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivymd.toast import toast

from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

from icecream import ic

from database import Database

import os
import json


KV = """
BoxLayout:
    orientation: 'vertical'

    MDScreenManager:
        LoginScreen:
        SignupScreen:
        MainScreen: 
        UserDetailScreen:


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
                    width: self.width
                    height: self.height

        MDBottomNavigationItem:
            name: 'screen 2'
            text: "Page 2"
            icon: 'format-list-bulleted'

            ScrollView:
                
                
                MDList:
                    id:user_list
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
                        root.add_smart_tile(root.path, description_field.text,  "[]")
                        root.clear()
    
        MDBottomNavigationItem:
            name: 'screen 4'
            text: "Page 4"
            icon: 'face-man-shimmer'
            on_tab_release: root.on_enter_tab4()

            BoxLayout:
                orientation : 'horizontal'
                MDFloatingActionButton:
                    icon: "camera-plus-outline"
                    pos_hint: {"center_y": .9}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.file_manager_open()


                
            BoxLayout:
                padding: 10
                orientation: 'vertical'

                MDLabel:
                    id: displayInfos
                    text: "Bienvenue"
                    theme_text_color: "Secondary"
                    halign: 'center'
                    valign: 'middle'

                MDRaisedButton:
                    text: "Logout"
                    pos_hint: {"center_x": .5, "center_y": .1}
                    padding: 10
                    on_release:
                        root.manager.current = 'login' 
                        root.clear()

                BoxLayout:
                    size_hint_y : None
                    height : 10
                   

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 0.7  

                    ScrollView:
                        GridLayout:
                            id: grid_tab4
                            cols: 2  
                            spacing: 10
                            padding: 10
                            size_hint_y: None
                            height: self.minimum_height


                
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

<UserDetailScreen>:
    name: 'user_profile'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(48)
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {"center_x": .1, "center_y": .5}
                on_release: root.manager.current = 'main'
            MDLabel:
                text: "Profil"
                bold: True
                theme_text_color: "Secondary"
                font_style: "H6"

        BoxLayout:
            orientation: 'vertical'

            MDLabel:
                id: user_name_label
                text: "Nom : "
                theme_text_color: "Secondary"
                halign: 'center'
                valign: 'middle'
            MDLabel:
                id: user_email_label
                text: "Adresse e-mail : "
                theme_text_color: "Secondary"
                halign: 'center'
                valign: 'middle'
                pos_hint: {"center_x": .5}
                background_color: (1, 1, 1, )

        BoxLayout:
            size_hint_y : None
            height : 10
            #la ligne est visible car elle a une couleur
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1
                Line:
                    width: 1
                    rectangle: self.x, self.y, self.width,dp(1)


        
        ScrollView:
            do_scroll_y: True
            id:scrollview_profiles_post

            GridLayout:
                id: user_posts_grid
                cols: 2
                spacing: 10
                padding: 10
                size_hint_y: None
                height: self.minimum_height

"""


class UserDetailScreen(Screen):
    def fill_user_posts_grid(self, user):
        app = MDApp.get_running_app()
        grid = self.ids.user_posts_grid
        grid.clear_widgets()
        grid.height = self.height / 2

        posts = app.db.select_posts_by_user(user[0])

        self.ids.scrollview_profiles_post.do_scroll_y = True
        if len(posts) == 0:
            label = MDLabel(
                text="Aucune photo à afficher pour le moment",
                bold=True,
                halign="center",
                color=(1, 1, 1, 1),
            )
            self.ids.scrollview_profiles_post.do_scroll_y = False

            grid.add_widget(label)
        for post in posts:
            self.add_smart_tile(post[3], post[2])

    def add_smart_tile(self, path, desc):
        smart_tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(1, 1, 1, 0.2),
            source=path,
            size_hint=(None, None),
            size=(self.width / 2.3, self.width / 2.3),
        )

        label = MDLabel(text=desc, bold=True, color=(1, 1, 1, 1))

        smart_tile.add_widget(label)

        self.ids.user_posts_grid.add_widget(smart_tile)


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

    def show_user_profile(self, user_id):
        app = MDApp.get_running_app()
        user = app.db.select_user_by_id(user_id)
        self.manager.current = "user_profile"
        self.user_screen = self.manager.get_screen("user_profile")

        self.user_screen.ids.user_name_label.text = "Nom : " + user[1]
        self.user_screen.ids.user_email_label.text = "Adresse e-mail : " + user[2]

        # on affiche les posts de l'utilisateur
        self.user_screen.fill_user_posts_grid(user)

    def on_enter(self):
        grid = self.ids.grid
        grid.clear_widgets()
        grid.height = self.height
        self.ids.displayInfos.text = ""
        self.on_enter_tab1()
        self.on_enter_tab2()
        self.on_enter_tab4()

    def on_enter_tab1(self):
        app = MDApp.get_running_app()
        grid = self.ids.grid
        grid.clear_widgets()

        total_height = 0

        grid.add_widget(BoxLayout(size_hint_y=None, height=10))  # margin top

        posts = app.db.select_all_posts()
        for post in posts:
            total_height += self.width
            self.add_smart_tile(post[3], post[2], post[4])

        grid.height = total_height + 55  # we had a little margin at the bottom

    def on_enter_tab2(self):
        app = MDApp.get_running_app()
        list = self.ids.user_list
        list.clear_widgets()
        list.height = self.height
        users = app.db.select_all_users()
        for user in users:
            list.add_widget(
                OneLineIconListItem(
                    IconLeftWidget(icon="account"),
                    text=user[1]
                    if user[1] != app.current_user[1]
                    else user[1] + " (Vous)",
                    on_release=lambda x, y=user[0]: self.on_user_click(y),
                )
            )

    def on_user_click(self, user_id):
        self.show_user_profile(user_id)

    def clear(self):
        self.ids.description_field.text = ""
        self.path = ""
        self.desc = ""

    def add_smart_tile(self, path, desc, liked="[]"):
        app = MDApp.get_running_app()

        list_liked = json.loads(liked)

        smart_tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(1, 1, 1, 0.2),
            source=path,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=(self.width, self.width),
        )

        smart_tile.bind(
            on_release=lambda x: self.show_user_profile(
                app.db.select_post_by_path_and_description(path, desc)[1]
            )
        )

        icon_button = MDIconButton(
            icon="heart-outline" if app.current_user[0] not in list_liked else "heart",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5},
        )

        icon_button.bind(
            on_release=lambda x: self.change_icon(icon_button, path, desc),
        )

        label = MDLabel(text=desc, bold=True, color=(1, 1, 1, 1))

        smart_tile.add_widget(icon_button)
        smart_tile.add_widget(label)

        self.ids.grid.add_widget(smart_tile)
        self.app = MDApp.get_running_app()

        if self.ids.description_field.text != "" and self.path != "":
            self.app.db.insert_post(
                self.app.current_user[0],
                desc,
                path,
                "[]",
            )

    def change_icon(self, icon_button, path, desc):
        post = self.app.db.select_post_by_path_and_description(path, desc)
        if icon_button.icon == "heart-outline":
            icon_button.icon = "heart"

            liked = json.loads(post[4])
            if self.app.current_user[0] not in liked:
                liked.append(self.app.current_user[0])
            self.app.db.update_likes_for_post(post[0], json.dumps(liked))

        else:
            icon_button.icon = "heart-outline"
            liked = json.loads(post[4])
            liked.remove(self.app.current_user[0])
            self.app.db.update_likes_for_post(post[0], json.dumps(liked))

    def on_enter_tab4(self):
        app = MDApp.get_running_app()
        self.user_infos = [
            app.current_user[1],
            app.current_user[2],
            app.current_user[3],
        ]
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

        grid = self.ids.grid_tab4
        grid.clear_widgets()
        # grid.height = self.height
        posts = app.db.select_posts_by_user(app.current_user[0])
        for post in posts:
            self.add_smart_tile_tab4(post[3], post[2])

    def add_smart_tile_tab4(self, path, desc):
        gap = self.width / 10
        smart_tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(1, 1, 1, 0.2),
            source=path,
            size_hint=(None, None),
            size=(self.width / 2.3, self.width / 2.3),
        )

        icon_button = MDIconButton(
            icon="delete",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5},
        )

        icon_button.bind(
            on_release=lambda x: self.delete_post(path, desc),
        )

        label = MDLabel(text=desc, bold=True, color=(1, 1, 1, 1))

        smart_tile.add_widget(icon_button)
        smart_tile.add_widget(label)

        self.ids.grid_tab4.add_widget(smart_tile)

    def delete_post(self, path, desc):
        app = MDApp.get_running_app()
        post = app.db.select_post_by_path_and_description(path, desc)
        app.db.suppr_post_by_id(post[0])
        self.on_enter_tab4()

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
        # self.db.suppr_all_posts()

        self.current_user = None

    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(SignupScreen(name="signup"))
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(MainScreen(name="main"))
        self.screen_manager.add_widget(UserDetailScreen(name="user_profile"))

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_stop(self):
        self.db.close()


if __name__ == "__main__":
    MainsApp().run()
