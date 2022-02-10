import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pywhatkit

# Opções do driver e url
url = "https://site.sanepar.com.br/mapa-rodizio-abastecimento-curitiba-rmc"

option = Options()
option.headless = True
enviar_msg = False
driver = webdriver.Chrome(options=option)

# Input do Endereço
endereco = input("Digite um endereço (Bairro, rua ou CEP) para consulta: ")

# Perguntar se quer mensagem no whats app e perguntar numero
pergunta_cel = input("Você quer que envie uma mensagem por Whats app? ").lower()

if pergunta_cel == "sim" or pergunta_cel == "s":
    celular_input = input("Digite um numero de celular para enviar a mensagem: ")
    celular = "+5541" + celular_input
    enviar_msg = True
    print(celular)

# Abrir Driver e dormir pra carregar tudo
driver.get(url)
time.sleep(10)

try:

    # Nesse caso, precisa achar o iframe (ignorar o erro no find_element_*, ele reclama mas se você não usa assim ele buga)
    map_iframe = driver.find_element_by_xpath('//iframe')
    driver.switch_to.frame(map_iframe)

    # Achando a caixa de input de endereço, digitando o input, esperando a resposta e clicando nela com arrow down e enter
    input_box = driver.find_element_by_xpath('//input[@id="esri_dijit_Search_0_input"]')
    driver.execute_script("arguments[0].scrollIntoView();", input_box)
    input_box.click()
    input_box.send_keys(endereco)
    time.sleep(5)
    # Caso ENTER não funcione da pra usar o click na Lupa (mas por algum motivo buga no headless = true)
    #search_button = driver.find_element_by_xpath(('//div[@title="Search"]'))
    input_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    input_box.send_keys(Keys.RETURN)

    # Sleep pra garantir que o resultado vai aparecer a tempo
    time.sleep(10)

    # Resultado
    element = driver.find_element_by_xpath('//*[@id="widgets_DistrictLookup_Widget_48"]/div[1]/div[3]')
    resultado = element.get_attribute('outerHTML')

    # Parseando e limpando o resultado
    soup = BeautifulSoup(resultado, 'html.parser')
    texto = soup.find(id="esri_dijit__PopupRenderer_0")
    previsao = texto.get_text()
    p_inicio = "Início"
    p_final = "(madrugada)"
    info_util_start = previsao.index(p_inicio)
    info_util_end = previsao.rindex(p_final) + len(p_final)
    previsao_final = previsao[info_util_start:info_util_end]
    print(previsao_final)

    time.sleep(5)

    # Enviando via Whats App (Por enquanto bugado https://github.com/Ankit404butfound/PyWhatKit/issues/149 e não envia sozinho a msg)
    if enviar_msg:
        pywhatkit.sendwhatmsg_instantly(celular, previsao_final, 15, False, 5)
        time.sleep(5)

finally:

    driver.quit()
