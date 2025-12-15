const loginMatricula = document.getElementById('login-matricula');
const loginPassword = document.getElementById('login-password');
const registroNome = document.getElementById('register-nome');
const registroMatricula = document.getElementById('register-matricula');
const registroEmail = document.getElementById('register-email');
const registroPassword = document.getElementById('register-password');

function showRegister() {
    document.getElementById('login').classList.remove('active');
    document.getElementById('registro').classList.add('active');
}

function showLogin() {
    document.getElementById('registro').classList.remove('active');
    document.getElementById('login').classList.add('active');
}

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);

    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = '🙈';
    } else {
        input.type = 'password';
        button.textContent = '👁';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    mostrarToast('Nosso sistema está em fase de testes. As matrículas ainda não são validadas.', 'primary');
});

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
        matricula: loginMatricula.value,
        senha: loginPassword.value
    }

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (data.status) {
        mostrarToast('Login realizado com sucesso!', 'success');

        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 1500);
    } else {
        mostrarToast('Erro no login: ' + data.message, 'error');
    }

});

document.getElementById('registroForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const payload = {
        nome: registroNome.value,
        matricula: registroMatricula.value,
        email: registroEmail.value,
        senha: registroPassword.value
    }

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    
    if (data.status) {
        mostrarToast('Registro realizado com sucesso! Você já pode fazer login.', 'success');
        
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 1500);
    } else {
        mostrarToast('Erro no registro: ' + data.message, 'error');
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