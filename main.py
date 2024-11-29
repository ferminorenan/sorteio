import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Lista dos participantes (substitua pelos nomes dos participantes do canal)
participantes = []

# Função para realizar o sorteio
def sorteio_amigo_secreto(update: Update, context: CallbackContext):
    if len(participantes) < 2:
        update.message.reply_text("É necessário pelo menos 2 participantes para realizar o sorteio.")
        return

    # Sorteio do amigo secreto (sem repetir ninguém)
    sorteio = participantes[:]
    random.shuffle(sorteio)
    
    # Mapeamento dos amigos secretos
    amigos_secretos = {}
    for i in range(len(participantes)):
        # Garantir que ninguém tire a si mesmo
        while sorteio[i] == participantes[i]:
            random.shuffle(sorteio)
        
        amigos_secretos[participantes[i]] = sorteio[i]
    
    # Enviar os resultados para cada participante de forma privada
    for participante in participantes:
        amigo = amigos_secretos[participante]
        context.bot.send_message(chat_id=participante, text=f"Seu amigo secreto é: {amigo}")
    
    update.message.reply_text("O sorteio foi realizado com sucesso! Cada participante receberá uma mensagem com o nome de seu amigo secreto.")

# Função para adicionar participantes ao sorteio
def adicionar_participante(update: Update, context: CallbackContext):
    usuario = update.message.from_user.id  # Identificador único do usuário
    if usuario not in participantes:
        participantes.append(usuario)
        update.message.reply_text(f"Você foi adicionado ao sorteio, {update.message.from_user.first_name}.")
    else:
        update.message.reply_text(f"Você já está no sorteio, {update.message.from_user.first_name}.")

# Função para remover participantes
def remover_participante(update: Update, context: CallbackContext):
    usuario = update.message.from_user.id
    if usuario in participantes:
        participantes.remove(usuario)
        update.message.reply_text(f"Você foi removido do sorteio, {update.message.from_user.first_name}.")
    else:
        update.message.reply_text(f"Você não está no sorteio, {update.message.from_user.first_name}.")

# Função para listar os participantes
def listar_participantes(update: Update, context: CallbackContext):
    if participantes:
        nomes = [update.message.bot.get_chat_member(chat_id=update.message.chat.id, user_id=id).user.full_name for id in participantes]
        update.message.reply_text("Participantes atuais: " + ", ".join(nomes))
    else:
        update.message.reply_text("Não há participantes no sorteio ainda.")

# Função principal para configurar o bot
def main():
    # Substitua 'SEU_TOKEN' pelo token do seu bot
    updater = Updater("TOKEN", use_context=True)
    
    # Adicionando handlers para os comandos
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("iniciar", sorteio_amigo_secreto))
    dp.add_handler(CommandHandler("adicionar", adicionar_participante))
    dp.add_handler(CommandHandler("remover", remover_participante))
    dp.add_handler(CommandHandler("listar", listar_participantes))
    
    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
