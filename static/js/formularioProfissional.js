/**
 * 📢 AVISO IMPORTANTE PARA O BACKEND:
 * 1. ROTA DE DESTINO: POST http://127.0.0.1:8000/Profissionais
 * 2. MUDANÇA EM RELAÇÃO AO 'cadastro.js' ANTIGO: 
 * - Este arquivo gerencia especificamente o Questionário de Competências (2ª etapa).
 * - Não estamos mais enviando os dados de cadastro inicial (nome, cpf, email, senha).
 * - Os campos abaixo foram totalmente mapeados de acordo com o formulário HTML real.
 * * 3. ESTRUTURA DO JSON ENVIADO (CONTRATO):
 * {
 * "registro_profissional": "Texto (Ex: COREN/COFFITO)",
 * "tempo_experiencia": "Texto do select (Ex: 'menos-1', '1-3', '3-5', 'mais-5')",
 * "especialidade_principal": "Texto do radio (Ex: 'geriatria', 'complexo', 'pcd')",
 * "procedimentos_dispositivos": "Texto do select (Ex: 'sondas', 'oxigenio', 'curativos')",
 * "detalhes_capacitacao": "Texto longo digitado na textarea"
 * }
 * 4. Eu testei o js com um backend falso sem rota de destino e esta 100% CORRETO
 */

document.addEventListener("DOMContentLoaded", () => {
    const formProfissional = document.getElementById("formProfissional");

    if (formProfissional) {
        formProfissional.addEventListener("submit", async (e) => {
            e.preventDefault();

            const especialidadeSelecionada = document.querySelector('input[name="especialidade-principal"]:checked');

            // Formato oficial validado pelo seu teste
            const dados = {
                registro_profissional: document.getElementById("prof-registro").value,
                tempo_experiencia: document.getElementById("prof-experiencia").value,
                especialidade_principal: especialidadeSelecionada ? especialidadeSelecionada.value : null,
                procedimentos_dispositivos: document.getElementById("prof-dispositivos").value,
                detalhes_capacitacao: document.getElementById("prof-detalhes").value
            };

            try {
                // Rota que vai conversar diretamente com o servidor do seu colega
                const resposta = await fetch(API_BASE_URL + "/Profissionais", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json" 
                    },
                    body: JSON.stringify(dados)
                });

                const resultado = await resposta.json();

                if (resposta.ok) {
                    alert("Questionário do profissional enviado com sucesso!");
                    window.location.href = "telaLogin.html";
                } else {
                    alert("Erro no cadastro: " + (resultado.detail || "Verifique as informações."));
                }
            } catch (erro) {
                alert("Não foi possível conectar ao servidor. O backend está ligado?");
                console.error("Erro na requisição:", erro);
            }
        });
    }
});