from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from random import shuffle

class FifteenPuzzle(GridLayout):
    def __init__(self, **kwargs):
        super(FifteenPuzzle, self).__init__(**kwargs)
        self.cols = 4
        self.spacing = 5
        self.tiles = [str(i) for i in range(1, 16)] + ['']
        shuffle(self.tiles)
        
        for tile in self.tiles:
            button = Button(text=tile,font_size=30)
            self.add_widget(button)




class FifteenPuzzleApp(App): 
    def build(self):
        return FifteenPuzzle()

if __name__ == '__main__':
    FifteenPuzzleApp().run()

