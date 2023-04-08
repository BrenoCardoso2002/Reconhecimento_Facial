# área das importações:
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
from Programacao.Back_End import Processamento

# classe da interface gráfica da aplicação:
class Interface(QWidget):
    # função de inicialização da classe:
    def __init__(self):
        super().__init__()

        # variaveis da tela:
        self.altura = 1
        self.largura = 1
        self.titulo = 'Reconhecimento facial'

        # variavel relativa ao back-end do programa:
        self.backEnd = ''

        # QLabel do video da camera:
        self.video = QLabel(self)
        self.video.setStyleSheet('background-color: black')
        self.video.move(5, 5)

        # chama a função que calcula e posiciona o video da camera:
        self.tamanhoVideo()

        # QLabel informação do que fazer:
        self.Informacao = QLabel(self)      
        self.Informacao.setText('Não está sendo reconhecido um rosto,\nposicione seu rosto melhor na camera!')
        self.Informacao.setStyleSheet("color: black; font-size: 42px; background-color: yellow")
        self.Informacao.setAlignment(Qt.AlignHCenter)

        # chama a função que calcula e posiciona a label de informação do que fazer:
        self.posicionaInformacao()

        # QLabel de aguarde a valdiação:
        self.label1 = QLabel(self)
        self.label1.setText('Reconhecimento facial\nem:')
        self.label1.setStyleSheet("color: blue; font-size: 32px")
        self.label1.setAlignment(Qt.AlignHCenter)
        
        # chama a função que calcula e posiciona a label1:
        self.posicionaLabel1()

        # QLabel de segundos para reconhecimento:
        self.segundosReconhecimento = QLabel(self)
        self.segundosReconhecimento.setText('10s')
        self.segundosReconhecimento.setStyleSheet("color: blue; font-size: 32px")
        
        # chama a função que calcula e posiciona o segundos para reconhecimento:
        self.posicionasegundosReconhecimento()

        # QLabel Status:
        self.Status = QLabel(self)
        self.Status.setText("Status!!!")
        self.Status.setStyleSheet("color: yellow; font-size: 28px; font-weight: bold")
        self.Status.setAlignment(Qt.AlignHCenter)

        # chama a função que calcula e posiciona o status:
        self.posicionaStatus()

        # instancia a classe do backEnd na variavel:
        self.backEnd = Processamento(self, self.video, self.label1, self.segundosReconhecimento, self.Informacao, self.Status)

        # chama a função que carrega a janela e suas propriedades:
        self.carregarJanela()

    # função que carrega a janela e suas propriedades:
    def carregarJanela(self):
        self.resize(self.largura, self.altura)
        self.setWindowTitle(self.titulo)
        self.showFullScreen()

    # função que calcula e posiciona o video da camera:
    def tamanhoVideo(self):
        # obtem a geometria da tela:
        desktopGeometry = QDesktopWidget().availableGeometry() 

        # tamanho da altura da tela:
        height = desktopGeometry.height()

        # tamanho da largura da tela:
        width = desktopGeometry.width()

        # obtem a posição relativa ao eixoX do video da camera:
        eixoX = self.video.geometry().x()

        # obtem a posição relativa ao eixoY do video da camera:
        eixoY = self.video.geometry().y()

        # calcula a altura do video:
        calcHeight = int(height - eixoY - (height * 0.15)) 

        # calcula a largura do video:
        calcWidth = int((width - eixoX) * 0.75)

        # redimensiona o video da camera:
        self.video.resize(calcWidth, calcHeight)

    # função que calcula e posiciona a label de informação do que fazer:
    def posicionaInformacao(self):
        # obtem a geometria do video:
        videoGeometry = self.video.geometry()

        # obtem o eixoX do video:
        eixoX_video = videoGeometry.x()

        # obtem o eixoY do video:
        eixoY_video = videoGeometry.y()

        # obtem a altura do video:
        height_video = videoGeometry.height()

        # obtem a largura do video:
        width_video = videoGeometry.width()

        # calcula o eixoX da informação:
        eixoY = eixoY_video + height_video + 5

        # move a informação:
        self.Informacao.move(eixoX_video, eixoY)

        # redimensiona a informação:
        self.Informacao.resize(width_video, 100)

    # função que calcula e posiciona a label1:
    def posicionaLabel1(self):
        # obtem a geometria da tela:
        desktopGeometry = QDesktopWidget().availableGeometry() 

        # tamanho da largura da tela:
        width = desktopGeometry.width()

        # tamanho da altura da tela:
        height = desktopGeometry.height()

        # obtem a largura do video da camera:
        width_video = self.video.geometry().width()

        # obtem o eixoX do video da camera:
        eixoX_video = self.video.geometry().x()

        # define a posição do eixoX da label1:
        eixoX = int(width_video + eixoX_video + (width * 0.00366))

        # define a posição do eixoY da label1:
        eixoY = int(height * 0.25)

        # move a label1:
        self.label1.move(eixoX, eixoY)
    
    # função que calcula e posiciona o segundos para reconhecimento:
    def posicionasegundosReconhecimento(self):
        # para calcular a posição dos segundos de validação vai ser usado como base a Label1.
        
        # obtem a geometria da label1:
        label1Geometry = self.label1.geometry()

        # obtem o eixoX da label1:
        eixoX_Label1 = label1Geometry.x()
        
        # obtem o eixoY da label1:
        eixoY_Label1 = label1Geometry.y()

        # calcula eixoX da label de segundos para reconhecimento:
        eixoX = eixoX_Label1 + 140

        # calcula eixoY da label de segundos para reconhecimento:
        eixoY = eixoY_Label1 + 70

        # move a label de segundos para reconhecimento:
        self.segundosReconhecimento.move(eixoX, eixoY)

    # função que calcula e posiciona o status:
    def posicionaStatus(self):
        # para calcular a posição dos segundos de validação vai ser usado como base a label de segundos para reconhecimento.

        # obtem a geometria da label de segundos para reconhecimento:
        sReconhecimentoGeometry = self.segundosReconhecimento.geometry()

        # obtem o eixoX da label de segundos para reconhecimento:
        eixoX_sReconhecimento = sReconhecimentoGeometry.x()

        # obtem o eixoY da label de segundos para reconhecimento:
        eixoY_sReconhecimento = sReconhecimentoGeometry.y()

        # calcula eixoX da label de segundos para reconhecimento:
        eixoX = eixoX_sReconhecimento - 35

        # calcula eixoY da label de segundos para reconhecimento:
        eixoY = eixoY_sReconhecimento + 50

        # move a label de segundos para reconhecimento:
        self.Status.move(eixoX, eixoY)

    # função que ve quando uma tecla é clicada:     
    def keyPressEvent(self, event):
            # verifica se a tecla clicada é o 'esc':
            if event.key() == Qt.Key_Escape:
                # fecha a tela:
                self.close()
