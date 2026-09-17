from machine import Pin
import time

time.sleep(0.1)  #espera a USB (Monitor Serial) ficar pronta

#saida: LEDs
led_verde = Pin(13, Pin.OUT)
led_amarelo = Pin(14, Pin.OUT)
led_vermelho = Pin(15, Pin.OUT)

#rntrada: botao (pull-up interno -> solto = 1, pressionado = 0)
botao = Pin(16, Pin.IN, Pin.PULL_UP)

# Potencia nominal do carregador
POTENCIA_CARREGADOR_W = 2000

#memoria: as tres situacoes do enunciado
SITUACOES = (
    # (titulo, geracao em W, consumo em W)
    ("SITUACAO 1 - ENERGIA SUFICIENTE", 4000, 1500),
    ("SITUACAO 2 - ENERGIA LIMITADA", 1800, 1500),
    ("SITUACAO 3 - ENERGIA INSUFICIENTE", 1000, 1800),
)


def determinar_status(disponivel):
    if disponivel >= POTENCIA_CARREGADOR_W:
        return "RECARGA AUTORIZADA", led_verde, "VERDE"
    if disponivel > 0:
        return "RECARGA REDUZIDA", led_amarelo, "AMARELO"
    return "RECARGA BLOQUEADA", led_vermelho, "VERMELHO"


def potencia_liberada(disponivel):
    if disponivel <= 0:
        return 0
    if disponivel > POTENCIA_CARREGADOR_W:
        return POTENCIA_CARREGADOR_W
    return disponivel


def acender_apenas(led_ligado):
    for led in (led_verde, led_amarelo, led_vermelho):
        led.value(led is led_ligado)


def binario_16(valor):
    """Os 16 bits que um registrador guardaria (negativo = complemento de 2)."""
    bits = "{:016b}".format(valor & 0xFFFF)
    return " ".join(bits[i:i + 4] for i in range(0, 16, 4))


def hexadecimal_16(valor):
    return "0x{:04X}".format(valor & 0xFFFF)


def mostrar_sessao(titulo, geracao, consumo):
    disponivel = geracao - consumo                    
    status, led, cor = determinar_status(disponivel)
    acender_apenas(led)                               

    print("=" * 40)                                  
    print(titulo)
    print("=" * 40)
    print("GERACAO:", geracao, "W")
    print("CONSUMO:", consumo, "W")
    print("DISPONIVEL:", disponivel, "W")
    print("LIBERADO P/ RECARGA:", potencia_liberada(disponivel), "W de",
          POTENCIA_CARREGADOR_W, "W")
    print()
    print("STATUS:")
    print(status)
    print("LED ACESO:", cor)
    print()
    print("DADO 'DISPONIVEL' EM 16 BITS COM SINAL:")
    print("DECIMAL:", disponivel)
    if disponivel < 0:
        print("BINARIO:", binario_16(disponivel), "(complemento de 2)")
    else:
        print("BINARIO:", binario_16(disponivel))
    print("HEXADECIMAL:", hexadecimal_16(disponivel))
    print()


def botao_clicado():
    if botao.value() == 1:
        return False
    time.sleep_ms(30)              #deixa a trepidacao (bounce) passar
    if botao.value() == 1:
        return False
    while botao.value() == 0:      #so conta o clique depois de soltar
        time.sleep_ms(10)
    return True


#prrograma principal
print("CHARGEGRID - CONTROLE INTELIGENTE DE SESSAO DE RECARGA")
print("Pressione o botao para passar para a proxima situacao.")
print()

indice = 0
mostrar_sessao(*SITUACOES[indice])

while True:
    if botao_clicado():
        indice = (indice + 1) % len(SITUACOES)
        mostrar_sessao(*SITUACOES[indice])
    time.sleep_ms(20)