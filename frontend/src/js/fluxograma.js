const fluxogramaDisplay = document.getElementById('fluxograma-display');

let dadosFluxograma = [];

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/fluxograma/');
        dadosFluxograma = await response.json();

        renderCards(dadosFluxograma);
    } catch (err) {
        console.error(err);
        mostrarToast('Erro ao carregar fluxograma', 'error');
    }
});

function renderCards(data) {
    data
    .sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'))
    .forEach(item => {
        const divSemestre = document.querySelector(`.semestre-${item.semestre}`);
        if (!divSemestre) return;

        const card = document.createElement('div');
        card.classList.add('fluxograma-card');
        card.dataset.value = item.id;

        const prereqs = item.pre_requisitos?.length
            ? item.pre_requisitos.map(p => p.nome).join(', ')
            : 'Sem pré-requisitos';

        card.innerHTML = `
            <h3>${item.nome}</h3>
            <p>${prereqs}</p>
            <span class="fluxograma-badge">${item.horas}</span>
        `;

        divSemestre.appendChild(card);
    });
}

fluxogramaDisplay.addEventListener('click', (e) => {
    const card = e.target.closest('.fluxograma-card');
    if (!card) return;

    const isActive = card.classList.contains('active');

    if (isActive) {
        card.classList.remove('active');
        mostrarToast('Matéria desmarcada', 'primary');
    } else {
        card.classList.add('active');
        const value = card.dataset.value;
        mostrarToast(`Matéria selecionada: ${value}`, 'success');
    }
});

function mostrarToast(mensagem, tipo = 'success') {
    const toastEl = document.getElementById('toastFeedback');
    const toastMessage = document.getElementById('toastMessage');

    toastMessage.textContent = mensagem;

    toastEl.classList.remove('bg-success', 'bg-danger', 'bg-primary');
    toastEl.classList.add(tipo === 'success' ? 'bg-success' : tipo === 'error' ? 'bg-danger' : 'bg-primary');

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}