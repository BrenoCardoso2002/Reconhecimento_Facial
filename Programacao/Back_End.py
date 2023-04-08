# área das importações:
import cv2
from cvzone.FaceDetectionModule import FaceDetector
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import datetime
import os
from PIL import Image
import face_recognition

# classe da programação por trás da aplicação:
class Processamento():
    # função de inicialização da classe:
    def __init__(self, tela, video, l1, sReconhecimento, informacao, status):
        super().__init__()

        # variaveis da classe relativas a classe anterior:
        self.tela = tela
        self.video = video
        self.l1 = l1
        self.sReconhecimento = sReconhecimento
        self.informacao = informacao
        self.status = status

        # abre a camera padrão:
        self.webCam = cv2.VideoCapture(0)

        # variavel que detecta o rosto:
        self.detectorFace = FaceDetector()

        # timer que atualiza o frame do video:
        timer_video = QTimer(tela)
        timer_video.timeout.connect(self.atualizaFrame)
        timer_video.start(1)

        # variaveis que contarão os segundos que aparecem na tela:
        self.tempoSegundos = 6 # é os segundos que aparecem na tela, define 6 para na hora que aparecer na tela ele ir de 5 a 0.
        self.segundoAux = 0 # esse é os segundos auxiliares pare verificar se houve mudança de segundo.

        # chama a função de nao rosto para deixar os dados padrões e os campos certos invisiveis:
        self.naoRosto()

    # função que atualiza o frame do video da camera:
    def atualizaFrame(self):
        # captura o frame da camera:
        sucesso, frame = self.webCam.read()

        # if que verifica se a camera foi aberta com sucesso:
        if sucesso:
            # redimensiona o video:
            frame = self.tamanhoWebCam(frame) # chama a função que define o tamanho do video da webCam

            # inverte a camera (não é necessário isso, podendo ser essa linha apagada ou comentada!):
            frame = cv2.flip(frame, 1)

            # detecta a face:
            # frame, faces = self.detectorFace.findFaceMesh(frame) # aqui exibe o desenho no rosto.
            frame, faces = self.detectorFace.findFaces(frame, False)

            # if que verifica se há um rosto na camera:
            if faces:
                # se tiver algum rosto na tela, ele verifica se há apenas um rosto na tela:
                if len(faces) == 1:
                    # se tiver um rosto ele verifica se o grau de detecção do rosto passa de 95%:
                    rosto = faces[0]
                    score = round((float(rosto['score'][0]) * 100), 2)
                    if score > 95:
                        self.simRosto()
                        # chama a função que controlas a contagem regressiva da tela:
                        self.contagemRegressiva(frame)
                    else:
                        self.naoRosto()
                else:
                    self.naoRosto()
            else:
                self.naoRosto()

            # converte o frame para um formato RGB:
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # cria o QImage do frame:
            h, w, ch = rgbFrame.shape
            image = QImage(rgbFrame.data, w, h, ch * w, QImage.Format_RGB888)

            # cria o QPixmap do QImage:
            pixmap = QPixmap.fromImage(image)

            # atualiza a label que exibira o frame do video:
            self.video.setPixmap(pixmap)
    
    # função que define o tamanho do video da webCam:
    def tamanhoWebCam(self, frame):
        width = self.video.geometry().width()
        height = self.video.geometry().height()
        resize = cv2.resize(frame, (width, height))
        return resize

    # função de configuração de não ter rosto:
    def naoRosto(self):
        self.l1.setVisible(False)
        self.sReconhecimento.setVisible(False)
        self.status.setVisible(False)
        self.informacao.setVisible(True)
        self.padraoDados()

    # função de configuração de ter rosto:
    def simRosto(self):
        self.l1.setVisible(True)
        self.sReconhecimento.setVisible(True)
        self.informacao.setVisible(False)
    
    # função que define os dados para padrão incial:
    def padraoDados(self):
        self.status.setText("Status!!!")
        self.statusDefault()
        self.tempoSegundos = 6
        self.segundoAux = 0
        self.sReconhecimento.setText(f'{self.tempoSegundos}s')

    # função que faz a contagem regressiva e faz a ação quando chegar no 0:
    def contagemRegressiva(self, frame):
        agora = datetime.datetime.now() # obtem a data atual do sistema:
        segundos = agora.strftime("%S") # obtem o segundo da data atual
        # if que verifica se os segundo auxiliar é diferente do segundo atual:
        if self.segundoAux != segundos: 
            self.segundoAux = segundos
            self.tempoSegundos -= 1
            if self.tempoSegundos > -1:
                self.sReconhecimento.setText(f'{self.tempoSegundos}s')
            if self.tempoSegundos == -1:
                self.reconhecimentoFacial(frame)
    
    # função que define o status como sucesso, ou seja, reconheceu um rosto:
    def statusSucesso(self, texto):
        self.status.setText(texto)
        self.status.setVisible(True)
        self.status.setStyleSheet("color: green; font-size: 28px; font-weight: bold")
    
    # função que define o status como fracasso, ou seja, não reconheceu um rosto:
    def statusFail(self):
        self.status.setText("Não reconhecido!")
        self.status.setVisible(True)
        self.status.setStyleSheet("color: red; font-size: 28px; font-weight: bold")
    
    # função que define o status como padrão, ou seja, antes de reconhecer ou nao um rosto:
    def statusDefault(self):
        self.status.setText("Status!!!")
        self.status.setVisible(False)
        self.status.setStyleSheet("color: yellow; font-size: 28px; font-weight: bold")
    
    # função que passa por todos os arquivos da pasta de imagem (primeira etapa do reconhemento facial):
    def reconhecimentoFacial(self, frame):
        cv2.imwrite('Programacao/Fotos/img_aux.jpg', frame) # salva a foto com um nome auxiliar

        pasta = "Programacao/Fotos"

        arquivos = os.listdir(pasta) # lista todos arquivo da pasta

        for i, arquivo in enumerate(arquivos):
            caminho_completo = os.path.join(pasta, arquivo)
            try:
                with Image.open(caminho_completo) as img:
                    nome_sem_extensao = os.path.splitext(arquivo)[0]
                    # passa por todos os arquivos menos o da foto tirada para o reconhecimento:
                    if nome_sem_extensao != 'img_aux':
                        # se vdd para de ver os arquivos:
                        print(caminho_completo)
                        # aqui verifica se achou um rosto "parecido":
                        if self.compara_tudo(caminho_completo):
                            self.statusSucesso(nome_sem_extensao)
                            break

            except:
                pass
    
            # Verifique se este é o último arquivo na lista e exibe o status fal
            if i == len(arquivos) - 1:
                # Este é o último arquivo na lista
                self.statusFail()     

    # compara a foto tirada com as da pasta:
    def compara_tudo(self, caminho):
        image_of_person_1 = face_recognition.load_image_file("Programacao/Fotos/img_aux.jpg")
        image_of_person_2 = face_recognition.load_image_file(caminho)

        # Encontre as codificações dos rostos nas imagens
        person_1_face_encoding = face_recognition.face_encodings(image_of_person_1)[0]
        person_2_face_encoding = face_recognition.face_encodings(image_of_person_2)[0]

        # Compare as codificações dos rostos e calcule a porcentagem de semelhança
        face_distances = face_recognition.face_distance([person_1_face_encoding], person_2_face_encoding)
        similarity = 1 - face_distances[0]

        porcentagem = round(similarity*100, 2)

        # se grau de semelhança for maior que 90% retorna vdd:
        if int(porcentagem) >= 75:
            return True