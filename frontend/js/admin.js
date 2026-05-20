const API_BASE_URL = "http://127.0.0.1:5000";

const token = localStorage.getItem("token");
const cargo = localStorage.getItem("cargo");

if (!token) {
  window.location.href = "login.html";
}

if (cargo !== "admin") {
  alert("Acesso negado. Apenas administradores podem acessar esta página.");
  window.location.href = "dashboard.html";
}

const headers = {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
};

const tabButtons = document.querySelectorAll(".tab-button");
const contentSections = document.querySelectorAll(".content-section");
const btnDashboard = document.getElementById("btn-dashboard");
const btnLogout = document.getElementById("btn-logout");

// RECURSOS
let recursoEditandoId = null;

const btnNovoRecurso = document.getElementById("btn-novo-recurso");
const btnSalvarRecurso = document.getElementById("btn-salvar-recurso");
const btnCancelarRecurso = document.getElementById("btn-cancelar-recurso");

const formRecursoBox = document.getElementById("form-recurso-box");
const listaRecursos = document.getElementById("lista-recursos");
const mensagemRecurso = document.getElementById("mensagem-recurso");

const inputNome = document.getElementById("recurso-nome");
const inputCategoria = document.getElementById("recurso-categoria");
const inputStatus = document.getElementById("recurso-status");
const inputLocalizacao = document.getElementById("recurso-localizacao");
const inputDescricao = document.getElementById("recurso-descricao");

// USUÁRIOS
let usuarioEditandoId = null;

const btnNovoUsuario = document.getElementById("btn-novo-usuario");
const btnSalvarUsuario = document.getElementById("btn-salvar-usuario");
const btnCancelarUsuario = document.getElementById("btn-cancelar-usuario");

const formUsuarioBox = document.getElementById("form-usuario-box");
const listaUsuarios = document.getElementById("lista-usuarios");
const mensagemUsuario = document.getElementById("mensagem-usuario");

const inputUsuarioNome = document.getElementById("usuario-nome");
const inputUsuarioEmail = document.getElementById("usuario-email");
const inputUsuarioSenha = document.getElementById("usuario-senha");
const inputUsuarioCargo = document.getElementById("usuario-cargo");

// CREDENCIAIS
const listaCredenciais = document.getElementById("lista-credenciais");

// ABAS
tabButtons.forEach(button => {
  button.addEventListener("click", () => {
    const targetId = button.getAttribute("data-target");

    tabButtons.forEach(btn => btn.classList.remove("active"));
    contentSections.forEach(section => section.classList.remove("active-section"));

    button.classList.add("active");
    document.getElementById(targetId).classList.add("active-section");
  });
});

// BOTÕES PRINCIPAIS
btnDashboard.addEventListener("click", () => {
  window.location.href = "dashboard.html";
});

btnLogout.addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("cargo");
  localStorage.removeItem("nome");
  window.location.href = "login.html";
});

// RECURSOS
btnNovoRecurso.addEventListener("click", () => {
  recursoEditandoId = null;
  limparFormularioRecurso();
  mensagemRecurso.textContent = "";
  btnSalvarRecurso.textContent = "Salvar Recurso";
  formRecursoBox.classList.remove("hidden");
});

btnCancelarRecurso.addEventListener("click", () => {
  recursoEditandoId = null;
  limparFormularioRecurso();
  mensagemRecurso.textContent = "";
  btnSalvarRecurso.textContent = "Salvar Recurso";
  formRecursoBox.classList.add("hidden");
});

btnSalvarRecurso.addEventListener("click", async () => {
  const nome = inputNome.value.trim();
  const categoria = inputCategoria.value;
  const status = inputStatus.value;
  const localizacao = inputLocalizacao.value.trim();
  const descricao = inputDescricao.value.trim();

  mensagemRecurso.textContent = "";

  if (!nome || !categoria || !status) {
    mensagemRecurso.textContent = "Nome, categoria e status são obrigatórios.";
    return;
  }

  const metodo = recursoEditandoId ? "PUT" : "POST";
  const url = recursoEditandoId
    ? `${API_BASE_URL}/resources/${recursoEditandoId}`
    : `${API_BASE_URL}/resources`;

  try {
    const response = await fetch(url, {
      method: metodo,
      headers,
      body: JSON.stringify({
        nome,
        categoria,
        status,
        localizacao,
        descricao
      })
    });

    const data = await response.json();

    if (!response.ok) {
      mensagemRecurso.textContent = data.error || "Erro ao salvar recurso.";
      return;
    }

    mensagemRecurso.textContent = recursoEditandoId
      ? "Recurso atualizado com sucesso."
      : "Recurso criado com sucesso.";

    recursoEditandoId = null;
    limparFormularioRecurso();
    btnSalvarRecurso.textContent = "Salvar Recurso";
    formRecursoBox.classList.add("hidden");
    carregarRecursos();

  } catch (error) {
    console.error("Erro ao salvar recurso:", error);
    mensagemRecurso.textContent = "Erro de conexão com o servidor.";
  }
});

function limparFormularioRecurso() {
  inputNome.value = "";
  inputCategoria.value = "";
  inputStatus.value = "";
  inputLocalizacao.value = "";
  inputDescricao.value = "";
}

async function carregarRecursos() {
  try {
    listaRecursos.innerHTML = "<p>Carregando recursos...</p>";

    const response = await fetch(`${API_BASE_URL}/resources`);
    const data = await response.json();

    if (!response.ok) {
      listaRecursos.innerHTML = "<p>Erro ao carregar recursos.</p>";
      return;
    }

    if (data.length === 0) {
      listaRecursos.innerHTML = "<p>Nenhum recurso cadastrado.</p>";
      return;
    }

    listaRecursos.innerHTML = "";

    data.forEach(recurso => {
      const item = document.createElement("div");
      item.classList.add("resource-item");

      item.innerHTML = `
        <h4>${recurso.nome}</h4>
        <p><strong>Categoria:</strong> ${recurso.categoria}</p>
        <p><strong>Status:</strong> ${recurso.status}</p>
        <p><strong>Localização:</strong> ${recurso.localizacao || "-"}</p>
        <p><strong>Descrição:</strong> ${recurso.descricao || "-"}</p>

        <div class="resource-actions">
          <button class="btn-edit-resource" data-id="${recurso.id}">
            Editar
          </button>

          <button class="btn-delete-resource" data-id="${recurso.id}">
            Excluir
          </button>
        </div>
      `;

      listaRecursos.appendChild(item);
    });

    adicionarEventosEditarRecursos(data);
    adicionarEventosExcluirRecursos();

  } catch (error) {
    console.error("Erro ao carregar recursos:", error);
    listaRecursos.innerHTML = "<p>Erro de conexão com o servidor.</p>";
  }
}

function adicionarEventosEditarRecursos(recursos) {
  const botoesEditar = document.querySelectorAll(".btn-edit-resource");

  botoesEditar.forEach(botao => {
    botao.addEventListener("click", () => {
      const recursoId = Number(botao.getAttribute("data-id"));
      const recurso = recursos.find(item => item.id === recursoId);

      if (!recurso) {
        alert("Recurso não encontrado.");
        return;
      }

      recursoEditandoId = recurso.id;

      inputNome.value = recurso.nome;
      inputCategoria.value = recurso.categoria;
      inputStatus.value = recurso.status;
      inputLocalizacao.value = recurso.localizacao || "";
      inputDescricao.value = recurso.descricao || "";

      mensagemRecurso.textContent = "";
      btnSalvarRecurso.textContent = "Atualizar Recurso";
      formRecursoBox.classList.remove("hidden");
    });
  });
}

function adicionarEventosExcluirRecursos() {
  const botoesExcluir = document.querySelectorAll(".btn-delete-resource");

  botoesExcluir.forEach(botao => {
    botao.addEventListener("click", async () => {
      const recursoId = botao.getAttribute("data-id");
      const confirmar = confirm("Deseja realmente excluir este recurso?");

      if (!confirmar) {
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/resources/${recursoId}`, {
          method: "DELETE",
          headers
        });

        const data = await response.json();

        if (!response.ok) {
          alert(data.error || "Erro ao excluir recurso.");
          return;
        }

        carregarRecursos();

      } catch (error) {
        console.error("Erro ao excluir recurso:", error);
        alert("Erro de conexão com o servidor.");
      }
    });
  });
}

// USUÁRIOS
btnNovoUsuario.addEventListener("click", () => {
  usuarioEditandoId = null;
  limparFormularioUsuario();
  mensagemUsuario.textContent = "";
  btnSalvarUsuario.textContent = "Salvar Usuário";
  inputUsuarioSenha.placeholder = "Digite a senha";
  formUsuarioBox.classList.remove("hidden");
});

btnCancelarUsuario.addEventListener("click", () => {
  usuarioEditandoId = null;
  limparFormularioUsuario();
  mensagemUsuario.textContent = "";
  btnSalvarUsuario.textContent = "Salvar Usuário";
  inputUsuarioSenha.placeholder = "Digite a senha";
  formUsuarioBox.classList.add("hidden");
});

btnSalvarUsuario.addEventListener("click", async () => {
  const nome = inputUsuarioNome.value.trim();
  const email = inputUsuarioEmail.value.trim();
  const senha = inputUsuarioSenha.value.trim();
  const cargo = inputUsuarioCargo.value;

  mensagemUsuario.textContent = "";

  if (!nome || !email || !cargo) {
    mensagemUsuario.textContent = "Nome, email e cargo são obrigatórios.";
    return;
  }

  if (!usuarioEditandoId && !senha) {
    mensagemUsuario.textContent = "Senha é obrigatória para cadastrar novo usuário.";
    return;
  }

  const metodo = usuarioEditandoId ? "PUT" : "POST";
  const url = usuarioEditandoId
    ? `${API_BASE_URL}/users/${usuarioEditandoId}`
    : `${API_BASE_URL}/users`;

  const dadosUsuario = {
    nome,
    email,
    cargo
  };

  if (senha) {
    dadosUsuario.senha = senha;
  }

  try {
    const response = await fetch(url, {
      method: metodo,
      headers,
      body: JSON.stringify(dadosUsuario)
    });

    const data = await response.json();

    if (!response.ok) {
      mensagemUsuario.textContent = data.error || "Erro ao salvar usuário.";
      return;
    }

    mensagemUsuario.textContent = usuarioEditandoId
      ? "Usuário atualizado com sucesso."
      : "Usuário criado com sucesso.";

    usuarioEditandoId = null;
    limparFormularioUsuario();
    btnSalvarUsuario.textContent = "Salvar Usuário";
    inputUsuarioSenha.placeholder = "Digite a senha";
    formUsuarioBox.classList.add("hidden");

    carregarUsuarios();
    carregarCredenciais();

  } catch (error) {
    console.error("Erro ao salvar usuário:", error);
    mensagemUsuario.textContent = "Erro de conexão com o servidor.";
  }
});

function limparFormularioUsuario() {
  inputUsuarioNome.value = "";
  inputUsuarioEmail.value = "";
  inputUsuarioSenha.value = "";
  inputUsuarioCargo.value = "";
}

async function carregarUsuarios() {
  try {
    listaUsuarios.innerHTML = "<p>Carregando usuários...</p>";

    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "GET",
      headers
    });

    const data = await response.json();

    if (!response.ok) {
      listaUsuarios.innerHTML = "<p>Erro ao carregar usuários.</p>";
      return;
    }

    if (data.length === 0) {
      listaUsuarios.innerHTML = "<p>Nenhum usuário cadastrado.</p>";
      return;
    }

    listaUsuarios.innerHTML = "";

    data.forEach(usuario => {
      const item = document.createElement("div");
      item.classList.add("resource-item");

      item.innerHTML = `
        <h4>${usuario.nome}</h4>
        <p><strong>Email:</strong> ${usuario.email}</p>
        <p><strong>Cargo:</strong> ${usuario.cargo}</p>

        <div class="resource-actions">
          <button class="btn-edit-user" data-id="${usuario.id}">
            Editar
          </button>

          <button class="btn-delete-user" data-id="${usuario.id}">
            Excluir
          </button>
        </div>
      `;

      listaUsuarios.appendChild(item);
    });

    adicionarEventosEditarUsuarios(data);
    adicionarEventosExcluirUsuarios();

  } catch (error) {
    console.error("Erro ao carregar usuários:", error);
    listaUsuarios.innerHTML = "<p>Erro de conexão com o servidor.</p>";
  }
}

function adicionarEventosEditarUsuarios(usuarios) {
  const botoesEditar = document.querySelectorAll(".btn-edit-user");

  botoesEditar.forEach(botao => {
    botao.addEventListener("click", () => {
      const usuarioId = Number(botao.getAttribute("data-id"));
      const usuario = usuarios.find(item => item.id === usuarioId);

      if (!usuario) {
        alert("Usuário não encontrado.");
        return;
      }

      usuarioEditandoId = usuario.id;

      inputUsuarioNome.value = usuario.nome;
      inputUsuarioEmail.value = usuario.email;
      inputUsuarioSenha.value = "";
      inputUsuarioCargo.value = usuario.cargo;

      mensagemUsuario.textContent = "";
      btnSalvarUsuario.textContent = "Atualizar Usuário";
      inputUsuarioSenha.placeholder = "Deixe em branco para manter a senha atual";
      formUsuarioBox.classList.remove("hidden");
    });
  });
}

function adicionarEventosExcluirUsuarios() {
  const botoesExcluir = document.querySelectorAll(".btn-delete-user");

  botoesExcluir.forEach(botao => {
    botao.addEventListener("click", async () => {
      const usuarioId = botao.getAttribute("data-id");
      const confirmar = confirm("Deseja realmente excluir este usuário?");

      if (!confirmar) {
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/users/${usuarioId}`, {
          method: "DELETE",
          headers
        });

        const data = await response.json();

        if (!response.ok) {
          alert(data.error || "Erro ao excluir usuário.");
          return;
        }

        carregarUsuarios();
        carregarCredenciais();

      } catch (error) {
        console.error("Erro ao excluir usuário:", error);
        alert("Erro de conexão com o servidor.");
      }
    });
  });
}

// CREDENCIAIS
async function carregarCredenciais() {
  try {
    listaCredenciais.innerHTML = "<p>Carregando credenciais...</p>";

    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "GET",
      headers
    });

    const data = await response.json();

    if (!response.ok) {
      listaCredenciais.innerHTML = "<p>Erro ao carregar credenciais.</p>";
      return;
    }

    if (data.length === 0) {
      listaCredenciais.innerHTML = "<p>Nenhuma credencial cadastrada.</p>";
      return;
    }

    listaCredenciais.innerHTML = "";

    data.forEach(usuario => {
      const item = document.createElement("div");
      item.classList.add("resource-item");

      const statusTexto = usuario.acesso_ativo ? "Acesso ativo" : "Acesso bloqueado";
      const botaoTexto = usuario.acesso_ativo ? "Revogar acesso" : "Liberar acesso";

      item.innerHTML = `
        <h4>${usuario.nome}</h4>
        <p><strong>Email:</strong> ${usuario.email}</p>
        <p><strong>Cargo:</strong> ${usuario.cargo}</p>
        <p><strong>Status:</strong> ${statusTexto}</p>

        <div class="resource-actions">
          <button class="btn-toggle-access" data-id="${usuario.id}">
            ${botaoTexto}
          </button>
        </div>
      `;

      listaCredenciais.appendChild(item);
    });

    adicionarEventosCredenciais();

  } catch (error) {
    console.error("Erro ao carregar credenciais:", error);
    listaCredenciais.innerHTML = "<p>Erro de conexão com o servidor.</p>";
  }
}

function adicionarEventosCredenciais() {
  const botoesCredenciais = document.querySelectorAll(".btn-toggle-access");

  botoesCredenciais.forEach(botao => {
    botao.addEventListener("click", async () => {
      const usuarioId = botao.getAttribute("data-id");

      try {
        const response = await fetch(`${API_BASE_URL}/users/${usuarioId}/toggle-access`, {
          method: "PATCH",
          headers
        });

        const data = await response.json();

        if (!response.ok) {
          alert(data.error || "Erro ao alterar credencial.");
          return;
        }

        carregarCredenciais();
        carregarUsuarios();

      } catch (error) {
        console.error("Erro ao alterar credencial:", error);
        alert("Erro de conexão com o servidor.");
      }
    });
  });
}

// INICIALIZAÇÃO
carregarRecursos();
carregarUsuarios();
carregarCredenciais();