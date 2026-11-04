# Especificação — ficha por documento e narrativa do processo (AGERGS, celebração de convênio/contrato de regulação)

Adaptação do prompt `metodologia-repo/scripts/fichas_trabalho.py` (ficha-v2) ao caso AGERGS-RS.
Contexto: a AGERGS (Agência Estadual de Regulação dos Serviços Públicos Delegados do RS) recebe, por convênio ou
contrato de prestação de serviços de regulação, a delegação municipal da regulação (em geral saneamento — água e esgoto,
prestados pela CORSAN ou outro prestador). Cada processo SEI aqui é a celebração (ou tentativa) de um desses instrumentos.

Entradas: `dados/documentos.csv` (uma linha por documento: processo, seq, doc_id, nome, páginas, datas de assinatura),
`dados/assinaturas.csv` (signatário, cargo, data) e o texto de cada peça em `dados/docs/<processo>/<seq>_<doc_id>.txt`.

## Regras obrigatórias
1. Só o que o texto diz. Cada "evidencia" é um trecho COPIADO LITERALMENTE do documento (10 a 160 caracteres, sem
   reescrever, sem reticências). Sem trecho literal, o item não entra.
2. Trabalho próprio × reproduzido (na dúvida, reproduzido).
3. Nada de número inventado: datas só as que aparecem no texto ou no CSV. Horas estimadas são HIPÓTESE (marcar).
4. Documento externo (ofício do município, lei municipal, plano de saneamento, contrato da CORSAN, certidões):
   ficha curta — autoria "externo", atividade, entregável, data se houver; não precisa de competências/horas.
5. Documento muito longo (> 300 linhas): leia o início (~150 linhas), o fim (~60 linhas) e procure por palavras-chave;
   não leia anexos técnicos inteiros.
6. Não reproduza dados pessoais além de nome+cargo do signatário (CPF, endereço, telefone, e-mail: nunca).

## Saída 1 — `dados/fichas/<processo>.jsonl` (uma linha JSON por documento, na ordem de seq)
{"processo": "...", "seq": 1, "doc_id": "...", "nome": "...", "autoria": "AGERGS"|"externo",
 "unidade": "unidade/cargo autor (ex.: 'Diretoria de Assuntos Jurídicos', 'Gabinete da Presidência', 'Município', 'Procuradoria Setorial PGE', 'Conselho Superior', 'Diretoria-Geral', 'DQS', 'DSI', 'Expediente/Protocolo')",
 "destino": "a quem encaminha, ou null", "data": "AAAA-MM-DD ou null",
 "atividade": um de ATIVIDADES (abaixo), "tarefa": "verbo no infinitivo + objeto, até 8 palavras",
 "entregavel": "...", "conclusao_de_merito": "... ou null",
 "natureza_trabalho": um de ["encaminhamento","comunicacao","instrucao_processual","analise_juridica","analise_tecnica_engenharia","analise_economico_financeira","auditoria_conferencia","relatoria_decisao","publicacao_registro","documento_externo"],
 "insumos": [{"tipo": "documento_do_processo|documento_do_municipio|norma_ou_contrato|base_externa|sistema_ou_base_interna|precedente", "descricao": "...", "evidencia": "trecho literal"}],
 "normas_citadas": [{"norma": "ex.: Lei Estadual 10.931/1997, art. 2º", "evidencia": "trecho literal"}],
 "complexidade": 1-5 (1 expediente; 2 comunicação/instrução simples; 3 análise de poucas peças com conclusão; 4 análise cruzada/posições divergentes; 5 modelagem/revisão metodológica),
 "horas_estimadas": número (HIPÓTESE; trabalho de servidor experiente, sem espera) ou null para externo,
 "composicao_texto": {"pct_autoral": n, "pct_transcricao": n, "pct_padrao": n},
 "sinais_perda": [{"tipo": "pedido_complementacao|devolucao_por_vicio|refazimento|reiteracao|aguardando_outra_unidade|diligencia_externa|sobrestamento|prazo_concedido", "evidencia": "trecho literal"}],
 "prazos": [{"dias": n, "beneficiario": "municipio|unidade_interna|prestador|orgao_externo", "evidencia": "trecho literal"}],
 "observacao": "até 2 frases, opcional"}

ATIVIDADES = solicitacao_municipio | autuacao_abertura | juntada_documentos_municipio | lei_autorizativa |
 encaminhamento_interno | analise_juridica | manifestacao_pge | analise_tecnica | analise_economico_financeira |
 elaboracao_minuta | revisao_ajuste_minuta | inexigibilidade_licitacao | deliberacao_conselho_superior |
 decisao_presidencia_diretoria | envio_minuta_ao_municipio | tratativa_com_municipio | assinatura_instrumento |
 publicacao_extrato | comunicacao_prestador | comunicacao_interna_pos_assinatura | cadastro_controle |
 cobranca_taxa_financeiro | aditivo_alteracao | arquivamento_encerramento | documento_externo_anexo | outro

## Saída 2 — `dados/narrativas/<processo>.json`
{"processo": "...", "numero_sei": "...", "municipio": "...", "instrumento": "convenio_delegacao|contrato_prestacao_servicos_regulacao|aditivo|outro",
 "servico": "agua_esgoto|residuos|outro", "prestador": "...", "fundamento_legal": ["..."],
 "situacao_final": "assinado_e_publicado|assinado_sem_publicacao_no_processo|aguardando_municipio|aguardando_agergs|arquivado_sem_celebracao|indeterminado",
 "evidencia_situacao": "trecho literal ou seq do documento",
 "marcos": [{"marco": "pedido_municipio|lei_autorizativa|abertura|parecer_juridico|manifestacao_pge|aprovacao_conselho|minuta_enviada|assinatura_municipio|assinatura_agergs|publicacao|comunicacao_prestador|encerramento", "seq": n, "data": "AAAA-MM-DD ou null"}],
 "sequencia_etapas": ["atividade em ordem, usando ATIVIDADES"],
 "unidades_envolvidas": ["..."],
 "desvios_e_retrabalho": [{"descricao": "...", "seq": [n], "evidencia": "trecho literal"}],
 "gargalos_percebidos": ["frase curta com seq de apoio"],
 "documentos_exigidos_do_municipio": ["..."],
 "diferencas_vs_padrao": "como este processo difere de um fluxo-padrão (pedido → análise jurídica → minuta → aprovação → assinatura → publicação)",
 "observacoes": "..."}
