# 🏋️ Gold Muscles - Site Institucional (Alunos)
### *"A vitrine digital de elite para a sua academia"*

Este projeto é a porta de entrada para os alunos. Uma Landing Page moderna com efeitos visuais de alta performance e sistema de matrícula integrado.

---

## 🛠️ Tecnologias Utilizadas
*   **Backend:** Python com Flask.
*   **Banco de Dados:** MySQL (compartilhado com o Gerenciamento).
*   **Frontend:** HTML5, CSS3 (Glassmorphism, Parallax) e JavaScript Puro.
*   **Máscaras:** iMask.js (para CPF, Telefone e Cartão).

---

## 📂 Estrutura de Pastas
*   `/static/css/style.css`: Toda a "magia" visual, cores douradas e efeitos Glow.
*   `/static/img/`: Onde você deve colocar as fotos dos personais.
*   `/templates/index.html`: O coração do site. Onde você edita textos e links.
*   `app.py`: O servidor que faz o site funcionar na porta `5000`.

---

## ✍️ Como Editar o Site (Para Iniciantes)

### 1. Trocar o número do WhatsApp
No arquivo `templates/index.html`, procure por:
`https://wa.me/5500000000000`
Substitua o `00...` pelo seu número com DDD (apenas números).

### 2. Mudar o Endereço no Mapa
No `index.html`, procure pela tag `<iframe>`. Dentro do link, mude o que vem depois de `q=` pelo seu endereço desejado (use `+` no lugar dos espaços).

### 3. Alterar Preços dos Planos
Os planos são carregados do banco de dados MySQL. Para mudar o valor, abra seu **HeidiSQL**, vá na tabela `planos` e mude a coluna `valor`. O site atualiza sozinho!

---

## 🚀 Como Rodar
1.  Certifique-se de que o **XAMPP (MySQL)** está ligado.
2.  Abra o terminal na pasta `Academia`.
3.  Digite: `python app.py`
4.  Acesse: `http://localhost:5000`

---
*Desenvolvido como parte do Ecossistema Gold Muscles Totalidade.*
