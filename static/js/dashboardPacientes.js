/**
 * 📢 INTEGRAÇÃO DINÂMICA DA DASHBOARD (CUIDADO PURO):
 * - Consome: GET /Profissionais
 * - Renderiza os cards de cuidadores em tempo real com filtros combinados.
 */

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

        listaProfissionais = await resposta.json();
        renderizarCards(listaProfissionais);

    } catch (erro) {
        console.error("Erro na busca de cuidadores:", erro);
        cardsGrid.innerHTML = `<p class="erro-dados">Não foi possível carregar a lista de cuidadores. Tente novamente mais tarde.</p>`;
    }
}

// 2. Desenha os cards na tela
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
        const localizacao = profissional.endereco_profissional || "Não informado";
        const id = profissional.id_profissional || profissional.id;

        card.innerHTML = `
            <img src="${fotoPerfil}" alt="Perfil de ${nome}">
            <div class="info">
                <h3>${nome}</h3>
                <p class="meta">${idade} anos · ${experiencia} anos de exp.</p>
                <p class="meta-sub">${localizacao}</p>
                <p class="rating">⭐ ${avaliacao}</p>
                <a href="#" class="btn" onclick="verPerfil(${id})">Ver perfil</a>
            </div>
        `;
        cardsGrid.appendChild(card);
    });
}

// 3. Configura os listeners para escutar mudanças nos campos
function configurarEventosDeBusca() {
    const inputBusca = document.getElementById("inputBusca");
    const selectEspecialidade = document.getElementById("selectEspecialidade");
    const selectCidade = document.getElementById("selectCidade");
    const btnBuscar = document.getElementById("btnBuscar");

    if (inputBusca) inputBusca.addEventListener("input", filtrarProfissionais);
    if (selectEspecialidade) selectEspecialidade.addEventListener("change", filtrarProfissionais);
    if (selectCidade) selectCidade.addEventListener("change", filtrarProfissionais);

    if (btnBuscar) {
        btnBuscar.addEventListener("click", (e) => {
            e.preventDefault();
            filtrarProfissionais();
        });
    }
}

// 4. Regra de filtragem robusta
function filtrarProfissionais() {
    const termoBusca = document.getElementById("inputBusca").value.toLowerCase().trim();
    const especialidadeSelecionada = document.getElementById("selectEspecialidade").value;
    const cidadeSelecionada = document.getElementById("selectCidade").value;

    const profissionaisFiltrados = listaProfissionais.filter(profissional => {
        
        const nome = (profissional.nome_profissional || "").toLowerCase();
        const endereco = (profissional.endereco_profissional || "").toLowerCase();
        const especialidade = (profissional.especialidade_principal || "").toLowerCase();

        // Regra 1: Input de Texto Livre
        const bateTexto = termoBusca === "" || 
                          nome.includes(termoBusca) || 
                          endereco.includes(termoBusca) || 
                          especialidade.includes(termoBusca);

        // Regra 2: Select de Especialidade (Usa includes para evitar erros de strings levemente diferentes)
        const bateEspecialidade = especialidadeSelecionada === "todos" || 
                                  especialidade.includes(especialidadeSelecionada.toLowerCase());

        // Regra 3: Select de Cidade (Varre o endereço completo buscando a cidade)
        const bateCidade = cidadeSelecionada === "todos" || 
                           endereco.includes(cidadeSelecionada.toLowerCase());

        return bateTexto && bateEspecialidade && bateCidade;
    });

    renderizarCards(profissionaisFiltrados);
}

function verPerfil(id) {
    console.log("Abrindo perfil do cuidador de ID:", id);
}
