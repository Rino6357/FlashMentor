from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random

Storage = {
    '1':'11',
    '2':'22',
    '3':'33',
    '4':'44'
}
flashCard = ''

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        top = GridLayout(cols=1)
        bottom = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        worInp = TextInput(
            multiline = True,
            size_hint_y = None,
            height = 50
        )
        worInp2 = TextInput(
            multiline = True,
            size_hint_y = None,
            height = 50
        )
        button2 = Button(
            text='Done',
            on_press=self.go_to_second_screen,
            size_hint_x=None,
            size_hint_y=None,
            height=100,
            width=200
        )

        top.add_widget(Label(text='', size_hint_y=None, height=50))
        top.add_widget(Label(text='Enter Word:', size_hint_y=None, height=80))
        top.add_widget(worInp)
        top.add_widget(Label(text='', size_hint_y=None, height=50))
        top.add_widget(Label(text='Enter Definition:', size_hint_y=None, height=80))
        top.add_widget(worInp2)
        top.add_widget(Label(text=''))
        top.add_widget(Label(text=''))
        bottom.add_widget(Label(text=''))
        button1 = Button(
            text='Add Word',
            on_press=lambda instance: self.on_add_pressed(worInp.text, worInp2.text),
            size_hint_x=None,
            size_hint_y=None,
            height=100,
            width=200
        )
        bottom.add_widget(button1)
        bottom.add_widget(Label(text='', size_hint_x=None, width=200))
        bottom.add_widget(button2)
        bottom.add_widget(Label(text=''))

        self.add_widget(top)
        self.add_widget(bottom)

    def go_to_second_screen(self, instance):
        amtOfCards = len(Storage)
        if amtOfCards > 0:
            global flashCard
            flashCard = random.choice(list(Storage.keys()))
            self.manager.get_screen('second_screen').update_answer_options()
            self.manager.current = 'second_screen'
        else:
            self.show_popup('Not enough flashcards!')


    def on_add_pressed(self, word, definition):
        Storage[word] = definition
        self.show_popup("Word added!")
        print(Storage)
    
    def show_popup(self, text):
        content = Label(text=f"{text}")
        popup = Popup(title="", content=content, size_hint=(None, None), size=(300, 200))
        popup.bind(on_touch_down=popup.dismiss)
        popup.open()

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        topSecond = BoxLayout(orientation='vertical')
        bottomSecond = BoxLayout(orientation='horizontal', height=.8)
        
        self.flashCardBox = Label(
            text='',
            font_size='50sp',
            size_hint=(1, 3.5)
        )
        self.placeHolder = Label(
            text=''
        )

        self.answer_options = []
        self.height = 230

        self.choice1 = Button(
            text='',
            on_press=lambda instance: self.check_answer(instance.text),
            size_hint_y=None,
            height=self.height
        )
        self.choice2 = Button(
            text='',
            on_press=lambda instance: self.check_answer(instance.text),
            size_hint_y=None,
            height=self.height
        )
        self.choice3 = Button(
            text='',
            on_press=lambda instance: self.check_answer(instance.text),
            size_hint_y=None,
            height=self.height
        )
        self.choice4 = Button(
            text='',
            on_press=lambda instance: self.check_answer(instance.text),
            size_hint_y=None,
            height=self.height
        )

        topSecond.add_widget(self.flashCardBox)
        topSecond.add_widget(self.placeHolder)
        bottomSecond.add_widget(self.choice1)
        bottomSecond.add_widget(self.choice2)
        bottomSecond.add_widget(self.choice3)
        bottomSecond.add_widget(self.choice4)

        self.add_widget(topSecond)
        self.add_widget(bottomSecond)

    def update_answer_options(self):
        self.answers = list(Storage.keys())
        unique_answers = set(self.answers)

        if len(unique_answers) >= 3:
            incorrect_options = random.sample(list(unique_answers - {flashCard}), 3)
        else:
            incorrect_options = list(unique_answers - {flashCard})

        position = random.randint(0, len(incorrect_options))
        self.answer_options = (
            incorrect_options[:position]
            + [flashCard]
            + incorrect_options[position:]
        )

        random.shuffle(self.answer_options)
        print(self.answer_options)
        print(unique_answers)

        for i, button in enumerate([self.choice1, self.choice2, self.choice3, self.choice4]):
            if i < len(self.answer_options):
                button.text = Storage[self.answer_options[i]]
            else:
                button.text = ""  

    def on_enter(self):
        self.flashCardBox.text = flashCard
        self.update_answer_options()

    def check_answer(self, selected_answer):
        if selected_answer == Storage[flashCard]:
            content = Label(text="Correct")
            popup = Popup(title="", content=content, size_hint=(None, None), size=(300, 200))
            popup.bind(on_dismiss=self.next_question)
            popup.open()
        else:
            content = Label(text="Incorrect")
            popup = Popup(title="", content=content, size_hint=(None, None), size=(300, 200))
            popup.bind(on_touch_down=popup.dismiss)
            popup.open()

    def next_question(self, instance):
        global flashCard
        flashCard = random.choice(list(Storage.keys()))
        self.update_answer_options()
        self.flashCardBox.text = flashCard

class BevHacks(App):
    def build(self):
        screen_manager = ScreenManager()
        home_screen = HomeScreen(name='home_screen')
        second_screen = SecondScreen(name='second_screen')
        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(second_screen)

        return screen_manager

if __name__ == "__main__":
    BevHacks().run()
