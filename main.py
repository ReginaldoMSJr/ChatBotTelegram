import re
import telebot
import requests
import json

bot = telebot.TeleBot("BOT_KEY")

def BuscarAcao(msg):
    r = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + msg.text.upper().strip() + '&apikey=API_KEY')
    response = json.loads(r.text)
    if(response != {}):
        MensagemAcaoCorreta(msg, response)
    else:
        MensagemAcaoIncorreta(msg)

def NomeUsuario(user):
    if(user.first_name != None and user.first_name != ''):
        nome = user.first_name
        if(user.last_name != None and user.last_name != ''):
            nome = nome + ' ' + user.last_name
        return nome
    else:
        return ''

def MensagemAcaoCorreta(msg, acao):
    bot.send_message(msg.chat.id, acao['Name'] + "\n\n" + acao['Symbol'] + " - " + acao['Exchange'] + "\n\nMin. 52 semanas: $" + acao['52WeekLow'] + "\n\nMax. 52 semanas: $" + acao['52WeekHigh'] + "\n\nPrevisão analistas: $" + acao['AnalystTargetPrice'])

def MensagemAcaoIncorreta(msg):
    bot.send_message(msg.chat.id, "Não encontramos nenhuma ação com o código " + msg.text.upper().strip() + "\n\nDigite um código válido")

def VerificarAcao(msg, resultadoEsperado):
    match = re.match('^[A-Z]{2,4}$', msg.text.upper().strip())
    return (match != None) == resultadoEsperado


@bot.message_handler(commands=['start'])
def MensagemInicial(msg):
    bot.send_message(msg.chat.id, "Olá, " + NomeUsuario(msg.from_user) + "\n\nSomos um ChatBot que faz a busca de algumas informações de ações da bolsa de valores norte americana\n\nFaça o teste digitando o código de uma ação")

@bot.message_handler(func= lambda m: VerificarAcao(m, True))
def Acao(msg):
    BuscarAcao(msg)

@bot.message_handler(func= lambda m: VerificarAcao(m, False))
def MensagemAcaoPadraoErrado(msg):
    bot.send_message(msg.chat.id, "O valor digitado está incorreto!\n\nDigite o código de uma ação da bolsa de valores norte americana composto por 2 a 4 letras\n\nExemplo: NFLX")

bot.infinity_polling(non_stop=True)
