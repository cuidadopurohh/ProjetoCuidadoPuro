create database cuidadopuro;
use cuidadopuro;

create table clientes(
id_cliente int auto_increment primary key,
nome_cliente varchar(100),
rg_cliente varchar(20),
cpf_cliente varchar(15),
endereco_cliente varchar(40),
telefone_cliente varchar(15),
idade_cliente int,
email_cliente varchar(150) unique,
senha_cliente varchar(25)
);

create table cuidador(
id_cuidador int auto_increment primary key,
nome_cuidador varchar(100),
rg_cuidador varchar(20),
cpf_cuidador varchar(15),
endereco_cuidador varchar(40),
telefone_cuidador varchar(15),
idade_cuidador int,
cidade_cuidador varchar(50),
email_cuidador varchar(150) unique,
senha_cuidador Varchar(25)
);


create table administrador(
id_admin int auto_increment primary key,
nome_admin varchar(100),
email_admin varchar(150) unique,
senha_admin varchar(25)
);

create table habilidades(
id_habil int auto_increment primary key,
habilidades varchar(100)
);

create table necessidades(
id_necess int auto_increment primary key,
necessidades varchar(100)
);

create table match_(

id_cuidador int,
id_cliente int,
agendamento varchar(50),
pagamento decimal(12,2),
foreign key(id_cuidador) references cuidador(id_cuidador),
foreign key(id_cliente) references clientes(id_cliente)
);

select * from clientes;

