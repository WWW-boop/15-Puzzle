from kivy.app import App
from kivy.uix.gridlayout import GridLayout

   
class FifteenPuzzleApp(App):
    def build(self):
        return GridLayout()

if __name__ == '__main__':
    FifteenPuzzleApp().run()

