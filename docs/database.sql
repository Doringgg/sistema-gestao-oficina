CREATE DATABASE oficina ;

USE oficina ;

CREATE TABLE clientes (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(45) NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE carros (
    placa VARCHAR(7) PRIMARY KEY,
    montadora VARCHAR(45) NOT NULL,
    modelo VARCHAR(45) NOT NULL,
    cor VARCHAR(45),
    clientes_cpf VARCHAR(14),
        FOREIGN KEY (clientes_cpf)
        REFERENCES clientes(cpf)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);