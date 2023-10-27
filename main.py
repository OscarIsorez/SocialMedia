from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from kivy.properties import ObjectProperty, StringProperty


from icecream import ic


# Définir le fichier KV
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

        MDBottomNavigationItem:
            name: 'screen 2'
            text: "Page 2"
            icon: 'format-list-bulleted'



        MDBottomNavigationItem:
            name: 'screen 3'
            text: "Page 3"
            icon: 'plus-box'
    
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
