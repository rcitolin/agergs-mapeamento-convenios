# Dados levantados — inventário, fonte, confiança e o que obter na AGERGS

| Dado | Fonte | Script / arquivo | Confiança | O que obter na AGERGS |
|---|---|---|---|---|
| Peças de cada processo (nome, id SEI, páginas, texto) | 20 PDFs exportados do SEI-RS | `base_documentos.py` → `dados/documentos.csv`, `dados/docs/` | Alta para peças nativas; baixa para 33 peças digitalizadas (`baixo_texto`) | OCR das peças digitalizadas; segmentação com rodapé sem parênteses |
| Data e signatário (cargo) de cada assinatura | Tarja "Documento assinado eletronicamente" | `dados/assinaturas.csv` | Alta | — |
| Unidade de cada peça | Cargo do signatário (regra `CARGO_UNIDADE`) ou unidade lida na ficha | `pipeline_agergs.py` | Média ("Especialista em Regulação" não indica a unidade) | Lotação dos signatários |
| **Andamentos (tramitação, posse por unidade)** | **Não disponível** nos PDFs | — | — | **Relatório de andamentos do SEI-RS** (pesquisa ou banco) dos 18 processos de celebração, para medir fila e posse reais |
| Atividade, natureza, complexidade e sinais de perda por peça | Fichas por agente, evidência literal | `dados/fichas/`, `saida/fichas_trabalho.*` | Média: ancoragem 100%, rótulo 81,6% às cegas nas substantivas (2 rodadas, 97 peças) | Validar as 18 divergências pendentes |
| Horas por peça (piso–teto) | Regra de `comum.py` (horas-base por natureza, laudas × coeficiente) | `pipeline_agergs.py` (`esforco`) | **Hipótese** | Medição de tempo de algumas peças-tipo (parecer, minuta, ofício) |
| Situação final, desvios, marcos | Narrativas dos agentes | `dados/narrativas/` | Média | Confirmar processos sem publicação nos autos (Alecrim, Arambaré, Campinas das Missões, Panambi, Passa Sete) e os pendentes (Capão Bonito do Sul, Mampituba, Unistalda) |
| Linha do tempo, fatos, procedimento da coorte | Código | `saida/fase2/casos_CONV.json`, `saida/bpmn/fatos_CONV.json`, `procedimento_CONV.json` | Alta como cálculo; limitada pela ausência de andamentos | — |
| Normas e requisitos | Texto integral baixado | `normas/`, `saida/fase3/normas_CONV.json` | Alta para normas federais (Planalto); **média** para as RS (fonte secundária) | Texto oficial do DOE-RS das Leis 16.266/2024 e 15.612/2021; Regimento Interno da AGERGS (rito do Conselho Superior); resolução da taxa de regulação |
| Conformidade | Testes por caso | `saida/fase3/conformidade_CONV.*` | Média: presença de peça nos autos, não exame de conteúdo | Confirmar se inexigibilidade e autorização estão em processo-mãe |
| Benchmarking | Agente com URLs | `dados/referencia/benchmark.*` | Média: sem verificação independente; nenhum ganho numérico | Convênios e contratos de AGESAN-RS, ARIS e AGIR; lista ANA de entidades aderentes |
| Processo orientativo e minuta padrão | SEI 002594-39.00/26-9 e 002840-39.00/26-3 | `dados/referencia/` | Alta (evidência literal) | Versão aprovada do fluxo e da minuta |
| **Volume anual de celebrações** | **Hipótese: 5** (casos de 2025 na amostra) | `fase3_agergs.py` (`VOLUME_ANUAL`) | **Hipótese** | **Cadastro de municípios conveniados** (data de assinatura, instrumento, situação) e fila de pedidos em análise |
| **Custo-hora** | **Hipótese:** R$ 55 / 88 / 121 (piso/esperado/teto) | `CUSTO_HORA` | **Hipótese** | Tabela de vencimentos e encargos por cargo (Especialista e Assistente de Regulação, assessores) |
| Datas de instrumentos antigos (2013–2016) | Texto das peças (sem assinatura eletrônica) | `pipeline_agergs.py` | Baixa: datas com erro no texto (Campinas) | Data real de assinatura e publicação dos convênios anteriores ao SEI |
| Custo de desenvolvimento e frações automatizáveis | Premissas do repositório (`comum.py`) | `fase3_agergs.py` (fase 4) | **Hipótese** | Contrato ou estimativa da DTI |
