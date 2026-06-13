/**
 * 📢 INTEGRAÇÃO DINÂMICA DA DASHBOARD (CUIDADO PURO):
 * - Consome: GET /Profissionais (ou a rota equivalente do seu monolito)
 * - Renderiza os cards de cuidadores em tempo real a partir do banco de dados.
 */

document.addEventListener("DOMContentLoaded", () => {
    carregarCuidadores();
});

async function carregarCuidadores() {
    const cardsGrid = document.getElementById("cardsGridCuidadores");
    
    if (!cardsGrid) return;

    try {
        // Envia uma requisição GET para puxar todos os profissionais cadastrados
        // API_BASE_URL vem do seu arquivo config.js
        const resposta = await fetch(API_BASE_URL + "/Profissionais", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!resposta.ok) {
            throw new Error("Erro ao coletar dados de profissionais do servidor.");
        }

        const profissionais = await resposta.json();

        // Limpa o contêiner (garantia contra duplicações)
        cardsGrid.innerHTML = "";

        if (profissionais.length === 0) {
            cardsGrid.innerHTML = `<p class="sem-dados">Nenhum cuidador cadastrado no momento.</p>`;
            return;
        }

        // Mapeia e renderiza cada profissional vindo da tabela do banco de dados
        profissionais.forEach(profissional => {
            const card = document.createElement("article");
            card.classList.add("card");

            // Mapeia os dados baseados nos campos do seu banco de dados
            // Caso sua tabela use nomes ligeiramente diferentes (ex: anos_experiencia), ajuste abaixo:
            const nome = profissional.nome_profissional || "Profissional";
            const idade = profissional.idade_profissional || "Não informada";
            const experiencia = profissional.tempo_experiencia || "0";
            const fotoPerfil = profissional.foto_url || "../cuidadopuro_teste/img/Design sem nome (2).png";
            const avaliacao = profissional.avaliacao || "5.0";

            card.innerHTML = `
                <img src="${fotoPerfil}" alt="Perfil de ${nome}">
                <div class="info">
                    <h3>${nome}</h3>
                    <p class="meta">${idade} anos · ${experiencia} anos de experiência</p>
                    <p class="rating">⭐ ${avaliacao}</p>
                    <a href="#" class="btn" onclick="verPerfil(${profissional.id})">Ver perfil</a>
                </div>
            `;

            cardsGrid.appendChild(card);
        });

    } catch (erro) {
        console.error("Erro na busca de cuidadores:", erro);
        cardsGrid.innerHTML = `<p class="erro-dados">Não foi possível carregar a lista de cuidadores. Tente novamente mais tarde.</p>`;
    }
}

// Função stub caso queira expandir para abrir detalhes do cuidador no futuro
function verPerfil(id) {
    console.log("Abrindo perfil do cuidador de ID:", id);
    // Aqui você pode redirecionar para uma tela de detalhes: window.location.href = `perfilCuidador.html?id=${id}`;
}
