# 🥇 Gold Muscles Totalidade: Ecossistema Fitness de Elite
### *"Transformando academias com tecnologia de ponta e design de luxo"*

Este repositório contém o ecossistema completo desenvolvido para a academia **Gold Muscles**, abrangendo desde o primeiro contato do aluno (Marketing/Venda) até a operação interna (Gestão/Treinos).

---

## 🏛️ Arquitetura do Projeto

O projeto é dividido em dois sistemas independentes que compartilham o mesmo banco de dados MySQL, garantindo sincronização em tempo real:

### 1. [🏋️ Academia (Site do Aluno)](./Academia/)
Uma Landing Page de alto padrão visual focada na experiência do usuário (UX).
*   **Destaques:** Efeito Parallax, design Glassmorphism, máscara de cartão de crédito segura e integração com WhatsApp.
*   **Objetivo:** Captura de leads e pré-matrícula online.
*   **Porta padrão:** `5000`

### 2. [⚙️ Academia Gerenciamento (Back-office)](./Academia%20gerenciamento/)
Um Dashboard administrativo robusto para a equipe da academia.
*   **Destaques:** Níveis de acesso (Dono, Funcionário, Colaborador), CRUD de alunos e personais, e gerador de fichas de treino com impressão minimalista.
*   **Objetivo:** Operação diária, controle de frequência e prescrição de treinos.
*   **Porta padrão:** `5001`

---

## 🛠️ Stack Tecnológica
*   **Backend:** Python 3.x + Flask.
*   **ORM:** SQLAlchemy (integração fluida com banco de dados).
*   **Banco de Dados:** MySQL (XAMPP).
*   **Frontend:** HTML5 semântico, CSS3 Moderno (Variáveis, Flexbox, Grid) e JavaScript Vanilla.
*   **Design:** Inspirado em tendências de luxo do Behance (Dark Mode & Gold accents).

---

## 🚀 Como Executar o Ecossistema

Para rodar o projeto completo no seu ambiente local:

1.  **Banco de Dados:** Inicie o MySQL no XAMPP e importe os modelos (o script `db.create_all()` nos servidores fará isso automaticamente na primeira execução).
2.  **Terminal 1 (Site Aluno):**
    ```bash
    cd Academia
    python app.py
    ```
3.  **Terminal 2 (Painel Admin):**
    ```bash
    cd "Academia gerenciamento"
    python app.py
    ```

---

## 🔒 Credenciais de Acesso (Demo)
Para testar o Painel Administrativo, use:
*   **Login:** `dono` | **Senha:** `123` (Acesso Total)
*   **Login:** `func` | **Senha:** `123` (Acesso Operacional)

---

## 📖 Manuais Detalhados
Cada pasta possui seu próprio manual técnico com instruções específicas:
*   [Manual do Site Aluno](./Academia/MANUAL.md)
*   [Manual do Sistema de Gestão](./Academia%20gerenciamento/MANUAL.md)

---
*Este projeto foi desenvolvido para demonstrar a criação de soluções Full-stack escaláveis e com foco em design premium para o setor de bem-estar.* 🥇🏋️‍♂️

## Autor: Miguel Santana 
