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
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            self.turma_salva = turma + '.txt'
            self.caminho_completo = os.path.join(diretorio_atual, self.turma_salva)
            open(self.caminho_completo, "w")
            
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
            with open(self.caminho_completo, 'a', encoding='utf-8') as arquivo:
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
    def _init_(self, **kwargs):
        super()._init_(**kwargs)

    def EditarTurma(self):
        self.nome_antigo = self.ids.nome_turma.text + '.txt'
        if self.nome_antigo != '.txt':
            self.AddWidget()

    def AddWidget(self):
        for child in self.ids.nome_novo.children:
            if isinstance(child, BotaoVoltar):
                self.ids.nome_novo.remove_widget(self.boxtext)
                self.ids.nome_novo.remove_widget(self.botaoenviar)
        self.botaoenviar = BotaoVoltar(size_hint=(None, None),
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
        self.ids.nome_novo.add_widget(self.botaoenviar)
        self.botaoenviar.bind(on_release=self.on_button_release)
        self.boxtext.focus = True
        Window.bind(on_keyboard=self.confirma)

    def on_button_release(self, instance):
        nome_novo = self.boxtext.text + '.txt'
        if self.nome_antigo and nome_novo:
            if os.path.isfile(self.nome_antigo):
                os.rename(self.nome_antigo, nome_novo)
                self.turma_salva = nome_novo

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
                self.botaoenviar2.unbind(on_release=self.on_button_release)
                self.ids.nome_novo.remove_widget(self.caixa_texto)
                self.ids.nome_novo.remove_widget(self.botaoenviar2)
                self.ids.nome_novo.remove_widget(self.caixa_nome_novo)
                return True
        return False

    def Editar_nome_aluno(self):
        self.nome_antigo = self.ids.nome_turma.text + '.txt'
        if self.nome_antigo != '.txt':
            self.boxt = BoxLayout()
            self.caixa_texto = TextInput(hint_text='Digite o número do aluno',
                                         font_size=30,
                                         size_hint=(1, None),
                                         size=(0, 60),
                                         multiline=False,
                                         pos_hint={'center_x': 0.0, 'center_y': 1})
            self.caixa_nome_novo = TextInput(hint_text='Digite o novo nome do aluno',
                                             font_size=30,
                                             size_hint=(1, None),
                                             size=(0, 60),
                                             multiline=False,
                                             pos_hint={'center_x': 0.0, 'center_y': 1})
            self.botaoenviar2 = BotaoVoltar(size_hint=(None, None),
                                            size=(80, 60),
                                            img='Enviar.png',
                                            pos_hint={'center_x': 0.0, 'center_y': 1})
            self.ids.nome_novo.add_widget(self.caixa_texto)
            self.ids.nome_novo.add_widget(self.caixa_nome_novo)
            self.ids.nome_novo.add_widget(self.botaoenviar2)
            self.botaoenviar2.bind(on_release=self.numero_aluno)

    def numero_aluno(self, instance):
        turma = self.ids.nome_turma.text
        numero = self.caixa_texto.text
        novo_nome = self.caixa_nome_novo.text
        diretorio_atual = os.getcwd()
        caminho_arquivo = os.path.join(diretorio_atual, turma + '.txt')
        encontrado = False
        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                turma_consulta = arquivo.readlines()
            for i, linha in enumerate(turma_consulta):
                aluno_numero, nome = linha.strip().split('-', 1)
                if aluno_numero == numero:
                    turma_consulta[i] = f"{numero}-{novo_nome}\n"
                    encontrado = True
            if encontrado:
                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    arquivo.writelines(turma_consulta)

class AddNotas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.c = 1
        self.verifica = 1
        self.cont = 0
        self.cont1 = 0
        self.valorquestao = list()
        self.dicionario = {}
        self.nota = list()
    def VerificaTurma(self):
        self.turma = self.ids.notas_turma.text
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Muda o diretório de trabalho para o diretório do arquivo
        os.chdir(diretorio_atual)
        # Verifica se o diretório foi mudado corretamente
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
            Window.bind(on_keyboard=self.ConfirmaValor)
            
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
        valor = float(self.boxtext.text)
        if valor != '' and valor !=0:
            self.boxtext.hint_text = f'Digite o valor da {self.c}° questão'
            self.boxtext.text = ''
            self.boxtext.focus = True
            self.valorquestao.append(valor)
        if self.c-1 == self.numero:
            self.boxtext.text = ''
            self.boxtext.hint_text = 'Enviado'
            Window.unbind(on_keyboard = self.ConfirmaValor)
            Window.bind(on_keyboard=self.ConfirmaNotas)
            self.PerguntaNotas()

    def PerguntaNotas(self, *args):
        self.boxpergunta = BoxLayout(padding = (60,0,60,0))
        with open(self.turma+'.txt','r') as arquivo:
            nomes = arquivo.readlines()
        for nome in nomes:
            if '1-' in nome:
                num,name = nome.split('-',1)
        print(name)
        self.perguntanota = TextInput(hint_text = f'Digite a nota da 1° questão de {name}',
                                 font_size = 30,
                                 size_hint= (1, None),
                                 multiline = False,
                                 height= 60)
        self.botaopergunta = BotaoVoltar(img = 'Enviar.png',
                                    size_hint= (None, None),
                                    size = (80,60),
                                    on_release = self.CalculaNotas)
        self.boxpergunta.add_widget(self.perguntanota)
        self.boxpergunta.add_widget(self.botaopergunta)
        self.perguntanota.focus = True
        self.ids.addnotas.add_widget(self.boxpergunta)
    
    def CalculaNotas(self, *args):
        self.cont +=1
        self.cont1 +=1
        arquivo = self.turma+'.txt'
        #Verificador se já foi digitado o número fornecido pelo usuário 
        if self.cont1 >= self.numero:
            self.verifica += 1
            self.cont1 = 0
        #Lê o arquivo em que contêm a turma
        with open(arquivo, 'r') as f:
            turma = f.readlines()
        #Recebe as notas digitadas
        self.nota.append(float(self.perguntanota.text))
        #Faz com que o número máximo de número de chamada seja do tamanho do arquivo
        if self.verifica > len(turma):
            self.verifica = len(turma)

        name = None
        #Procura no arquivo turma o portador do númera da chamada atual
        for c1 in turma:
            if str(self.verifica)+'-' in c1:
                num,name = c1.split('-',1)
        #verifica se existe um nome do aluno
        if name is not None:
            self.perguntanota.text = ''
            self.perguntanota.hint_text = f'Digite a nota da {self.cont1+1}° questão de {name}'
            self.perguntanota.focus = True
        else:
            self.perguntanota.text = ''
            self.perguntanota.hint_text = 'Enviado'
        #Chama a função que vai inserir as notas no arquivo
        if self.cont >= self.numero*len(turma):
            self.Arquivo_for_dicionario(arquivo = arquivo, nota=self.nota)
        
    def Arquivo_for_dicionario(self, arquivo, nota, *args):
        # lendo o arquivo turma
        with open(arquivo, 'r') as f:
            turma = f.readlines()
        aluno = {}
        for id in turma:
            notas = list()
            # Sepera número da chamada e nome do aluno
            num, name = id.split('-',1)
            # Adiciona o nome e número da chamada em um dicionário
            aluno["numero da chamada"] = num
            aluno["nome"] = str(name[:-1])
            for c in range(0, self.numero):
                notas.append(nota[c])
                aluno[f"nota {c+1}"] = nota[c]
            del nota[0:self.numero]
            nota_final = sum(notas)
            aluno["Nota Final"] = nota_final
            #Faz um dicionário do dicionário aluno
            self.dicionario[str(num)] = aluno.copy()
        #Apaga o Arquivo
        with open(arquivo, 'w', encoding='utf-8') as ap:
            ap.write('')
        #Percorre co dicinário
        for c in range(0,len(self.dicionario)):
            cha_name = self.dicionario.get(f"{c+1}", {}).get("numero da chamada") + '-' + self.dicionario.get(f"{c+1}", {}).get("nome")
            #Escreve o número da chamada e o nome do aluno
            with open(arquivo,'a', encoding='utf-8') as r:
                r.write(cha_name + '\n')
            #Percorre o número de questão
            for c1 in range(0,self.numero):
                notas = f'Nota {c1+1}: {self.dicionario.get(f"{c+1}", {}).get(f"nota {c1+1}")}'
                #Adiciona as notas no arquivo
                with open(arquivo, 'a', encoding='utf-8') as n:
                    n.write(notas+'\n')
            n_final = f'Nota Final: {self.dicionario.get(f"{c+1}", {}).get("Nota Final")}'
            #Adiciona a nota final no arquivo
            with open(arquivo, 'a', encoding='utf-8') as nf:
                nf.write(n_final+'\n')

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
        self.cont = 0
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
            self.ids.enviarquestao.trigger_action(duration=0.01)

    def ConfirmaValor(self, window, key, *args):
        if key == 13:
            self.botaoenviar.trigger_action(duration=0.1)
    
    def ConfirmaNotas(self, window, key, *args):
        if key == 13:
            self.botaopergunta.trigger_action(duration=0.1)
    
    def on_pre_leave(self):
        self.c = 0
        self.valorquestao = list()
        self.notas = list()
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_keyboard=self.confirma)
        Window.unbind(on_keyboard=self.ConfirmaBimestre)
        Window.unbind(on_keyboard=self.ConfirmaQuestao)
        Window.unbind(on_keyboard=self.ConfirmaValor)
        Window.unbind(on_keyboard=self.ConfirmaNotas)
        self.ids.notas_turma.text = ''
        self.ids.notas_turma.hint_text = 'Digite o nome da turma'
        self.ids.bimestre.text = ''
        self.ids.bimestre.hint_text = 'Digite o bismestre'
        self.ids.number_question.text = ''
        self.ids.number_question.hint_text = 'Digite número de questões da prova'
        if self.is_layout_in_layout(self.ids.addnotas, self.box):
            self.ids.addnotas.remove_widget(self.box)
        if self.is_layout_in_layout(self.ids.addnotas, self.boxpergunta):
            self.ids.addnotas.remove_widget(self.boxpergunta)
        
    def is_layout_in_layout(self, parent_layout, target_layout):
        if target_layout in parent_layout.children:
            return True
        for child in parent_layout.children:
            if isinstance(child, BoxLayout):
                if self.is_layout_in_layout(child, target_layout):
                    return True
        return False

class Aplicativo(App):
    def build(self):
        return Gerenciador()


Aplicativo().run()
