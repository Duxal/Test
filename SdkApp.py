#from kivy.app import App
#from kivy.lang import Builder

#GUI = Builder.load_file('teste.kv')

#class MeuApp(App):
#    def build(self):
#        return GUI
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock

from Sdk_jg import maker

kivy.require('2.0.0')

class SudokuApp(App):
    def build(self):
        # Criação da grade de Sudoku
        self.puzzle, self.solu = maker('medio')  # Dificuldade padrão: médio
        self.soluOn = False
        self.selected_cell = None

        self.grid = GridLayout(cols=9,
                               rows=9,
                               padding=20,
                               spacing=5,
                               size_hint=(None, None),
                               size=(600, 600),
                               pos_hint={'center_x': 0.5, 'center_y': 0.55}
                               )


        # Criar botões
        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                btn = Button(font_size=30, size_hint=(None, None), width=55, height=55,
                             background_normal='', background_color=(1, 1, 1, 1))
                btn.bind(on_press=self.cell_pressed)
                btn.pos_hint = {'center': (col / 9, row / 9)}
                row_cells.append(btn)
                self.grid.add_widget(btn)
            self.cells.append(row_cells)

        # Layout principal
        self.main_layout = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.grid)

        # adicionar o timer
        self.timer_seconds = 0  # Armazena o tempo decorrido em segundos
        self.timer_label = Label(text="Tempo: 00:00", font_size=24, size_hint_y=0.1)  # Label do tempo
        self.main_layout.add_widget(self.timer_label)

        # Botões de controle (resolver, novo jogo e dificuldade)
        control_layout = BoxLayout(size_hint_y=0.1)

        solve_btn = Button(text="Resolver", on_press=self.show_solution)
        #new_game_btn = Button(text="New Game", on_press=self.new_game)

        # Botões de dificuldade
        difficulty_layout = BoxLayout(size_hint_y=0.1)
        easy_btn = Button(text="Fácil", on_press=lambda instance: self.change_difficulty('facil'))
        medium_btn = Button(text="Médio", on_press=lambda instance: self.change_difficulty('medio'))
        hard_btn = Button(text="Difícil", on_press=lambda instance: self.change_difficulty('dificil'))

        difficulty_layout.add_widget(easy_btn)
        difficulty_layout.add_widget(medium_btn)
        difficulty_layout.add_widget(hard_btn)

        control_layout.add_widget(solve_btn)
        #control_layout.add_widget(new_game_btn)

        self.main_layout.add_widget(control_layout)
        self.main_layout.add_widget(difficulty_layout)

        self.update_grid()  # Atualiza a grade com os números do Sudoku

        return self.main_layout

    def update_grid(self):
        """Atualiza a grade com os números e solução"""
        for row in range(9):
            for col in range(9):
                btn = self.cells[row][col]
                num = self.puzzle[row][col]

                if type(num) == str and num != ' ' and self.soluOn:  # Se o numero for do tipo string
                    btn.text = str(self.solu[row][col])  # Mostrar a solução
                    btn.color = (0, 1, 0, 1)  # Verde para soluções
                elif type(num) == str and num != ' ':
                    btn.text = num  # Numero de entrada
                    btn.color = (0, 0, 1, 1)  # Azul para entradas
                elif type(num) == int and num != ' ':
                    btn.text = str(num)  # Mostrar numeros estáticos
                    btn.color = (0, 0, 0, 1)  # Preto para numeros estáticos
                else:
                    btn.text = ""

    def show_solution(self, instance):
        """Exibe as soluções de Sudoku"""
        self.soluOn = True
        self.update_grid()

    def new_game(self, instance):
        """Inicia um novo jogo"""
        self.puzzle, self.solu = maker(self.current_difficulty)  # Usa a dificuldade atual
        self.soluOn = False
        self.update_grid()

    def change_difficulty(self, difficulty):
        """Altera a dificuldade e gera um novo jogo"""
        self.current_difficulty = difficulty
        self.new_game(None)  # Gera um novo jogo com a nova dificuldade

    def cell_pressed(self, instance):
        """Ação ao pressionar um quadrado"""
        if instance.text == "":
            self.selected_cell = instance
            self.open_input_popup()

    def open_input_popup(self):
        """Abre um popup para inserir um número"""
        input_popup = Popup(title="Insira um valor",
                            size_hint=(None, None), size=(400, 400))
        popup_layout = BoxLayout(orientation='vertical')

        # Campo de entrada de texto
        text_input = TextInput(font_size=40, multiline=False, size_hint_y=1)
        popup_layout.add_widget(text_input)

        # Botões numéricos
        num_layout = GridLayout(cols=3, size_hint_y=1)
        for num in range(1, 10):
            button = Button(text=str(num), on_press=lambda instance, n=num: self.fill_value(n, text_input, input_popup))
            num_layout.add_widget(button)
        clear_btn = Button(text="Sair", on_press=lambda instance: self.clear_value(text_input, input_popup))
        num_layout.add_widget(clear_btn)

        popup_layout.add_widget(num_layout)
        input_popup.content = popup_layout
        input_popup.open()

    def fill_value(self, num, text_input, popup):
        """Preenche o número na célula selecionada"""
        if self.selected_cell:
            self.selected_cell.text = str(num)
            self.selected_cell.color = (0, 0, 1, 1)
            row, col = self.get_cell_position(self.selected_cell)
            self.puzzle[row][col] = str(num)  # Atualiza com o valor inserido
        text_input.text = ""  # Limpa o campo de entrada
        popup.dismiss()  # Fecha o popup

    def clear_value(self, text_input, popup):
        """Limpa a célula selecionada"""
        if self.selected_cell:
            self.selected_cell.text = ""
            row, col = self.get_cell_position(self.selected_cell)
            self.puzzle[row][col] = ' '  # Limpa a célula do puzzle
        text_input.text = ""  # Limpa o campo de entrada
        popup.dismiss()  # Fecha o popup

    def get_cell_position(self, cell):
        """Retorna a posição da célula na grade"""
        for row in range(9):
            if cell in self.cells[row]:
                return row, self.cells[row].index(cell)
        return None, None


    def update_timer(self, dt):
        self.timer_seconds += 1
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.text = f"Tempo: {minutes:02}:{seconds:02}"

    def new_game(self, instance):
        """Inicia um novo jogo e reseta o tempo"""
        self.puzzle, self.solu = maker(self.current_difficulty)
        self.soluOn = False
        self.timer_seconds = 0  # Reseta o timer
        self.timer_label.text = "Tempo: 00:00"

        Clock.unschedule(self.update_timer)  # Para o timer antigo
        Clock.schedule_interval(self.update_timer, 1)  # Inicia um novo timer

        self.update_grid()

if __name__ == "__main__":
    app = SudokuApp()
    app.current_difficulty = 'medio'  # Dificuldade padrão
    app.run()
