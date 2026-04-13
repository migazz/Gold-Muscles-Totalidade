# ⚙️ Gold Muscles - Gerenciamento Operacional
### *"O cérebro administrativo da sua academia"*

Este é o sistema de Back-office onde a equipe da Gold Muscles controla cadastros, aprova pagamentos e gera treinos para os alunos.

---

## 🔒 Sistema de Acessos (Login)
O sistema possui 3 níveis de permissão para garantir a segurança:

1.  **Dono (login: `dono` / senha: `123`):** Controle total. Pode aprovar, inativar e excluir alunos, além de demitir e contratar personais.
2.  **Funcionário (login: `func` / senha: `123`):** Pode ver listas e criar fichas de treino. Não pode excluir alunos nem personais.
3.  **Colaborador (login: `colab` / senha: `123`):** Acesso básico para visualização e consulta.

---

## 📋 Funcionalidades Principais

### 1. Gestão de Alunos
*   **Aprovação:** Matrículas feitas no site caem como "Pendentes". O dono aprova após o pagamento na recepção.
*   **Inativação:** Para alunos que pararam de pagar mas você não quer apagar o histórico.
*   **Exclusão:** Remove o aluno e TODAS as fichas de treino dele permanentemente.

### 2. Gestão de Personais (Trainers)
*   **Contratação:** Cadastre o nome, especialidade e horários para que ele apareça no site público na hora!
*   **Demitir:** Botão de lixeira (exclusivo do dono). O sistema bloqueia a demissão se o personal ainda tiver fichas ativas (segurança de dados).

### 3. Fichas de Treino & Impressão
*   **Criação:** Selecione o aluno e o treinador, e use o campo "Treino Livre" para ditar as séries.
*   **Impressão Minimalista:** O botão "IMPRIMIR" gera um documento limpo, com a Logo Gold Muscles, pronto para o aluno levar para o treino ou salvar em PDF.

---

## 🚀 Como Rodar
1.  Abra o terminal na pasta `Academia gerenciamento`.
2.  Digite: `python app.py`
3.  Acesse: `http://localhost:5001`

---
*Gerencie com autoridade. Treine com força.*
