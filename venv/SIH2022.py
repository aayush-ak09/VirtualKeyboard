import cvzone as cz
import cv2
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

cap = cv2.VideoCapture(0)
cap.set(3, 1980)
cap.set(4, 1280)

class KeyboardGrid(GridLayout):
    def __init__(self,**kwargs):      # contructor with one or many arguments
        super(KeyboardGrid, self).__init__()
        self.cols=3
        self.add_widget(shape='square')

        self.add_widget(shape='square')

        self.add_widget(shape='square')

        self.add_widget(shape='square')

        self.press = Button(text='Camera')
        self.press.bind(on_press=self.Camera)
        self.add_widget(self.press)

        self.add_widget(shape='square')

        self.add_widget(shape='square')

        self.add_widget(shape='square')

        self.add_widget(shape='square')

    def Camera(self, instance):
        while True:
            success, img = cap.read()
            cv2.imshow("Image", img)
            cv2.waitKey(1)


class KeyboardApp(App):
    def build(self):
        return KeyboardGrid()

if __name__ == '__main__':
    KeyboardApp().run()


