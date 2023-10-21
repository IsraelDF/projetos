import pandas as pd
import requests

# Passo 1: Baixar e unir os dados de 2021, 2022 e 2023
url = "http://dados.recife.pe.gov.br/dataset/perfil-das-pessoas-vacinadas-covid-19"
response = requests.get(url)
data = response.json()

# Suponha que os dados estejam em uma lista chamada "data"
# Você pode precisar explorar o JSON para encontrar os dados corretos

# Passo 2: Criar um DataFrame do Pandas com os dados
df = pd.DataFrame(data)

# Passo 3: Limpar e transformar os dados

# Passo 4: Calcular o número total de pessoas vacinadas
total_vacinados = len(df)

# Passo 5: Encontrar a cidade que tomou mais doses da vacina CORONAVAC
cidade_mais_doses = df[df['Nome da Vacina'] == 'CORONAVAC - SINOVAC (BUTANTAN)']['Nome do Município'].value_counts().idxmax()

# Passo 6: Criar a coluna 'tipo_faixa_etaria'
# Aqui, você pode usar o método .apply() para criar a nova coluna com base na idade
def categorizar_faixa_etaria(idade):
    if 3 <= idade <= 12:
        return 'Crianças'
    elif 13 <= idade <= 19:
        return 'Adolescentes'
    elif 20 <= idade <= 39:
        return 'Jovens adultos'
    elif 40 <= idade <= 59:
        return 'Adultos de meia-idade'
    else:
        return 'Idosos'

df['tipo_faixa_etaria'] = df['Idade'].apply(categorizar_faixa_etaria)

# Passo 7: Criar a coluna 'regiao'
# Você pode usar o método .apply() novamente para criar a nova coluna com base na cidade
def categorizar_regiao(cidade):
    metropolitana = ["Recife", "Olinda", "Jaboatão dos Guararapes", "Paulista", "Camaragibe", "São Lourenço da Mata", "Abreu e Lima", "Igarassu", "Cabo de Santo Agostinho"]
    return "Metropolitana" if cidade in metropolitana else "Interior"

df['regiao'] = df['Nome do Município'].apply(categorizar_regiao)

# Passo 8: Contar pessoas vacinadas por 'regiao' e 'tipo_faixa_etaria'
contagem = df.groupby(['regiao', 'tipo_faixa_etaria']).size().reset_index(name='Total')

# Passo 9: Calcular idade média por 'regiao' e 'tipo_faixa_etaria'
idade_media = df.groupby(['regiao', 'tipo_faixa_etaria'])['Idade'].mean().reset_index(name='Idade Média')

# Passo 10: Encontrar a vacina mais administrada por 'regiao' e 'tipo_faixa_etaria'
vacina_mais_administrada = df.groupby(['regiao', 'tipo_faixa_etaria'])['Nome da Vacina'].agg(pd.Series.mode).reset_index(name='Vacina Mais Administrada')

# Passo 11: Calcular a proporção de homens e mulheres vacinados por 'regiao' e 'tipo_faixa_etaria'
proporcao_sexo = df.groupby(['regiao', 'tipo_faixa_etaria', 'Sexo']).size().unstack().reset_index()
proporcao_sexo['Proporção de Homens'] = proporcao_sexo['M'] / (proporcao_sexo['M'] + proporcao_sexo['F'])
proporcao_sexo['Proporção de Mulheres'] = proporcao_sexo['F'] / (proporcao_sexo['M'] + proporcao_sexo['F'])

# Agora você pode acessar os resultados e exibi-los
print("Número total de pessoas vacinadas:", total_vacinados)
print("Cidade que tomou mais doses da vacina CORONAVAC:", cidade_mais_doses)
print("Contagem de pessoas vacinadas por região e faixa etária:")
print(contagem)
print("Idade média das pessoas vacinadas por região e faixa etária:")
print(idade_media)
print("Vacina mais administrada por região e faixa etária:")
print(vacina_mais_administrada)
print("Proporção de homens e mulheres vacinados por região e faixa etária:")
print(proporcao_sexo)
