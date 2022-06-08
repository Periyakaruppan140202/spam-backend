from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
import requests
stringie="""
<main_screen>:
    md_bg_color:(245/255, 171/255, 201/255,1)
    MDBoxLayout:
        padding:"10sp","10sp"
        md_bg_color:(255/255, 229/255, 226/255,1)
        pos_hint:{"center_x":0.5,"center_y":0.5}
        size_hint:0.7,0.7
        radius:[30]
        orientation:"vertical"
        spacing:"10sp"
        MDLabel:
            id:lb1
            text:"Spam Check"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (233/255, 59/255, 129/255,1)
            font_style:"H4"
            adaptive_height:1
        MDTextField:
            id:tf2
            hint_text: "URL"
            size_hint_x:0.8
            color_mode: 'custom'
            text:"192.168.29.187:5000"
            line_color_normal:(182/255, 201/255, 240/255,1)
            pos_hint:{"center_x":0.5,"center_y":0.5}
            line_color_focus: (182/255, 201/255, 240/255,1)
            helper_text: "enter the url here"
            helper_text_mode: "on_focus"
        MDTextField:
            id:tf1
            multiline: True
            hint_text: "Type here...!"
            size_hint:0.8,0.7
            color_mode: 'custom'
            line_color_normal:(182/255, 201/255, 240/255,1)
            pos_hint:{"center_x":0.5,"center_y":0.5}
            line_color_focus: (182/255, 201/255, 240/255,1)
            helper_text: "Check for SPAM msg"
            helper_text_mode: "on_focus"
        MDFillRoundFlatIconButton:
            icon: "trash-can-outline"
            text: "Check"
            md_bg_color:(233/255, 59/255, 129/255,1)
            pos_hint:{"center_x":0.5,"center_y":0.5}
            on_release:root.check(tf1.text)
        
"""
Builder.load_string(stringie)
default="192.168.29.187:5000"
class main_screen(MDScreen):
    def check(self,string):
        default=self.ids.tf2.text
        try:
            if string=="":
                return
            result=requests.post(f"http://{default}/predict/{string}")
            self.ids.lb1.text=result.text
        except Exception as e:
            print(e)
            self.ids.lb1.text="Oops"
class GUI_MLapp(MDApp):
    def build(self):
        Main_screen=main_screen()
        return Main_screen


if __name__=="__main__":
    gui_object=GUI_MLapp()
    gui_object.run()