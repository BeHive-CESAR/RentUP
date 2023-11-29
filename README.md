<h2 align="center">
 <img src="https://img.shields.io/badge/REPO Size-231 KB-blue?style=for-the-badge" alt="size" />
  <img src="https://img.shields.io/badge/Languages-1-blue?style=for-the-badge" alt="Server Ok" />
  <img src="https://img.shields.io/badge/License-MIT-blue?color=blue&style=for-the-badge" alt="License" />
</h2>
<div align="center" alt="RentUpLogo">
 
 ![rentup-logo](https://github.com/BeHive-CESAR/RentUP/assets/114539692/0e52f689-4465-459c-ba1c-0bd0cc6ea1c4)

</div>

## 💡 <code>De onde surgiu ?</code>
Bem vindo a mais um produto do grupo BeeHive, grupo de estudantes da faculdade CESAR School, desenvolvedores e entusiastas de tecnologia e inovação.
Contando brevemente a historia desse projeto:

Nessa oportunidade tivemos o prazer de trabalhar juntamente ao Garagino (Grupo de estudo cientifico dos alunos da CESAR), que chegaram ao nosso grupo com uma problematica bem clara:
- A falta de um sistema que os ajudasse a monitorar os equipamentos do laboratório.
- A falta de controle dos empréstimos que são realizados pelo laboratório,  atualmente isso é feito de uma forma muito desestruturada.

A partir de encontros com responsáveis pelo Garagino nós imergimos no problema para vir com a melhor solução para eles, e após todo processo nós criamos o RentUp.

## 🤔 <code>O que é o RentUP? </code>
O **RentUP** é uma **API para gerenciamento** de **estoque, usuários e empréstimos** para laboratórios maker

Oferecendo:
- Sistema de permissões para usuários
- Sistema de autorização, acompanhamento e controle de empréstimos
- Controle e acompanhamento de estoque em tempo real
- Inferencia de dados, auxiliando o gerente do lab na tomada de decisões

## 🦄 <code>Por que usar o RentUP?</code>
  
Agora você me pergunta, qual vantagem que eu, como cliente, teria em usar o produto RentUp?

A resposta é bem simples: por ser uma API, a **flexibilidade** e **escalabilidade** do produto se diferenciam dos seus concorrentes no mercado.

Tornando qualquer tipo de integração com o front-end desejado, simples e prática de se fazer. Em pouco tempo, é possível se adaptar a qualquer demanda.

Sabe quando é necessário que haja uma mudança ou adaptação no produto já feito? Seja em relação à atualização de uma tecnologia ou até mesmo uma evolução de sistema? A nossa solução cobre exatamente esse problema. Sendo uma API, qualquer tipo de integração com o front-end desejado, é simples e prática de se fazer. Em pouco tempo, é possível se adaptar a qualquer demanda.

Então a pergunta certa seria, ***Porque não usar?*** 

## 🧑‍💻 <code>Tecnologias usadas no desenvolvimento</code>

<h2 align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python" />
  
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostGreSQL" />
  <img src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" alt="vscode" />
</h2>

<div align="center">

| Tecnologia | Descriçao | Versão |
|:---:|---------|:-----------:|
|  **Python**  |Back-end do projeto e contrução da APi| <img src="https://img.shields.io/badge/3.11.2-black" /> |
|  **FastAPI**  |Framework usar para criação de API Rest|    <img src="https://img.shields.io/badge/0.103.2-black" />       |
|  **PostgreSQL**  |Banco de dados utilizado|    <img src="https://img.shields.io/badge/15.3-black" /> |
|  **Alambic**  | Ferramenta usada para migrações do banco de dados |    <img src="https://img.shields.io/badge/1.12.1-black" /> |
|  **SqlAlchemy**  | ORM utilizado para controle do banco de dados |    <img src="https://img.shields.io/badge/2.0.20-black" /> |

</div>

## 💻 <code>Utilizando o RentUP</code>
Para garantir o funcionamento e aplicação da API desenvolvida, colocamos ela em funcionamento juntamente ao framework *StreamLit*, que é uma ferramenta para contrução de interfaces web.

A utilização dessa ferramenta foi realizada devido à agilidade que ela proporciona à equipe.

<div align="center" justify-content= "space-around">

[Interface Usuário](https://github.com/BeHive-CESAR/frontUserRentUp) |
[Interface Administrador](https://github.com/BeHive-CESAR/frontAdmRentUp)

</div>


Segue algumas imagens e gifs do funcionamento dela nessa aplicação, validadando assim seu funcionamento.

Inserir gif e imagem :)

## ⚙️ <code>Instruções de instalação</code>

- Linguagem Utilizada
    - Python
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
5. Clone o repositorio do RentUP e abra o projeto no seu VSCode (Ou a IDE que preferir)
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

## <code>Mais detalhes - Google Sites</code>
<div align="center">
 <a href="">
  
  [![GoogleSites](https://img.shields.io/badge/Acessar%20Site%20-Google%20Sites-%)](https://sites.google.com/cesar.school/beehive/início)

</a>
</div>


##
## <code>Desenvolvido por:</code>
<div align="center">
  <table>
    <tr>
      <td align="center"><a href=https://github.com/lucasgdbs><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/LucasGdBS?v=4" width="100px;" alt=""/><br /><sub><b>Lucas Gabriel</b></sub><br /></a></td>
      <td align="center"><a href=https://github.com/Carlos3du><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Carlos3du" width="100px;" alt=""/><br /><sub><b>Carlos Eduardo</b></sub><br /></a></td>
      <td align="center"><a href=https://github.com/FernandaFBMarques><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/FernandaFBMarques" width="100px;" alt=""/><br /><sub><b>Maria Fernanda</b></sub><br /></a></td>
      <td align="center"><a href=https://github.com/Gabriel-Chaves0><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Gabriel-Chaves0" width="100px;" alt=""/><br /><sub><b>Gabriel Chaves</b></sub><br /></a></td>
      <td align="center"><a href=https://github.com/PedroVillasBoas><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/PedroVillasBoas" width="100px;" alt=""/><br /><sub><b>Pedro Villas Boas</b></sub><br /></a></td>
      <td align="center"><a href=https://github.com/Caiobadv><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/Caiobadv" width="100px;" alt=""/><br /><sub><b>Caio Barreto</b></sub><br /></a></td>
    </tr>
  </table>
</div>
