/**
 * Arquivo JavaScript para manipulação da interface da Academia Gold Muscles.
 * Responsável pelo carrossel, rolagem suave e interações.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- LÓGICA DO CARROSSEL DE PERSONAIS ---
    const container = document.querySelector('.carousel-container');
    const items = document.querySelectorAll('.personal-card');
    const nextBtn = document.querySelector('.next-btn');
    const prevBtn = document.querySelector('.prev-btn');
    
    let currentIndex = 0;

    /**
     * Atualiza a posição do carrossel baseado no index atual.
     */
    function updateCarousel() {
        const offset = -currentIndex * 100;
        container.style.transform = `translateX(${offset}%)`;
    }

    // Botão Próximo
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % items.length;
            updateCarousel();
        });
    }

    // Botão Anterior
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            updateCarousel();
        });
    }

    // --- ROLAGEM SUAVE DOS LINKS ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- ANIMAÇÃO DE APARECIMENTO (REVEAL) AO DAR SCROLL ---
    const revealElements = document.querySelectorAll('section');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(50px)';
        el.style.transition = 'all 0.8s ease-out';
        revealObserver.observe(el);
    });

    // --- MÁSCARAS DE INPUT (IMask) ---
    const phoneMask = IMask(document.getElementById('telefone'), { mask: '(00) 00000-0000' });
    const cpfMask = IMask(document.getElementById('cpf'), { mask: '000.000.000-00' });
    const cardMask = IMask(document.getElementById('numero_cartao'), { mask: '0000 0000 0000 0000' });
    const dateMask = IMask(document.getElementById('validade_cartao'), { mask: '00/00' });
    const cvvMask = IMask(document.getElementById('cvv_cartao'), { mask: '000' });

    // --- LÓGICA DO MODAL DE MATRÍCULA ---
    const modalOverlay = document.getElementById('matriculaModal');
    const closeModalBtn = document.getElementById('closeModal');
    const formContent = document.getElementById('form-content');
    const successMessage = document.getElementById('success-message');
    const matriculaForm = document.getElementById('matriculaForm');
    const selectPagamento = document.getElementById('metodo_pagamento');
    const cartaoFields = document.getElementById('cartao-fields');
    
    // Mostra/Esconde campos de cartão baseado na escolha
    selectPagamento.addEventListener('change', () => {
        if (selectPagamento.value === 'Cartão de Crédito') {
            cartaoFields.style.display = 'block';
            document.getElementById('numero_cartao').required = true;
            document.getElementById('validade_cartao').required = true;
            document.getElementById('cvv_cartao').required = true;
        } else {
            cartaoFields.style.display = 'none';
            document.getElementById('numero_cartao').required = false;
            document.getElementById('validade_cartao').required = false;
            document.getElementById('cvv_cartao').required = false;
        }
    });

    // Abre o modal ao clicar em "Assinar Agora"
    document.querySelectorAll('.btn-matricular').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const planoId = btn.getAttribute('data-id');
            const planoNome = btn.getAttribute('data-nome');
            
            document.getElementById('planoEscolhidoNome').innerText = planoNome;
            document.getElementById('plano_id').value = planoId;
            
            formContent.style.display = 'block';
            successMessage.style.display = 'none';
            cartaoFields.style.display = 'none';
            matriculaForm.reset();
            
            modalOverlay.classList.add('active');
        });
    });

    // Fechar modal
    function closeModal() {
        modalOverlay.classList.remove('active');
    }
    
    closeModalBtn.addEventListener('click', closeModal);
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) closeModal();
    });

    // Submissão do formulário via AJAX
    matriculaForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btnSubmit = document.getElementById('btnSubmitForm');
        btnSubmit.innerText = 'Processando...';
        btnSubmit.disabled = true;

        const formData = {
            plano_id: document.getElementById('plano_id').value,
            nome: document.getElementById('nome').value,
            email: document.getElementById('email').value,
            telefone: phoneMask.unmaskedValue,
            cpf: cpfMask.unmaskedValue,
            metodo_pagamento: selectPagamento.value,
            // Dados sensíveis que o backend vai descartar, guardando apenas o final do número
            numero_cartao: cardMask.value 
        };

        try {
            const response = await fetch('/api/matricular', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                formContent.style.display = 'none';
                successMessage.style.display = 'block';
                
                setTimeout(() => {
                    closeModal();
                }, 6000);
            } else {
                alert('Ocorreu um erro: ' + result.message);
            }
        } catch (error) {
            alert('Falha na comunicação com o servidor. Verifique se o Flask está rodando.');
        } finally {
            btnSubmit.innerText = 'Concluir Matrícula';
            btnSubmit.disabled = false;
        }
    });
});
