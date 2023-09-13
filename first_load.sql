create database lab;

create table itens(
	nome_item varchar(50) primary key,
	qnt_total integer not null,
	qnt_estoque integer not null,
	qnt_emprestados integer not null,
	qnt_danificados integer not null
);

create table users(
	id SERIAL primary key,
	nome varchar(50) not null,
	email varchar(100) not null,
	item varchar(50),
	state bool not null,
	FOREIGN KEY (item) REFERENCES itens(nome_item)
);
