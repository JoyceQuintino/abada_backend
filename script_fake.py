from faker import Faker
import csv
import random

fake = Faker('pt_BR')

header = ['nome', 'apelido', 'numero', 'cidade', 'estado', 'sexo', 'idade', 'filiacao', 'graduacao']
data = []

graduacao = ['Laranja', 'Laranja-azul', 'Azul', 'Azul-verde', 'Verde', 'Verde-roxa', 'Roxa', 'Roxa-marrom', 'Marrom', 'Marrom-vermelha', 'Vermelha', 'Vermelha-branca', 'Branca']

apelidos_unicos = set()

for _ in range(300):
    apelido = fake.user_name()
    while apelido in apelidos_unicos:
        apelido = fake.user_name()
    apelidos_unicos.add(apelido)
    
    row = [fake.name(), apelido, fake.random_int(min=1, max=1000), fake.city(), fake.state(), fake.random_element(elements=('M', 'F')), fake.random_int(min=18, max=90), fake.job(), random.choice(graduacao)]
    data.append(row)

with open('dados_falsos.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("Arquivo 'dados_falsos.csv' criado com sucesso!")