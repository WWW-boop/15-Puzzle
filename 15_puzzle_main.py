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
        self.create_board()

    def create_board(self):
        for tile in self.tiles:
            button = Button(text=tile, font_size=30, on_press=self.tile_click)
            self.add_widget(button)

    def tile_click(self, instance):
        current_index = self.tiles.index(instance.text)
        empty_index = self.tiles.index('')
        if self.is_adjacent(current_index, empty_index):
            self.tiles[current_index], self.tiles[empty_index] = self.tiles[empty_index], self.tiles[current_index]
            self.update_buttons()

    def is_adjacent(self, index1, index2):
        row1, col1 = divmod(index1, 4)
        row2, col2 = divmod(index2, 4)
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

    def update_buttons(self):
        self.clear_widgets()
        for tile in self.tiles:
            button = Button(text=tile, font_size=30, on_press=self.tile_click)
            self.add_widget(button)




class FifteenPuzzleApp(App): 
    def build(self):
        return FifteenPuzzle()

if __name__ == '__main__':
    FifteenPuzzleApp().run()

