-- Criação do Banco de Dados para a Academia Gold Muscles
CREATE DATABASE IF NOT EXISTS gold_muscles;
USE gold_muscles;

-- Tabela para armazenar os planos da academia
CREATE TABLE IF NOT EXISTS planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    beneficios TEXT NOT NULL
);

-- Tabela para armazenar os personal trainers
CREATE TABLE IF NOT EXISTS personais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    horarios VARCHAR(255) NOT NULL,
    dias VARCHAR(255) NOT NULL,
    imagem_url VARCHAR(255) NOT NULL
);

-- Inserindo alguns planos iniciais de exemplo
INSERT INTO planos (nome, valor, beneficios) VALUES 
('Plano Silver', 89.90, 'Acesso à musculação; Armário rotativo; App de treino'),
('Plano Gold', 129.90, 'Musculação total; Aulas coletivas; Leve um amigo 4x/mês; Área VIP'),
('Plano Muscle VIP', 199.90, 'Personal trainer 1x semana; Avaliação física mensal; Brinde exclusivo; Acesso ilimitado');

-- Inserindo alguns personais iniciais de exemplo
INSERT INTO personais (nome, descricao, horarios, dias, imagem_url) VALUES 
('Ricardo Silva', 'Especialista em hipertrofia e emagrecimento.', '06:00 - 12:00', 'Seg, Qua, Sex', 'trainer1.png'),
('Camila Santos', 'Especialista em funcional e pilates clínico.', '14:00 - 20:00', 'Ter, Qui, Sáb', 'trainer2.png');
