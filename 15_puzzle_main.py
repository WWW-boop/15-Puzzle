from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class FifteenPuzzle(GridLayout):
    def __init__(self, **kwargs):
        super(FifteenPuzzle, self).__init__(**kwargs)
        self.cols = 2  
        
        for i in range(4):
            button = Button(text = f'{i + 1}')
            self.add_widget(button)




class FifteenPuzzleApp(App): 
    def build(self):
        return FifteenPuzzle()

if __name__ == '__main__':
    FifteenPuzzleApp().run()

