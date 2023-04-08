# área das importações:
import sys
from PyQt5.QtWidgets import QApplication
from Programacao.Front_End import Interface

# if de inicialização:
if __name__ == '__main__':
    # cria uma instância da aplicação:
    app = QApplication(sys.argv)

    # cria uma instância da classe que cuida da interface gráfica da aplicação:
    janela = Interface()

    # exibe a interface gráfica:
    janela.show()

    # executa a aplicação e aguarda até que ela seja encerrada:
    sys.exit(app.exec())
