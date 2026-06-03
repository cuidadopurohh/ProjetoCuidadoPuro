/**
 * 📢 AVISO IMPORTANTE PARA O BACKEND:
 * 1. ROTA DE DESTINO: POST http://127.0.0.1:8000/Clientes
 * 2. MUDANÇAS E TRATAMENTO DE DADOS:
 * - Este arquivo gerencia especificamente o Questionário de Saúde (2ª etapa).
 * - Para evitar quebras, o campo 'idade_paciente' já está sendo convertido automaticamente
 * para Número Inteiro (int) usando `parseInt()` antes de disparar a requisição.
 * - ATENÇÃO AOS NOMES: Para este formulário de triagem clínica, mudamos as chaves para 
 * 'nome_paciente' e 'idade_paciente' (no cadastro.js antigo era 'nome_cliente').
 * * 3. ESTRUTURA DO JSON ENVIADO (CONTRATO):
 * {
 * "nome_paciente": "Texto completo",
 * "idade_paciente": 78, (Enviado como INT/Número)
 * "condicao_principal": "Texto do select (Ex: 'idoso-limitacao', 'pos-cirurgico')",
 * "nivel_suporte": "Texto do radio (Ex: 'basico', 'intermediario', 'intensivo')",
 * "observacoes_cuidados": "Texto longo da textarea (alergias/restrições)"
 * }
 * 4. Eu testei o js com um backend falso sem rota de destino e esta 100% CORRETO
 */

document.addEventListener("DOMContentLoaded", () => {
    const formPaciente = document.getElementById("formPaciente");

    if (formPaciente) {
        formPaciente.addEventListener("submit", async (e) => {
            e.preventDefault();

            // Captura o rádio button que estiver selecionado no momento do envio
            const suporteSelecionado = document.querySelector('input[name="nivel-suporte"]:checked');

            // Monta o objeto com os dados REAIS do formulário do paciente
            const dados = {
                nome_paciente: document.getElementById("paciente-nome").value,
                idade_paciente: parseInt(document.getElementById("paciente-idade").value),
                condicao_principal: document.getElementById("condicao-principal").value,
                nivel_suporte: suporteSelecionado ? suporteSelecionado.value : null,
                observacoes_cuidados: document.getElementById("observacoes").value
            };

            // =========================================================================
            // SE QUISER TESTAR LOCALMENTE SEM BACKEND:
            // Descomente as duas linhas abaixo (remova as duas barras //) e comente o bloco try/catch
            // console.log("=== DADOS DO PACIENTE CAPTURADOS ===");
            // console.dir(dados); return;
            // =========================================================================

            try {
                // Envia os dados para a rota do seu backend para Clientes/Pacientes
                const resposta = await fetch("http://127.0.0.1:8000/Clientes", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json" 
                    },
                    body: JSON.stringify(dados)
                });

                const resultado = await resposta.json();

                if (resposta.ok) {
                    alert("Questionário de saúde do paciente enviado com sucesso!");
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