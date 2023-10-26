create database rentup;

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
	user_email varchar(100) not null,
	item_nome varchar(50) not null,
	data_emprestimo timestamp not null,
	data_devolucao timestamp,
	estado varchar(50) not null,
	FOREIGN KEY (item_nome) REFERENCES itens (nome_item),
	FOREIGN KEY (user_email) REFERENCES users (email)
);
