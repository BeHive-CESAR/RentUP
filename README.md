# RentUP
> API favorita do Garagino!

## 🤔 O que o RentUP? 
O **RentUP** é uma **API para gerenciamento** de **estoque, usuários e empréstimos** para laboratórios maker

Oferecendo:
- Sistema de permissões para usuários
- Sistema de autorização, acompanhamento e controle de empréstimos
- Controle e acompanhamento de estoque em tempo real
- Inferencia de dados, auxiliando o gerente do lab na tomada de decisões

## 🦄 Por que usar o RentUP?
  Escrever o diferenial aqui

## 🧑‍💻 Tecnologias usadas no desenvolvimento
  Escrever aqui as tecnologias usadas e pq
  (FastAPI, PostgreSQL, Python, Alambic, SqlAlchemy)

## ⚙️ Instruções de instalação

- Linguagem Utilizada
    - ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
    -  Utilizamos a versão 3.11.2!
### Instalando e configurando o postgreSQL
1. Instale o <a src="https://www.postgresql.org/download/">PostgreSQL</a>
2. Faça a instalação normal e coloque a senha se sua escolha. Mas cuidado! Não se esqueça dela
3. *Opcional:* Recomendamos que utilize o <a src="https://dbeaver.io/download/">DBeaver</a> para manipular o banco de dados. Mas caso prefira, não tem problema usar o pgAdmin4, gerenciador padrão do PosgreSQL
4. No DBeaver clique em **"Nova conexão"**. 
    1. Selecione o PostgreSQL e clique em avançar
    2. Se você fez a instalação de forma padrão só precisará colocar sua senha *(definida no passo 2)* no campo senha
    3. Clique em concluir e sua conexão deve estar funcionando
    4. Clique na setinha ao lado do elefantinho e irá aparecer uma pasta chamada *Bancos de Dados*. Clique com o  botão direito sobre ela e selecione **Criar nova Banco de Dados**
    5. Preencha o nome do banco de dados como preferir! O nosso se chama RentUP 😁
    6. Agora vamos montar sua string de conexão com o banco! Ficará assim: **postgresql+pg8000://postgres:*SUASENHA*@localhost:5432/*NOMEDOSEUBANCODEDADOS*** . Deixa ela salva, pois vamos precisar jaja
5. Clone o repositorio do RentUP e abra o projeto do seu VSCode (Ou a IDE que preferir)
### Preparando seu ambiente de desenvolvimento (No windows)
1. Crie seu ambiente virtual 
```
python -m venv venv
```
2. Ative seu ambiente virtual
```
.\venv\Scripts\activate
```
3. Instale todas as dependências do projeto
```
pip install -r requirements
```
4. Quase tudo pronto! Crie um arquivo no diretório do projeto chamado **.env** e nele você vai colocar o seguinte:
```
CONNECT= --- AQUI VOCÊ COLOCA A STRING DE CONEXÃO FEITA NO PASSO 4.6 ---
SECRET_KEY= --- AQUI VOCÊ COLOCA UMA RANDOM HEX KEY ---
ALGORITHM=HS256
``` 
Pode gerar a Random Hex Key nesse site <a href="https://www.browserling.com/tools/random-hex">aqui</a>
5. Ufa! Tudo pronto! Agora basta executar esses 2 comandos *(um de cada vez)* para rodar o projeto!
```
alembic upgrade head
uvicorn api.main:app --reload
```




##
## Desenvolvido por:
<div align="center">
  <table>
    <tr>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/LucasGdBS?v=4" width="100px;" alt=""/><br /><sub><b>Lucas Gabriel</b></sub></a><br /></a></td>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Carlos3du" width="100px;" alt=""/><br /><sub><b>Carlos Eduardo</b></sub></a><br /></a></td>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/FernandaFBMarques" width="100px;" alt=""/><br /><sub><b>Maria Fernanda</b></sub></a><br /></a></td>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Gabriel-Chaves0" width="100px;" alt=""/><br /><sub><b>Gabriel Chaves</b></sub></a><br /></a></td>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/PedroVillasBoas" width="100px;" alt=""/><br /><sub><b>Pedro Villas Boas</b></sub></a><br /></a></td>
      <td align="center"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Caiobadv" width="100px;" alt=""/><br /><sub><b>Caio Barreto</b></sub></a><br /></a></td>
    </tr>
  </table>
</div>
