create database if not exists rentup;

create table itens(
	nome_item varchar(50) primary key,
	qnt_total integer not null,
	qnt_estoque integer not null,
	qnt_emprestar integer not null,
	qnt_emprestados integer not null,
	qnt_danificados integer not null,
	descricao varchar(200)
);

create table users(
	nome varchar(50) not null,
	email varchar(100) not null primary key,
	senha varchar(100) not null,
	papel varchar(50) not null
);

create table rent(
	id SERIAL primary key,
	item_nome varchar(50) not null,
	user_id int not null,
	data_emprestimo date not null,
	data_deovlucao date,
	FOREIGN KEY (item_nome) REFERENCES itens (nome_item),
	FOREIGN KEY (user_id) REFERENCES users (id)
);
