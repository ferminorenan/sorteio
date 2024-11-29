import random
import pywhatkit as kit
import os

# Função para carregar participantes de um arquivo .txt
def carregar_participantes(arquivo):
    participantes = []
    if not os.path.exists(arquivo):
        print(f"Arquivo '{arquivo}' não encontrado. Certifique-se de que ele exista no diretório.")
        return participantes
    
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split(",")  # Formato esperado: Nome,Telefone
            if len(dados) == 2:
                participantes.append({"nome": dados[0], "telefone": dados[1]})
            else:
                print(f"Formato inválido na linha: {linha}")
    
    return participantes

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
def enviar_mensagens(sorteio, participantes):
    for participante in participantes:
        nome = participante["nome"]
        telefone = participante["telefone"]
        amigo = sorteio[nome]
        mensagem = f"Olá {nome}! 🎉 Você tirou {amigo} no amigo secreto! 🤫"
        try:
            print(f"Enviando mensagem para {nome} ({telefone})...")
            kit.sendwhatmsg_instantly(telefone, mensagem, wait_time=10)  # Aguarda 10 segundos
            print(f"Mensagem enviada para {nome}.")
        except Exception as e:
            print(f"Erro ao enviar mensagem para {nome} ({telefone}): {e}")

# Função principal
def main():
    # Solicita login, se necessário
    print("Certifique-se de que o WhatsApp Web esteja configurado e logado.")
    input("Pressione Enter após fazer login no WhatsApp Web para continuar...")

    # Carrega participantes do arquivo
    arquivo_participantes = "participantes.txt"  # Substitua pelo caminho do seu arquivo
    participantes = carregar_participantes(arquivo_participantes)
    
    if not participantes:
        print("Nenhum participante carregado. Verifique o arquivo de entrada.")
        return
    
    # Realiza o sorteio e envia as mensagens
    sorteio = sortear_amigo_secreto(participantes)
    enviar_mensagens(sorteio, participantes)

# Executa o programa
if __name__ == "__main__":
    main()
