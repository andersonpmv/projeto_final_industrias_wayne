const API_BASE_URL = "http://127.0.0.1:5000";

const token = localStorage.getItem("token");
const cargo = localStorage.getItem("cargo");

const dashboardContainer = document.getElementById("dashboard-container");
const erroBox = document.getElementById("erro-box");
const container = document.querySelector(".container");
const adminBtn = document.getElementById("admin-btn");

let graficoAreas = null;

if (!token) {
  window.location.href = "login.html";
  throw new Error("Token não encontrado");
}

const headers = {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
};

function mostrarErroDashboard(mensagem) {
  erroBox.textContent = mensagem;
  erroBox.style.display = "block";
}

function limparErroDashboard() {
  erroBox.textContent = "";
  erroBox.style.display = "none";
}

function ativarLoading() {
  container.classList.add("loading");
}

function desativarLoading() {
  container.classList.remove("loading");
}

function redirecionarParaLogin(mensagem) {
  localStorage.removeItem("token");
  localStorage.removeItem("cargo");
  localStorage.removeItem("nome");

  window.location.href = "login.html";
  throw new Error(mensagem);
}

function configurarBotaoAdmin() {
  if (!adminBtn) {
    return;
  }

  if (cargo !== "admin") {
    adminBtn.style.display = "none";
    return;
  }

  adminBtn.addEventListener("click", () => {
    window.location.href = "admin.html";
  });
}

async function carregarResumoDashboard() {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/summary`, {
      method: "GET",
      headers
    });

    if (response.status === 401 || response.status === 403) {
      redirecionarParaLogin("Sessão inválida ou sem permissão.");
    }

    if (!response.ok) {
      throw new Error("Erro ao carregar resumo do dashboard.");
    }

    const data = await response.json();

    document.getElementById("total-logs").textContent = data.total_logs;
    document.getElementById("total-permitidos").textContent = data.total_permitidos;
    document.getElementById("total-negados").textContent = data.total_negados;

    document.getElementById("area-mais-acessada").textContent =
      data.area_mais_acessada ? data.area_mais_acessada.nome : "-";

    document.getElementById("total-usuarios").textContent = data.total_usuarios;
    document.getElementById("usuarios-ativos").textContent = data.usuarios_ativos;
    document.getElementById("usuarios-bloqueados").textContent = data.usuarios_bloqueados;
    document.getElementById("total-recursos").textContent = data.total_recursos;
    document.getElementById("total-areas").textContent = data.total_areas;

    renderizarGraficoAreas(data.acessos_por_area || []);

  } catch (error) {
    console.error("Erro no resumo do dashboard:", error);
    mostrarErroDashboard("Erro ao carregar os dados do dashboard.");
  }
}

async function carregarAlertasSeguranca() {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/security-alerts`, {
      method: "GET",
      headers
    });

    if (response.status === 401 || response.status === 403) {
      redirecionarParaLogin("Sessão inválida ou sem permissão.");
    }

    if (!response.ok) {
      throw new Error("Erro ao carregar alertas de segurança.");
    }

    const data = await response.json();

    const usuariosLista = document.getElementById("usuarios-suspeitos");
    const areasLista = document.getElementById("areas-sensiveis");

    usuariosLista.innerHTML = "";
    areasLista.innerHTML = "";

    if (!data.usuarios_suspeitos || data.usuarios_suspeitos.length === 0) {
      usuariosLista.innerHTML = "<li>Nenhum usuário suspeito encontrado.</li>";
    } else {
      data.usuarios_suspeitos.forEach(usuario => {
        const li = document.createElement("li");

        li.textContent =
          `${usuario.nome} | Negados: ${usuario.negados} | Tentativas: ${usuario.total_tentativas} | Taxa: ${usuario.taxa_negacao}%`;

        usuariosLista.appendChild(li);
      });
    }

    if (!data.areas_sensiveis || data.areas_sensiveis.length === 0) {
      areasLista.innerHTML = "<li>Nenhuma área sensível encontrada.</li>";
    } else {
      data.areas_sensiveis.forEach(area => {
        const li = document.createElement("li");
        li.textContent = `${area.area} | Negados: ${area.negados}`;
        areasLista.appendChild(li);
      });
    }

  } catch (error) {
    console.error("Erro nos alertas de segurança:", error);
    mostrarErroDashboard("Erro ao carregar alertas de segurança.");
  }
}

function renderizarGraficoAreas(acessosPorArea) {
  const canvas = document.getElementById("areasChart");

  if (!canvas) {
    return;
  }

  const ctx = canvas.getContext("2d");

  const labels = acessosPorArea.map(item => item.area);
  const valores = acessosPorArea.map(item => item.quantidade);

  if (graficoAreas) {
    graficoAreas.destroy();
  }

  graficoAreas = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Quantidade de acessos",
        data: valores
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          labels: {
            color: "white"
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: "white"
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "white",
            precision: 0
          }
        }
      }
    }
  });
}

document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("cargo");
  localStorage.removeItem("nome");

  window.location.href = "login.html";
});

async function iniciarDashboard() {
  limparErroDashboard();
  ativarLoading();
  configurarBotaoAdmin();

  try {
    await carregarResumoDashboard();
    await carregarAlertasSeguranca();

    dashboardContainer.classList.remove("hidden");

  } catch (error) {
    console.error("Erro ao iniciar dashboard:", error);

  } finally {
    desativarLoading();
  }
}

iniciarDashboard();