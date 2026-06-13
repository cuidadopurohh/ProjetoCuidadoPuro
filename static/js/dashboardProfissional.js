document.addEventListener("DOMContentLoaded", () => {
    carregarPacientes();
});

async function carregarPacientes() {
    const cardsGrid = document.getElementById("cardsGridPacientes");
    
    if (!cardsGrid) return;

    try {
        // Realiza a chamada na rota do seu backend que lista os clientes/pacientes
        // Lembre-se de verificar se sua rota se chama /Pacientes, /Clientes ou /Assistidos
        const resposta = await fetch(API_BASE_URL + "/Clientes", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!resposta.ok) {
            throw new Error("Não foi possível obter a lista de pacientes do servidor.");
        }

        const pacientes = await resposta.json();

        // Limpa a grade para evitar repetições indesejadas
        cardsGrid.innerHTML = "";

        if (pacientes.length === 0) {
            cardsGrid.innerHTML = `<p class="sem-dados">Nenhum paciente necessitando de cuidados no momento.</p>`;
            return;
        }

        // Percorre o array retornado pela tabela do banco de dados
        pacientes.forEach(paciente => {
            const card = document.createElement("article");
            card.classList.add("card");

            // Mapeia os dados das propriedades JSON devolvidas pela sua FastAPI.
            // Altere os nomes das variáveis caso os campos da sua tabela sejam diferentes.
            const nome = paciente.nome_paciente || "Paciente Oculto";
            const idade = paciente.idade_paciente || "Não informada";
            const nivelSuporte = paciente.nivel_suporte || "A combinar";
            const fotoPerfil = paciente.foto_url || "../cuidadopuro_teste/img/Design sem nome (2).png";
            const avaliacao = paciente.avaliacao_cadastro || "5.0";

            card.innerHTML = `
                <img src="${fotoPerfil}" alt="Perfil de ${nome}">
                <div class="info">
                    <h3>${nome}</h3>
                    <p class="meta">${idade} anos · ${nivelSuporte}</p>
                    <p class="rating">⭐ ${avaliacao}</p>
                    <a href="#" class="btn" onclick="verPerfilPaciente(${paciente.id})">Ver perfil</a>
                </div>
            `;

            cardsGrid.appendChild(card);
        });

    } catch (erro) {
        console.error("Erro ao processar o carregamento da lista de pacientes:", erro);
        cardsGrid.innerHTML = `<p class="erro-dados">Houve um problema ao carregar os painéis de pacientes. Tente recarregar a página.</p>`;
    }
}

function verPerfilPaciente(id) {
    console.log("Exibindo perfil detalhado do paciente com ID:", id);
    // Próximo passo opcional: window.location.href = `detalhesPaciente.html?id=${id}`;
}
