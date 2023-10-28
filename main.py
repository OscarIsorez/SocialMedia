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

from kivy.uix.button import Button

from icecream import ic


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
            on_release:  
                root.manager.current = 'login'
                root.afficher_infos()

<MainScreen>:
    name: 'main'

    MDBottomNavigation:

        radius: [25, 25, 25, 25]
        pos_hint: {'center_x': .5, 'center_y': .52}


        MDBottomNavigationItem:
            name: 'screen 1'
            text: "Page 1"
            icon: 'greenhouse'

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



        MDBottomNavigationItem:
            name: 'screen 3'
            text: "Page 3"
            icon: 'plus-box'
            on_tab_release: root.on_enter_tab3()
            MDFloatLayout:

                MDRoundFlatIconButton:
                    text: "Open manager"
                    icon: "folder"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.file_manager_open()
    
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
            on_release:  root.manager.current = 'main'
        MDRaisedButton:
            text: "Create Account"
            on_release:  root.manager.current = 'signup'
"""


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    profilename = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def afficher_infos(self):
        ic(self.profilename.text)
        ic(self.email.text)
        ic(self.password.text)


class MainScreen(Screen):
    profilename = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def on_enter(self):
        grid = self.ids.grid
        grid.clear_widgets()
        grid.height = self.height

    def add_smart_tile(self):
        smart_tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(1, 1, 1, 0.2),
            source="cat.jpg",
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

        label = MDLabel(text="Julia and Julie", bold=True, color=(1, 1, 1, 1))

        smart_tile.add_widget(icon_button)
        smart_tile.add_widget(label)

        self.ids.grid.add_widget(smart_tile)
        ic("Smart tile added !")

    def on_enter_tab3(self):
        self.add_smart_tile()

    def on_enter_tab4(self):
        self.ids.displayInfos.text = "Bienvenue, " + str(
            self.manager.get_screen("signup").profilename.text
            + " !\n"
            + "Votre adresse e-mail est : \n"
            + str(self.manager.get_screen("signup").email.text)
            + "\n"
            + "Votre mot de passe est : \n"
            + str(self.manager.get_screen("signup").password.text)
        )


class MainsApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(SignupScreen(name="signup"))
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(MainScreen(name="main"))
        ic(self.screen_manager.screens)

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


if __name__ == "__main__":
    MainsApp().run()
