# Mapeamento e melhoria do processo de celebração de convênios e contratos de delegação da regulação — AGERGS

Aplicação da metodologia do repositório do curso
([`RaulAraujoSilva/mapeamento-processos-sei`](https://github.com/RaulAraujoSilva/mapeamento-processos-sei)) ao processo pelo qual um **município delega à AGERGS a
regulação** de um serviço público, por convênio (2018–2020) ou por contrato de prestação de serviços de regulação
(2025–2026), além de um termo aditivo. A base são os 20 processos SEI da pasta-mãe: 18 celebrações (Alecrim,
Arambaré, Campinas das Missões, Capão Bonito do Sul, Chiapetta — aditivo, Jaguari, Lagoa Bonita do Sul, Liberato
Salzano, Mampituba, Mata, Minas do Leão, Nova Bréscia, Panambi, Passa Sete, Passo Fundo, Salvador do Sul, Unistalda,
Vila Nova do Sul), o processo orientativo (SEI 002594-39.00/26-9) e o da minuta padrão (SEI 002840-39.00/26-3).

As adaptações do método a esta base (PDFs sem andamentos, um único tipo de processo) estão em
[docs/METODO_ADAPTADO.md](docs/METODO_ADAPTADO.md).

## Resultados principais

Todos os números saem dos arquivos de `saida/`, calculados por código. Horas e custo são **hipótese até a calibração
com os servidores**. Com 18 casos, as medianas ainda são instáveis.

| Pergunta | Resposta | Fonte |
|---|---|---|
| Quanto dura uma celebração? | Lead time mediano de **74,5 dias úteis** (q1 de 23, q3 de 135,8, máximo de 376) | `saida/fase3/linha_base_CONV.json` |
| Quanto disso é trabalho? | A execução cobre **14,3%** do lead somado; PCE no teto de **1,7%**; mediana de 8,6 h-teto por caso | `saida/bpmn/fatos_CONV.json` |
| Existe um processo-padrão? | Não: **18 caminhos em 18 casos**; mediana de 7,5 passagens e 2 retornos por caso | idem |
| Onde está a espera? | Comunicação pós-assinatura (21,3% da espera total), pedido do município sem resposta até a reiteração (16,3%), publicação (16,1%), minuta (13,8%) e análise jurídica (10,5%); só 14,6% é tempo de terceiros | idem |
| Quanto se cumpre da lei? | Parecer jurídico antes da assinatura em 50% dos casos; autorização formal em 16,7%; publicação em 66,7%; publicação em até 10 du em 20%; decisão em até 30 dias da instrução em 33,3%; inexigibilidade nos autos em 0% dos contratos | `saida/fase3/conformidade_CONV.json` |
| Quanto se ganha? | Lead mediano simulado (cenário esperado): 31,0 du na fase 1 (−58,4%), 26,2 du na fase 2 (−64,8%), 24,6 du na fase 3 (−67,0%); faixa de −47,5% a −78,3% na fase 3 | `saida/fase3/resultado_tobe_CONV.json` |
| É bom piloto de automação com IA? | Não como piloto de automação completa: nota 60,0 (P01 de referência: 80,0), e os portões de volume, procedimento e padrão falham. O ganho vem das fases 1 e 2 (fluxo e regras) | `saida/fase4/matriz_automacao_CONV.json` |

O achado do caso de referência se repete: **o tempo é espera, não trabalho**. A fase 1 do TO-BE (kit de adesão,
minuta padrão com parecer referencial, dono do processo e prazos, publicação e comunicado em prazo fixo) responde
pela maior parte do ganho, sem tecnologia nova.

## Paradas para validação (o aluno decide)

1. **Auditoria às cegas abaixo do critério**: em duas rodadas (97 peças), 81,6% de concordância nas peças
   substantivas, contra 85% exigidos. As divergências estão em `saida/auditoria/auditoria_classificador_CONV.json`. Três já foram corrigidas e justificadas
   em `dados/correcoes_rotulos.json`. Por isso o processo está como *indicativo*, não *procedimento*.
2. **Normas estaduais de fonte secundária** (Leis RS 16.266/2024 e 15.612/2021): conferir no DOE-RS.
3. **Volume anual e custo-hora**: hipóteses (5 celebrações/ano; R$ 55 a 121/h). Trocar em `scripts/fase3_agergs.py`.
4. **Dono do processo** (DAI, como propõe o processo orientativo) e **escolha do piloto de automação**: decisão da gestão.

## Mapa

| Pasta/arquivo | Conteúdo | Equivalente no repositório |
|---|---|---|
| `textos/` | Texto integral dos 20 PDFs (`pdftotext -layout`) | `dados/relator` |
| `dados/` | Base por documento, assinaturas, texto por peça, fichas e narrativas dos agentes, referência (orientativo, minuta padrão, benchmark). **Contém nomes de servidores: não publicar** | `dados/` (fora do git) |
| `normas/` | Base normativa em texto integral + `indice.json` | `normas/` |
| `ESPECIFICACAO_FICHAS.md` | Especificação das fichas por peça e das narrativas | prompt de `scripts/fichas_trabalho.py` |
| `scripts/base_documentos.py` | Segmenta os PDFs em documentos e lê as assinaturas | `coleta/` |
| `scripts/pipeline_agergs.py` | Fichas + ancoragem, esforço, linha do tempo, fatos, procedimento, fase 0 | `trilhas.py`, `fichas_trabalho.py`, `fatos.py`, `procedimento.py` |
| `scripts/gerar_bpmn_agergs.py` | BPMN 2.0 e visualizador, com o gerador do repositório | `gerar_bpmn.py` |
| `scripts/fase3_agergs.py` | Auditoria às cegas, normas, conformidade, validador da avaliação, linha de base, TO-BE, controles, priorização | `verificar_normas.py`, `conformidade.py`, `validar_avaliacao.py`, `linha_base.py`, `validar_tobe.py`, `simular_tobe.py`, `validar_controles.py`, `priorizacao_automacao.py` |
| `saida/` | Todas as saídas: `fichas_trabalho.*`, `processos_indicadores.csv`, `estadias.csv`, `Mapeamento_AGERGS_Celebracao.xlsx`, `bpmn/`, `fase2/`, `fase3/`, `fase4/`, `auditoria/` | `saida/` |
| `docs/` | Relatórios; `docs/bpmn/index.html` (diagramas); `docs/site/index.html` (site navegável) | `docs/` |

## Publicação e dados pessoais

Este repositório segue a regra do repositório de referência: **dados pessoais ficam fora do git**.

- Ficaram de fora o texto integral dos PDFs (`textos/`), o texto por peça (`dados/docs/`) e as amostras da auditoria
  às cegas com texto integral. Sem eles, as etapas que releem o texto (ancoragem das evidências e auditoria) não
  rodam; todas as demais rodam a partir de `dados/fichas`, `dados/narrativas` e `dados/documentos.csv`.
- Nomes de pessoas foram trocados pela função, com a mesma letra para a mesma pessoa em todos os arquivos:
  conselheiros viram "Conselheiro A", "Conselheiro B" etc.; demais servidores, `[servidor da agência]`; pessoas
  externas (prefeitos, representantes do prestador), `[pessoa citada]`. Números de OAB, e-mails, telefones e CPF
  foram retirados.
- Números de processo SEI, unidades da agência e municípios continuam, porque são informação pública.
- Como as evidências das fichas foram anonimizadas, um trecho que continha nome não confere mais, letra por letra,
  com o texto original.

## Como rodar de novo

```bash
python3 scripts/pipeline_agergs.py
```

```bash
python3 scripts/fase3_agergs.py
```

```bash
python3 scripts/gerar_bpmn_agergs.py
```

O gerador do BPMN usa o repositório de referência: clone `mapeamento-processos-sei` como `metodologia-repo/`
na pasta ao lado desta. `scripts/base_documentos.py` refaz a base a partir dos PDFs, que não estão aqui.

Dependências: Python 3.12 ou mais recente, `pandas`, `numpy`, `openpyxl` e `matplotlib`; `pdftotext` (poppler) para
extrair o texto. As etapas de julgamento (fichas, narrativas, modelo, avaliação, melhorias, controles) têm saída em
arquivo e não precisam ser refeitas para recalcular os números. Duas rodadas com os mesmos dados geram arquivos
idênticos.
