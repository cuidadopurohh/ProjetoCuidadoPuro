/**
 * 📢 INTEGRAÇÃO DINÂMICA DA DASHBOARD (CUIDADO PURO):
 * - Consome: GET /Profissionais (ou a rota equivalente do seu monolito)
 * - Renderiza os cards de cuidadores em tempo real a partir do banco de dados.
 */

// Variável global para armazenar os dados brutos vindos da tabela do Banco de Dados
let listaProfissionais = [];

document.addEventListener("DOMContentLoaded", () => {
    carregarCuidadores();
    configurarEventosDeBusca();
});

// 1. Busca os dados iniciais na API FastAPI
async function carregarCuidadores() {
    const cardsGrid = document.getElementById("cardsGridCuidadores");
    if (!cardsGrid) return;

    try {
        const resposta = await fetch(API_BASE_URL + "/Profissionais", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!resposta.ok) {
            throw new Error("Erro ao coletar dados de profissionais do servidor.");
        }

        // Alimenta a variável global com o array do banco
        listaProfissionais = await resposta.json();

        // Renderiza todos os profissionais de início
        renderizarCards(listaProfissionais);

    } catch (erro) {
        console.error("Erro na busca de cuidadores:", erro);
        cardsGrid.innerHTML = `<p class="erro-dados">Não foi possível carregar a lista de cuidadores. Tente novamente mais tarde.</p>`;
    }
}

// 2. Função responsável exclusivamente por desenhar os cards na tela
function renderizarCards(profissionais) {
    const cardsGrid = document.getElementById("cardsGridCuidadores");
    if (!cardsGrid) return;

    cardsGrid.innerHTML = "";

    if (profissionais.length === 0) {
        cardsGrid.innerHTML = `<p class="sem-dados">Nenhum cuidador corresponde aos filtros selecionados.</p>`;
        return;
    }

    profissionais.forEach(profissional => {
        const card = document.createElement("article");
        card.classList.add("card");

        const nome = profissional.nome_profissional || "Profissional";
        const idade = profissional.idade_profissional || "Não informada";
        const experiencia = profissional.tempo_experiencia || "0";
        const fotoPerfil = profissional.foto_url || "../cuidadopuro_teste/img/Design sem nome (2).png";
        const avaliacao = profissional.avaliacao || "5.0";
        const cidade = profissional.cidade || "Não informada";

        card.innerHTML = `
            <img src="${fotoPerfil}" alt="Perfil de ${nome}">
            <div class="info">
                <h3>${nome}</h3>
                <p class="meta">${idade} anos · ${experiencia} anos de exp.</p>
                <p class="meta-sub">${cidade}</p>
                <p class="rating">⭐ ${avaliacao}</p>
                <a href="#" class="btn" onclick="verPerfil(${profissional.id})">Ver perfil</a>
            </div>
        `;
        cardsGrid.appendChild(card);
    });
}

// 3. Monitora o que o usuário digita ou seleciona
function configurarEventosDeBusca() {
    const inputBusca = document.getElementById("inputBusca");
    const selectEspecialidade = document.getElementById("selectEspecialidade");
    const selectCidade = document.getElementById("selectCidade");
    const btnBuscar = document.getElementById("btnBuscar");

    // Filtra em tempo real enquanto digita
    if (inputBusca) inputBusca.addEventListener("input", filtrarProfissionais);
    
    // Filtra imediatamente ao alterar um Select
    if (selectEspecialidade) selectEspecialidade.addEventListener("change", filtrarProfissionais);
    if (selectCidade) selectCidade.addEventListener("change", filtrarProfissionais);

    // Evita comportamento padrão se clicarem no botão Buscar
    if (btnBuscar) {
        btnBuscar.addEventListener("click", (e) => {
            e.preventDefault();
            filtrarProfissionais();
        });
    }
}

// 4. Regra de filtragem lógica combinada
function filtrarProfissionais() {
    const termoBusca = document.getElementById("inputBusca").value.toLowerCase().trim();
    const especialidadeSelecionada = document.getElementById("selectEspecialidade").value;
    const cidadeSelecionada = document.getElementById("selectCidade").value;

    // Aplica as regras de filtro sobre o array global na memória
    const profissionaisFiltrados = listaProfissionais.filter(profissional => {
        
        // Dados do banco normalizados para caixa baixa (evitar problemas de maiúsculas/minúsculas)
        const nome = (profissional.nome_profissional || "").toLowerCase();
        const cidadeProfissional = (profissional.cidade || "").toLowerCase();
        const especialidade = (profissional.especialidade || "").toLowerCase();

        // Regra 1: Input de Texto (Nome, Cidade ou Especialidade)
        const bateTexto = termoBusca === "" || 
                          nome.includes(termoBusca) || 
                          cidadeProfissional.includes(termoBusca) || 
                          especialidade.includes(termoBusca);

        // Regra 2: Select de Especialidade
        const bateEspecialidade = especialidadeSelecionada === "todos" || 
                                  profissional.especialidade === especialidadeSelecionada;

        // Regra 3: Select de Cidade
        const bateCidade = cidadeSelecionada === "todos" || 
                           profissional.cidade === cidadeSelecionada;

        // Retorna o profissional apenas se passar em TODAS as 3 condições ao mesmo tempo
        return bateTexto && bateEspecialidade && bateCidade;
    });

    // Redesenha a tela apenas com os resultados filtrados
    renderizarCards(profissionaisFiltrados);
}

function verPerfil(id) {
    console.log("Abrindo perfil do cuidador de ID:", id);
}
