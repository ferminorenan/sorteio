import random
import pywhatkit as kit
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLineEdit, QHBoxLayout, QLabel, QListWidget, QMessageBox, QComboBox
)

# Função para realizar o sorteio do amigo secreto
def sortear_amigo_secreto(participantes):
    nomes = [p["nome"] for p in participantes]
    random.shuffle(nomes)  # Embaralha os nomes

    sorteio = {}
    for i, participante in enumerate(participantes):
        amigo = nomes[i]
        # Garantir que ninguém tire a si mesmo
        while amigo == participante["nome"]:
            random.shuffle(nomes)
            amigo = nomes[i]
        sorteio[participante["nome"]] = amigo
    
    return sorteio

# Função para enviar mensagens via WhatsApp
def enviar_mensagens(sorteio, participantes, janela):
    for participante in participantes:
        nome = participante["nome"]
        telefone = participante["telefone"]
        amigo = sorteio[nome]
        mensagem = f"Olá {nome}! 🎉 Você tirou {amigo} no amigo secreto! 🤫"
        try:
            kit.sendwhatmsg_instantly(telefone, mensagem, wait_time=10)  # Aguarda 10 segundos
        except Exception as e:
            janela.atualizar_status(f"Erro ao enviar mensagem para {nome} ({telefone}): {e}")

# Classe principal da interface
class SorteadorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sorteador de Amigo Secreto")
        self.setGeometry(100, 100, 500, 400)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Seção para adicionar participantes
        self.participantes_layout = QHBoxLayout()
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do participante")
        
        # Adicionando a ComboBox para selecionar o código do país
        self.codigo_pais_combo = QComboBox()
        self.codigo_pais_combo.addItems(["+55 (Brasil)", "+1 (EUA)", "+44 (Reino Unido)", "+33 (França)", "+49 (Alemanha)"])
        self.codigo_pais_combo.setCurrentText("+55 (Brasil)")  # Valor padrão
        
        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("Telefone (sem o código do país)")
        self.btn_adicionar = QPushButton("Adicionar Participante")
        self.btn_adicionar.clicked.connect(self.adicionar_participante)

        self.participantes_layout.addWidget(QLabel("Nome:"))
        self.participantes_layout.addWidget(self.nome_input)
        self.participantes_layout.addWidget(QLabel("Código País:"))
        self.participantes_layout.addWidget(self.codigo_pais_combo)
        self.participantes_layout.addWidget(QLabel("Telefone:"))
        self.participantes_layout.addWidget(self.telefone_input)
        self.participantes_layout.addWidget(self.btn_adicionar)

        self.layout.addLayout(self.participantes_layout)

        # Lista de participantes
        self.lista_participantes = QListWidget()
        self.layout.addWidget(self.lista_participantes)

        # Botão para realizar o sorteio
        self.btn_sortear = QPushButton("Sortear e Enviar Mensagens")
        self.btn_sortear.clicked.connect(self.sortear_enviar)
        self.layout.addWidget(self.btn_sortear)

        self.setCentralWidget(self.central_widget)
        self.participantes = []

    def adicionar_participante(self):
        nome = self.nome_input.text().strip()
        telefone = self.telefone_input.text().strip()
        codigo_pais = self.codigo_pais_combo.currentText().split()[0]  # Obtém apenas o código, ex: +55

        if not nome or not telefone:
            QMessageBox.warning(self, "Erro", "Nome e telefone são obrigatórios.")
            return

        if any(p["nome"] == nome for p in self.participantes):
            QMessageBox.warning(self, "Erro", f"O participante '{nome}' já foi adicionado.")
            return

        telefone_completo = f"{codigo_pais}{telefone}"
        self.participantes.append({"nome": nome, "telefone": telefone_completo})
        self.lista_participantes.addItem(f"{nome} - {telefone_completo}")
        self.nome_input.clear()
        self.telefone_input.clear()

    def sortear_enviar(self):
        if len(self.participantes) < 2:
            QMessageBox.warning(self, "Aviso", "É necessário pelo menos 2 participantes para realizar o sorteio.")
            return

        try:
            sorteio = sortear_amigo_secreto(self.participantes)
            enviar_mensagens(sorteio, self.participantes, self)
            QMessageBox.information(self, "Sucesso", "Sorteio realizado e mensagens enviadas com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro durante o sorteio ou envio de mensagens: {e}")

    def atualizar_status(self, mensagem):
        # Atualiza a interface com informações sobre o progresso
        QMessageBox.information(self, "Status", mensagem)

# Inicialização da aplicação
def main():
    app = QApplication([])
    sorteador = SorteadorApp()
    sorteador.show()
    app.exec()

if __name__ == "__main__":
    main()
