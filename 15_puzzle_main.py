from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from random import shuffle

from kivy.uix.popup import Popup
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.slider import Slider


class SettingsButton(ButtonBehavior, Image):
    pass

class FifteenPuzzle(BoxLayout,):

    def __init__(self, **kwargs):
        super(FifteenPuzzle, self).__init__(**kwargs)
        self.orientation = 'vertical'  

        with self.canvas.before:
            Color(255, 255, 255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)
            
        self.game_layout = GridLayout(cols=4, spacing=10,)
        self.add_widget(self.game_layout)

        self.tiles = [str(i) for i in range(1, 16)] + ['']
        shuffle(self.tiles)
        self.create_board()

        self.timer_layout = BoxLayout(size_hint=(1, 0.1))  
        self.add_widget(self.timer_layout)

        self.timer_label = Button(text="Time: 00:00", font_size=25, size_hint=(0.8, 1),background_color=(0,0,0,1))
        self.timer_layout.add_widget(self.timer_label)

        self.elapsed_time = 0
        self.game_running = False

        reset_button = Button(text='Reset', on_press=self.reset_puzzle,size_hint=(0.1,1),background_color=(0,0,0,1))
        self.timer_layout.add_widget(reset_button)

        self.music_sound = SoundLoader.load('sound\music_sound.wav')
        self.win_sound = SoundLoader.load('sound\win_sound.wav')
        self.music_sound.volume = 0.1
        self.win_sound.volume = 0.4
        self.play_music_sound()

        self.pause_resume_button = Button(text='Pause', on_press=self.pause_resume_timer, size_hint=(0.1, 1),background_color=(0,0,0,1))
        self.timer_layout.add_widget(self.pause_resume_button)
        
        help_button = Button(text='Help', on_press=self.show_help_popup, size_hint=(0.1, 1),background_color=(0,0,0,1))
        self.timer_layout.add_widget(help_button)

        self.button_click_count = 0

        settings_button = SettingsButton(source='image\settings_icon.png', on_press=self.show_settings_popup,size_hint=(0.1, 1))
        self.timer_layout.add_widget(settings_button)

    def show_help_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        how_to_play_label = Label(text='How to Play', font_size=24)
        content.add_widget(how_to_play_label)
        content.add_widget(Label(text='1. Click on a tile adjacent to the empty space to move it.'))
        content.add_widget(Label(text='2. Try to arrange the numbers in ascending order.'))
        content.add_widget(Label(text='3. Click the "Reset" button to start a new game.'))
        content.add_widget(Label(text='4. Have fun!'))

        popup = Popup(title='Help / Instructions', content=content, size_hint=(None, None), size=(700, 500))
        popup.open()

    def show_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Settings'))
        content.add_widget(Button(text='Theme'))
        content.add_widget(Button(text='Option 2'))

        volume_label = Label(text='Volume')
        content.add_widget(volume_label)

        volume_slider = Slider(min=0, max=1, value=self.music_sound.volume)
        volume_slider.bind(value=self.update_volume)
        content.add_widget(volume_slider)

        popup = Popup(title='Settings', content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    def create_board(self):
        for tile in self.tiles:
            if tile:  
                button = Button(text=tile, font_size=50, on_press=self.tile_click,background_color=(251,0, 0,0.8),color=(0,0,0,1))
            else:
                button = Label(text='', font_size=30)  
            self.game_layout.add_widget(button)
    

    def is_solved(self):
        return self.tiles == [str(i) for i in range(1, 16)] + ['']

    def tile_click(self, instance):
        if not self.game_running:
            self.game_running = True
            self.timer_label.text = "Time: 00:00"
            self.elapsed_time = 0
            Clock.schedule_interval(self.update_timer, 1)

        self.play_click_sound() 
        self.button_click_count += 1

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
            self.timer_label.text += f"\nButton Clicks: {self.button_click_count}"

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
            self.play_win_sound()

    def play_win_sound(self):
        if self.win_sound:
            if self.music_sound and self.music_sound.state == 'play':
                self.music_sound.stop()
            self.win_sound.play()

    def play_music_sound(self):
        if self.music_sound:
            self.music_sound.play()

    def play_click_sound(self):
        click_sound = SoundLoader.load('sound\press_sound.wav')
        click_sound.volume = 0.5
        if click_sound:
            click_sound.play()

    def check_win(self):
        return self.tiles == [str(i) for i in range(1, 16)] + ['']
    
    def is_adjacent(self, index1, index2):
        row1, col1 = divmod(index1, 4)
        row2, col2 = divmod(index2, 4)
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

    def update_buttons(self):
        self.game_layout.clear_widgets()
        for tile in self.tiles:
            if tile:  
                button = Button(text=tile, font_size=50, on_press=self.tile_click,background_color=(251,0, 0,0.8),color=(0,0,0,1))
            else:
                button = Label(text='', font_size=30)  
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
        self.button_click_count = 0

    def show_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Settings'))
        content.add_widget(Button(text='Theme'))
        content.add_widget(Button(text='Option 2'))


        volume_label = Label(text='Volume')
        content.add_widget(volume_label)

        volume_slider = Slider(min=0, max=1, value=self.music_sound.volume)
        volume_slider.bind(value=self.update_volume)
        content.add_widget(volume_slider)

        popup = Popup(title='Settings', content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    def update_volume(self, instance, value):
        self.music_sound.volume = value
        self.win_sound.volume = value
    
    def pause_resume_timer(self, instance):
        if self.game_running:
            if self.pause_resume_button.text == 'Pause':
                Clock.unschedule(self.update_timer)
                self.pause_resume_button.text = 'Resume'
            else:
                Clock.schedule_interval(self.update_timer, 1)
                self.pause_resume_button.text = 'Pause'

    def update_music_volume(self, instance, value):
        self.music_sound.volume = value

    def update_win_sound_volume(self, instance, value):
        self.win_sound.volume = value
    
class FifteenPuzzleApp(App): 
    def build(self):
        return FifteenPuzzle()

if __name__ == '__main__':
    FifteenPuzzleApp().run()