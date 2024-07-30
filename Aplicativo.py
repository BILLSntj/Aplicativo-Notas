from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import os


class Botao(ButtonBehavior, Label):
    cor = ListProperty([0.7, 0.5, 0.1, 1])
    cor_press = ListProperty([0.3, 0.3, 0.3, 1])
    loc = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(Botao, self).__init__(**kwargs)

    def on_pos(self, *args):
        Clock.schedule_once(self.Atualizar, 0)

    def on_size(self, *args):
        Clock.schedule_once(self.Atualizar, 0)

    def on_press(self, *args):
        self.cor, self.cor_press = self.cor_press, self.cor

    def on_release(self, *args):
        self.cor_press, self.cor = self.cor, self.cor_press

    def on_cor(self, *args):
        Clock.schedule_once(self.Atualizar, 0)

    def Atualizar(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height, self.height),
                    pos=self.pos)
            Ellipse(size=(self.height, self.height),
                    pos=(self.x+self.width-self.height, self.y))
            Rectangle(size=(self.width-self.height, self.height),
                      pos=(self.x+self.height/2.0, self.y))


class BotaoVoltar(ButtonBehavior, Label):
    cor = ListProperty([1, 1, 1, 1])
    cor_press = ListProperty([0.1, 0.1, 0.1, 1])
    img = StringProperty('')

    def __init__(self, **kwargs):
        super(BotaoVoltar, self).__init__(**kwargs)

    def on_pos(self, *args):
        Clock.schedule_once(self.Atualizar, 0)

    def on_size(self, *args):
        Clock.schedule_once(self.Atualizar, 0)

    def on_press(self, *args):
        self.cor, self.cor_press = self.cor_press, self.cor

    def on_release(self, *args):
        self.cor_press, self.cor = self.cor, self.cor_press

    def Atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height, self.height),
                    pos=(self.pos),
                    source=self.img)


class Gerenciador(ScreenManager):
    pass


class Menu(Screen):
    pass


class NovaTurma(Screen):
    def __init__(self, **kwargs):
        super(NovaTurma, self).__init__(**kwargs)
        self.turma_salva = '0'
        self.number_alunos = 0
        self.c = 0

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard=self.confirma)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def confirma(self, window, key, *args):
        if key == 13:
            self.ids.enviar1.trigger_action(duration=0.1)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_keyboard=self.confirma)
        Window.unbind(on_keyboard=self.confirma_alunos)
        Window.unbind(on_keyboard=self.confirma_nomes)
        self.ids.Turma.hint_text = 'Digite o Nome da turma'
        self.ids.alunos.hint_text = 'Digite o número de alunos'
        self.ids.nomes.hint_text = 'Digite o nome do 1° aluno da chamada'
        self.c = 0

    def confirma_alunos(self, window, key, *arg):
        if key == 13:
            self.ids.enviar2.trigger_action(duration=0.1)

    def confirma_nomes(self, window, key, *ags):
        if key == 13:
            self.ids.enviar3.trigger_action(duration=0.1)

    def CriarTurma(self):
        turma = self.ids.Turma.text
        number_alunos = self.ids.alunos.text
        if turma != '':
            self.ids.Turma.text = ''
            self.ids.Turma.hint_text = 'Enviado'
            self.ids.alunos.focus = True
            Window.unbind(on_keyboard=self.confirma)
            Window.bind(on_keyboard=self.confirma_alunos)
            open(turma + '.txt', "w")
            self.turma_salva = turma
        if number_alunos != '':
            self.ids.alunos.text = ''
            self.ids.alunos.hint_text = 'Enviado'
            self.ids.nomes.focus = True
            Window.unbind(on_keyboard=self.confirma_alunos)
            Window.bind(on_keyboard=self.confirma_nomes)
            self.number_alunos = int(number_alunos)

    def Alunos(self):
        self.c += 1
        nomes = self.ids.nomes.text
        if nomes != '':
            self.ids.nomes.text = ''
            self.ids.nomes.hint_text = f'Digite o nome do {
                self.c+1}° aluno da chamada'
            self.ids.nomes.focus = True
            with open(self.turma_salva + '.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(str(self.c) + '-' + nomes + '\n')
        if self.c == self.number_alunos:
            self.ids.nomes.text = ''
            self.ids.nomes.hint_text = 'Enviado'

    def Consultar_Outra_Turma(self):
        self.ids.Turma.text = ''
        self.ids.alunos.text = ''
        self.ids.nomes.text = ''
        self.ids.Turma.hint_text = 'Digite o Nome da turma'
        self.ids.alunos.hint_text = 'Digite o número de alunos'
        self.ids.nomes.hint_text = 'Digite o nome do 1° aluno da chamada'
        self.ids.Turma.focus = True
        Window.unbind(on_keyboard=self.confirma_nomes)
        Window.bind(on_keyboard=self.confirma)


class Consultar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard=self.confirma)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def confirma(self, window, key, *args):
        if key == 13:
            self.ids.enviar4.trigger_action(duration=0.1)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_keyboard=self.confirma)
        self.existe_label(self.ids.box_secundario)
        self.ids.consulta_turma.text = ''
        self.ids.consulta_turma.hint_text = 'Digite o nome da turma'
        for widget in range(len(self.ids.box.children)):
            self.ids.box.remove_widget(self.ids.box.children[0])

    def Mostrar(self):
        turma = self.ids.consulta_turma.text
        diretorio_atual = os.getcwd()
        caminho_arquivo = os.path.join(diretorio_atual, turma+'.txt')
        if os.path.isfile(caminho_arquivo):
            with open(turma+'.txt', 'r', encoding='utf-8') as arquivo:
                turma_consulta = arquivo.readlines()
            for c in range(0, len(turma_consulta)-1):
                x = len(turma_consulta[c+1])
                if x < len(turma_consulta[c]):
                    x = len(turma_consulta[c])
            for aluno in turma_consulta:
                label = Label(
                    text=f"{aluno[:-1]}:",
                    halign='left',
                    valign='middle',
                    color=[1, 1, 1, 1],
                    pos=(0, 0),
                    size_hint=(1, None),
                    size=(self.x, 60))
                self.ids.box.add_widget(label)
        else:
            self.ids.box_secundario.add_widget(Label(
                text="Nome de turma inválido! Consulte outra turma",
                color=[1, 0, 0, 1],
                font_size=30))

    def Consultar_Nova_turma(self):
        self.ids.consulta_turma.text = ''
        self.ids.consulta_turma.hint_text = 'Digite o nome da turma'
        self.ids.consulta_turma.focus = True
        self.existe_label(self.ids.box_secundario)
        for widget in range(len(self.ids.box.children)):
            self.ids.box.remove_widget(self.ids.box.children[0])

    def existe_label(self, layout):
        for child in layout.children:
            if isinstance(child, Label):
                layout.remove_widget(child)
                return True
        return False


class Editar(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)

    def EditarTurma(self):
        self.nome_antigo = self.ids.nome_turma.text + '.txt'
        if self.nome_antigo != '.txt':
            self.AddWidget()

    def AddWidget(self):
        for child in self.ids.nome_novo.children:
            if isinstance(child, BotaoVoltar):
                self.ids.nome_novo.remove_widget(self.boxtext)
                self.ids.nome_novo.remove_widget(self.botaoenviar1)
        self.botaoenviar1 = BotaoVoltar(size_hint=(None, None),
                                       size=(80, 60),
                                       img='Enviar.png',
                                       pos_hint={'center_x': 0.0, 'center_y': 1})
        self.boxtext = TextInput(hint_text='Digite o novo nome da turma',
                                 font_size=30,
                                 size_hint=(1, None),
                                 size=(0, 60),
                                 multiline=False,
                                 pos_hint={'center_x': 0.0, 'center_y': 1})
        self.ids.nome_novo.add_widget(self.boxtext)
        self.ids.nome_novo.add_widget(self.botaoenviar1)
        self.botaoenviar1.bind(on_release=self.on_button_release)
        self.boxtext.focus = True
        Window.bind(on_keyboard=self.confirma)

    def AddWidgetaluno(self):
        for child in self.ids.nome_novo.children:
            if isinstance(child, BotaoVoltar):
                self.ids.nome_novo.remove_widget(self.boxtext2)
                self.ids.nome_novo.remove_widget(self.botaoenviar1)
        self.box = BoxLayout(orientation='vertical', padding=(60, 60, 60, 500))
        self.botaoenviar1 = BotaoVoltar(size_hint=(None, None),
                                        size=(80, 60),
                                        img='Enviar.png',
                                        pos_hint={'center_x': 0.0, 'center_y': 1})
        self.boxtext2 = TextInput(hint_text='Digite o novo nome da turma',
                                  font_size=30,
                                  size_hint=(1, None),
                                  size=(0, 60),
                                  multiline=False,
                                  padding=(60, 60, 60, 60),
                                  pos_hint={'center_x': 0.0, 'center_y': 1})
        self.box.add_widget(self.botaoenviar1)
        self.box.add_widget(self.boxtext2)
        self.botaoenviar1.bind(on_release=self.on_button_release)
        self.boxtext2.focus = True
        Window.bind(on_keyboard=self.confirma)

        self.botaoenviar3 = BotaoVoltar(size_hint=(None, None),
                                        size=(80, 60),
                                        img='Enviar.png',
                                        pos_hint={'center_x': 0.0, 'center_y': 1})
        self.boxtext4 = TextInput(hint_text='Digite o novo nome da turma',
                                  font_size=30,
                                  size_hint=(1, None),
                                  size=(0, 60),
                                  multiline=False,
                                  pos_hint={'center_x': 0.0, 'center_y': 1})
        self.ids.nome_novo.add_widget(self.boxtext4)
        self.ids.nome_novo.add_widget(self.botaoenviar3)
        self.botaoenviar3.bind(on_release=self.on_button_release)
        self.boxtext4.focus = True
        Window.bind(on_keyboard=self.confirma)

    def on_button_release(self, instance):
        nome_novo = self.boxtext.text+'.txt'
        os.rename(self.nome_antigo, nome_novo)

    def confirma(self, window, key, *args):
        if key == 13:
            self.botaoenviar.trigger_action(duration=0.1)

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self):
        for child in self.ids.nome_novo.children:
            if isinstance(child, BotaoVoltar):
                self.botaoenviar.unbind(on_release=self.on_button_release)
                self.ids.nome_novo.remove_widget(self.boxtext)
                self.ids.nome_novo.remove_widget(self.botaoenviar)
                return True
        return False

    def Editar_nome_aluno(self):
        self.nome_antigo = self.ids.nome_turma.text + '.txt'
        if self.nome_antigo != '.txt':
            self.AddWidgetaluno()
    

class Editar_Turma(Screen):
    pass


class Editar_Aluno(Screen):
    pass

class AddNotas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.c = 1
        self.valorquestao = list()
    def VerificaTurma(self):
        self.turma = self.ids.notas_turma.text
        diretorio_atual = os.getcwd()
        caminho_arquivo = os.path.join(diretorio_atual, self.turma+'.txt')
        if os.path.isfile(caminho_arquivo):
            self.ids.bimestre.focus = True
            self.ids.notas_turma.text = ''
            self.ids.notas_turma.hint_text = 'Enviado'
            Window.unbind(on_keyboard = self.confirma)
            Window.bind(on_keyboard = self.ConfirmaBimestre)
        else:
            self.Atencao()
    
    def Atencao(self, *args):
        box = BoxLayout(orientation='vertical',
                        padding=(10, 10, 0, 0),
                        spacing=10)
        botoes = BoxLayout(padding=10,
                           spacing=10)

        self.pop = Popup(title='Turma inválida! Deseja digitar outra turma?',
                         content=box,
                         size_hint=(None, None),
                         size=(300, 230))

        sim = Botao(text='Sim',
                    color=(0, 0, 0, 1),
                    cor=(0.3, 0.7, 0.3, 1),
                    size_hint=(0.3, None),
                    height=40,
                    on_release=self.RespostaSim)
        nao = Botao(text='Não',
                    color=(0, 0, 0, 1),
                    cor=(0.7, 0.2, 0.2, 1),
                    size_hint=(0.3, None),
                    height=40,
                    on_release=self.RespostaNao)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='Atenção.png')

        box.add_widget(atencao)
        box.add_widget(botoes)
        self.pop.open()

    def VerificaBimestre(self,*args):
        self.bim = self.ids.bimestre.text
        if self.bim != '1' and self.bim != '2' and self.bim != '3' and self.bim != '4':
            self.AtencaoBim()
        else:
            self.ids.bimestre.text = ''
            self.ids.bimestre.hint_text = 'Enviado'
            self.ids.number_question.focus = True
            Window.unbind(on_keyboard=self.ConfirmaBimestre)
            Window.bind(on_keyboard=self.ConfirmaQuestao)
    
    def AtencaoBim(self, *args):
        box = BoxLayout(orientation='vertical',
                        padding=(20, 20, 20, 10),
                        spacing=20)
        self.popbim = Popup(title='Bimestre Inválido! Digite outro',
                            content=box,
                            size_hint=(None, None),
                            size=(300, 250))
        ok = Botao(text='ok',
                   color=(0, 0, 0, 1),
                   cor=(0.3, 0.7, 0.3, 1),
                   size_hint=(1, None),
                   height=40,
                   on_release=self.RespostaOk)
        atencao = Image(source='Atenção.png')

        box.add_widget(atencao)
        box.add_widget(ok)

        self.popbim.open()

    def VerificaQuestao(self, *args):
        self.num_ques = self.ids.number_question.text
        try:
            self.numero = int(self.num_ques)
        except ValueError:
            self.AtencaoQuestao()
            return
        
        if self.numero >= 0:
            self.ids.number_question.text = ''
            self.ids.number_question.hint_text = 'Enviado'
            Window.unbind(on_keyboard = self.ConfirmaQuestao)
            Window.bind(on_keyboard = self.ConfirmaValor)
            self.Widgets()
        else:
            self.AtencaoQuestao()
    
    def Widgets(self, *args):
        self.box = BoxLayout(padding = (60,0,60,0))
        self.boxtext = TextInput(hint_text = 'Digite o valor da 1° questão',
                            size_hint= (1, None),
                            height = 60,
                            multiline = False,
                            font_size = 30)
        self.botaoenviar = BotaoVoltar(img = 'Enviar.png',
                                  size_hint= (None, None),
                                  size = (80,60),
                                  on_release = self.SalvarValores)
        self.box.add_widget(self.boxtext)
        self.box.add_widget(self.botaoenviar)
        self.ids.addnotas.add_widget(self.box)
        self.boxtext.focus = True
    
    def SalvarValores(self, *args):
        self.c +=1
        valor = self.boxtext.text
        if valor != '' and valor !=0:
            self.boxtext.hint_text = f'Digite o valor da {self.c} questão'
            self.boxtext.text = ''
            self.boxtext.focus = True
            self.valorquestao.append(valor)
        if self.c-1 == self.numero:
            self.boxtext.text = ''
            self.boxtext.hint_text = 'Enviado'

    def AtencaoQuestao(self, *args):
        box = BoxLayout(orientation= 'vertical',
                        padding = (30,20,30,20),
                        spacing = 10)
        self.popques = Popup(title = 'Número inválido! Digite outro',
                             content = box,
                             size_hint= (None, None),
                             size = (300,250))
        atencao = Image(source = 'Atenção.png')
        ok = Botao(text = 'ok',
                   color = (0,0,0,1),
                   cor = (0.3,0.7,0.3,1),
                   size_hint= (1, None),
                   height = 40,
                   on_release = self.RespostaOkq)
        box.add_widget(atencao)
        box.add_widget(ok)
        self.popques.open()

    def RespostaOkq(self, *args):
        self.popques.dismiss()
        self.ids.number_question.text = ''
        self.ids.number_question.hint_text = 'Digite o número de questões da prova'
        self.ids.number_question.focus = True
        Window.bind(on_keyboard=self.ConfirmaQuestao)
    
    def RespostaOk(self,*args):
        self.popbim.dismiss()
        self.ids.bimestre.text = ''
        self.ids.bimestre.hint_text = 'Digite o bimestre'
        self.ids.bimestre.focus = True

    def RespostaSim(self,*args):
        self.pop.dismiss()
        self.ids.notas_turma.focus = True
        self.ids.notas_turma.text = ''
        self.ids.notas_turma.hint_text = 'Digite o nome da turma'
        Window.bind(on_keyboard=self.confirma)
    def RespostaNao(self,*args):
        App.get_running_app().root.current = 'menu'
        self.pop.dismiss()

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard = self.confirma)
        self.ids.notas_turma.focus = True
    
    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True
    
    def confirma(self, window, key, *args):
        if key == 13:
            self.ids.enviarturma.trigger_action(duration=0.1)

    def ConfirmaBimestre(self, window, key, *args):
        if key == 13:
            self.ids.enviarbimestre.trigger_action(duration=0.1)

    def ConfirmaQuestao(self, window, key, *args):
        if key == 13:
            self.ids.enviarquestao.trigger_action(duration=0.1)

    def ConfirmaValor(self, window, key, *args):
        if key == 13:
            self.botaoenviar.trigger_action(duration=0.1)
    
    def on_pre_leave(self):
        self.c = 0
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_keyboard=self.confirma)
        Window.unbind(on_keyboard=self.ConfirmaBimestre)
        Window.unbind(on_keyboard=self.ConfirmaQuestao)
        self.ids.notas_turma.text = ''
        self.ids.notas_turma.hint_text = 'Digite o nome da turma'
        self.ids.bimestre.text = ''
        self.ids.bimestre.hint_text = 'Digite o bismestre'
        self.ids.number_question.text = ''
        self.ids.number_question.hint_text = 'Digite número de questões da prova'
        self.ids.addnotas.remove_widget(self.box)

class Aplicativo(App):
    def build(self):
        return Gerenciador()


Aplicativo().run()
