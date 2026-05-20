const form = document.getElementById("login-form");
const mensagemErro = document.getElementById("mensagem-erro");

const API_BASE_URL = "https://wayne-security-backend.onrender.com";

function mostrarErroLogin(mensagem) {
  mensagemErro.textContent = mensagem;
}

function limparErroLogin() {
  mensagemErro.textContent = "";
}

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value.trim();

  limparErroLogin();

  if (!email || !senha) {
    mostrarErroLogin("Preencha email e senha.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: email,
        senha: senha
      })
    });

    const data = await response.json();

    if (response.status === 401 || response.status === 403 || response.status === 404) {
      mostrarErroLogin(data.error || "Credenciais inválidas.");
      return;
    }

    if (!response.ok) {
      mostrarErroLogin(data.error || "Erro ao fazer login.");
      return;
    }

    localStorage.setItem("token", data.token);
    localStorage.setItem("cargo", data.cargo);
    localStorage.setItem("nome", data.nome);

    window.location.href = "dashboard.html";

  } catch (error) {
    mostrarErroLogin("Erro de conexão com o servidor.");
    console.error("Erro no login:", error);
  }
});