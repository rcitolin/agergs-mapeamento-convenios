# Benchmark TO-BE: celebração de convênios de delegação de regulação de saneamento (AGERGS)

Gerado em 2026-11-04. Dados completos em `benchmark.json` (13 práticas, todas com URL aberta).

| id | prática | onde | etapa | fonte |
|---|---|---|---|---|
| BM-01 | Manifestação jurídica referencial (ON AGU 55/2014): dispensa de análise jurídica individual quando a área técnica atesta enquadramento | AGU / PGFN (Parecer Referencial CCA/PGFN 07/2020) | Análise jurídica da minuta/instrução do convênio (parecer da Procuradoria) | documento_oficial |
| BM-02 | Parecer referencial sobre minutas padronizadas de convênio, com dispensa de análise individualizada | Ministério da Saúde / CONJUR-MS (CGU/AGU) - Parecer Referencial nº 00002/2025 | Minuta padrão de convênio + parecer jurídico referencial | documento_oficial |
| BM-03 | Uso obrigatório/recomendado de minutas padronizadas AGU, com justificativa e juntada aos autos se houver alteração | Ministério da Saúde / CONJUR-MS (citando Portaria CGU 03/2019 art. 18 e Enunciado BPC 06) | Elaboração da minuta do convênio | documento_oficial |
| BM-04 | Convênio de cooperação com conteúdo mínimo legal para delegação da regulação (autorização expressa do titular) | ARSAE-MG / Lei estadual MG 18.309/2009 art. 5º §3º (redação da Lei 25.669/2025) | Checklist de cláusulas da minuta / instrução da adesão | norma |
| BM-05 | Delegação da regulação por convênio com lei municipal autorizativa e taxa paga pelo prestador | AGR-GO / Convênio nº 13/2022 (município de Goiás) | Instrução: documentação mínima (lei autorizativa, PMSB, contrato) e minuta | documento_oficial |
| BM-06 | Publicação do convênio em prazo fixo (30 dias da assinatura) e comunicação à Câmara Municipal | AGR-GO / Convênio nº 13/2022 cláusula sétima | Publicação e comunicação pós-assinatura (prazo/SLA) | documento_oficial |
| BM-07 | Convênio-padrão de cooperação técnica entre agência e municípios de bloco regional (URAE), vinculado ao contrato de concessão e com vigência atrelada a ele | ARSESP / URAE 1 Sudeste - Convênio SEI 0049477828 (processo 133.00002671/2024-58) | Minuta padrão do convênio / vigência | documento_oficial |
| BM-08 | Procedimento nacional de comprovação de adoção das normas de referência pela entidade reguladora (condição de acesso a recursos federais) | ANA / Lei 9.984/2000 art. 4º-B (incl. Lei 14.026/2020) e Resolução ANA 134/2022 | Comunicação/registro junto à ANA; pré-requisito de elegibilidade da agência | norma |
| BM-09 | Delegação da regulação a agência de outro Estado condicionada à inexistência de agência estadual aderente às normas ANA | Lei 11.445/2007 art. 23 §§1º, 1º-A, 1º-B | Instrução: justificativa da escolha da agência | norma |
| BM-10 | Instrução padronizada de contratação direta (art. 72) e publicidade do ato; inexigibilidade (art. 74) | Lei 14.133/2021 arts. 72 e 74 | Enquadramento jurídico e checklist de instrução (art. 72) | norma |
| BM-11 | Modelos de minutas padronizados com apoio do jurídico previstos como obrigação de governança das contratações | Lei 14.133/2021 art. 19, IV | Minuta padrão aprovada previamente pelo jurídico | norma |
| BM-12 | Lista pública da ANA das entidades reguladoras que comprovaram adoção das normas de referência, com ciclo anual de comprovação | ANA (reportagem da Agência iNFRA sobre o ciclo 2025) | Comunicação à ANA / lista de entidades reguladoras | noticia_secundaria |
| BM-13 | Cadastro de usuário externo no SEI com liberação em até cinco dias úteis, para assinatura eletrônica por quem é externo ao órgão | MGI (SEI/MGI) - página Usuário Externo | Assinatura eletrônica pelo município (SEI usuário externo/gov.br) | site_institucional |

## Leitura por foco
- (a) Adesão padronizada/documentação mínima: BM-04, BM-05, BM-09, BM-10.
- (b) Minuta padrão e parecer referencial: BM-01, BM-02, BM-03, BM-07, BM-11.
- (c) Assinatura eletrônica: BM-13.
- (d) Prazos e SLA: BM-06, BM-13.
- (e) Publicação e comunicação ANA: BM-06, BM-08, BM-12.

## Ressalvas
Nenhum ganho numérico reportado pelas fontes. BM-12 é fonte secundária (notícia).

## Lacunas
- AGESAN-RS: página de convênios aberta (https://www.agesan-rs.com.br/documentacao/convenios/) lista 8 convênios e 'Protocolo de Intenções', mas só links para PDFs; não li modelo nem rito de adesão. Pendente: abrir os PDFs.
- ARIS (SC), AGIR (SC), ARES-PCJ, ARPB, AGEMS: busca não retornou página oficial de adesão/checklist que eu tenha aberto; nenhuma prática registrada.
- TCE-RS/TCU sobre inexigibilidade (art. 74 Lei 14.133) para delegação a agência: nenhum acórdão localizado; TCE-SC (cautelar sobre manutenção de contrato com agência) retornou HTTP 403 e não foi lido.
- Transferegov/Manual AGU de convênios e checklists AGU: apenas o parecer referencial CONJUR-MS (que cita as minutas CNCIC/CGU/AGU) foi lido; páginas do Transferegov não foram abertas.
- ANA: página oficial com a lista de entidades reguladoras que adotaram NRs e SNIRH não abertas (URLs tentadas deram 404); NR 4 não verificada.
- Nenhuma fonte lida reporta ganho numérico (tempo/custo) das práticas; ganho_reportado=null em todas. Prazos citados (30 dias de publicação; 5 dias úteis SEI) são regras, não ganhos.
- Observação de método: trechos de leis (Lei 14.026, Lei 14.133, Lei MG 25.669) foram extraídos via WebFetch (modelo resumidor) com acentos restaurados; recomenda-se conferência manual do trecho na fonte. Trechos de PDFs (BM-01,02,03,05,07) foram conferidos em texto extraído por pdftotext.
