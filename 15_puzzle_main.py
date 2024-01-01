from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from random import shuffle

class FifteenPuzzle(BoxLayout):
    def __init__(self, **kwargs):
        super(FifteenPuzzle, self).__init__(**kwargs)
        self.orientation = 'vertical'  

        with self.canvas.before:
            Color(255, 255, 255, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)

        self.game_layout = GridLayout(cols=4, spacing=5)
        self.add_widget(self.game_layout)

        self.tiles = [str(i) for i in range(1, 16)] + ['']
        shuffle(self.tiles)
        self.create_board()

        self.timer_layout = BoxLayout(size_hint=(1, 0.1))  
        self.add_widget(self.timer_layout)

        self.timer_label = Button(text="Time: 00:00", font_size=20, size_hint=(0.8, 1))
        self.timer_layout.add_widget(self.timer_label)

        self.elapsed_time = 0
        self.game_running = False

        reset_button = Button(text='Reset', on_press=self.reset_puzzle)
        self.timer_layout.add_widget(reset_button)

    def create_board(self):
        for tile in self.tiles:
            button = Button(text=tile, font_size=30, on_press=self.tile_click)
            self.game_layout.add_widget(button)

    def is_solved(self):
        return self.tiles == [str(i) for i in range(1, 16)] + ['']

    def tile_click(self, instance):
        if not self.game_running:
            self.game_running = True
            self.timer_label.text = "Time: 00:00"
            self.elapsed_time = 0
            Clock.schedule_interval(self.update_timer, 1)

        current_index = self.tiles.index(instance.text)
        empty_index = self.tiles.index('')
        if self.is_adjacent(current_index, empty_index):
            self.tiles[current_index], self.tiles[empty_index] = self.tiles[empty_index], self.tiles[current_index]
            self.animate_tile_move(instance, current_index, empty_index)

        if self.is_solved():
            self.game_running = False
            Clock.unschedule(self.update_timer)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            congratulations_message = f"Congratulations! Puzzle Solved in {minutes:02}:{seconds:02}"
            self.timer_label.text = congratulations_message

    def animate_tile_move(self, instance, from_index, to_index):
        row_from, col_from = divmod(from_index, 4)
        row_to, col_to = divmod(to_index, 4)

        cell_size = instance.width, instance.height
        target_pos = (
            col_to * cell_size[0] + self.game_layout.x,
            (3 - row_to) * cell_size[1] + self.game_layout.y,)

        anim = Animation(pos=target_pos, duration=0.2)
        anim.start(instance)
        anim.bind(on_complete=lambda _, __: self.on_animation_complete())

    def on_animation_complete(self):
        self.update_buttons()
        if self.check_win():
            Clock.unschedule(self.update_timer)
            self.game_running = False

    def check_win(self):
        return self.tiles == [str(i) for i in range(1, 16)] + ['']
    
    def is_adjacent(self, index1, index2):
        row1, col1 = divmod(index1, 4)
        row2, col2 = divmod(index2, 4)
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

    def update_buttons(self):
        self.game_layout.clear_widgets()
        for tile in self.tiles:
            button = Button(text=tile, font_size=30, on_press=self.tile_click)
            self.game_layout.add_widget(button)

    def update_timer(self, dt):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.text = f"Time: {minutes:02}:{seconds:02}"

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def reset_puzzle(self, instance):
        self.tiles = [str(i) for i in range(1, 16)] + ['']
        shuffle(self.tiles)
        self.game_layout.clear_widgets()
        self.create_board()
        self.game_running = False
        Clock.unschedule(self.update_timer)
        self.timer_label.text = "Time: 00:00"
    
class FifteenPuzzleApp(App): 
    def build(self):
        return FifteenPuzzle()

if __name__ == '__main__':
    FifteenPuzzleApp().run()
