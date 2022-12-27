"""a ideia do código é enviar um e-mail em uma data e hora específicas de feliz aniversário,
selecionando uma das quatro cartas padrão"""


from datetime import datetime
import pandas
import random
import smtplib

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

today = datetime.now()
today_tuple = (today.month, today.day)
"""para checar se hoje é um dos aniversários passados no csv foi criada uma tupla
para armazenar o mês e o dia"""
data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
""" No arquivo CSV em anexo o arquivo está do seguinte modo:
name,email,year,month,day
Test,test@email.com,1961,12,21
Portanto, no código acima, o comando iterrows faz a iteração pelo data (que recebeu o arquivo
 brithday.csv já devidamente lido), então, as colunas month e day são passadas como chaves e o próprio
 data_row é passado como valor na relação key:value, ou seja,
 o código está substituindo a seguinte ideia padrão:
 new_dict = {new_key: new_value for (index, data_row) in data.iterrows()
 Assim, o mês e dia ficam atrelados, passados como índice, para a coluna data (data_row), o data row
 é a coluna toda, ou seja, Test,test@email.com,1961,12,21 """
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
"""as linhas acima verificam se há algum aniversário no dia atual, se houver, ele passa o nome da pessoa
 para a birthday_person, depois o file path segue o caminho para escolher uma das 3 cartas disponíveis"""
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])
"""o código acima vai abrir o caminho do arquivo que já vai ser a carta selecionada, vai ler, e então vai 
substituir o espaço nome, que na carta está assim [NAME] pelo nome da pessoa na coluna name. Atentar que a
mesma variável primeiro lê o arquivo e depois guarda a carta do conteúdo alterado"""
    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )
"""A função with é usada para abrir o arquivo sem necessidade de usar depois o close.
 A função starttls é usada por questão de segurança, para encripitar o e-mail.
Provavelmente vai dar um erro, pois é preciso baixar todo nível de segurança do e-mail utilizado 
para enviar para que o sistema faça o processamento. Caso não funcione, ver a opção senha provisória,
 ver se não digitou nada errado e, por fim, tentar outro e-mail se não conseguir"""