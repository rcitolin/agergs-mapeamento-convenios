# Fase 1 — conteúdo das peças: fichas de trabalho e esforço

04/11/2026 · fichas em `saida/fichas_trabalho.jsonl` (completas) e `saida/fichas_trabalho.csv` (resumo) · especificação
em `ESPECIFICACAO_FICHAS.md` (adaptação do prompt ficha-v2 de `metodologia-repo/scripts/fichas_trabalho.py`) ·
narrativas por processo em `docs/ASIS.md`.

## 1. O que foi feito

- **Piloto = carteira inteira.** Com 18 processos de um só tipo, não houve seleção de piloto. Todos os casos e os 2
  processos de gestão (processo orientativo e minuta padrão) receberam ficha, peça a peça.
- **Leitura em paralelo.** Um agente por processo (Passo Fundo em duas partes), seguindo a mesma especificação; os 6
  processos novos foram lidos numa segunda rodada, com a mesma especificação. Cada ficha traz atividade, tarefa,
  entregável, conclusão de mérito, natureza do trabalho, insumos, normas citadas, complexidade (1 a 5), composição do
  texto (autoral, transcrição, padrão), sinais de perda e prazos.
- **Cobertura.** 381 fichas para 381 documentos, sem documento sem ficha e sem ficha sem documento
  (`saida/auditoria_ancoragem.json`). Nos 18 casos: 358 fichas, sendo 256 de peças da AGERGS e 102 externas
  (76 do município e 26 do prestador).
- **Ancoragem por código.** Toda evidência de ficha é um trecho literal da peça. A função `ancorar` (a mesma regra de
  `fichas_trabalho.py`) conferiu 732 evidências: **100% ancoradas**.
- **Peça externa** (ofício do prefeito, lei municipal, PMSB, contrato da CORSAN) recebe ficha curta, sem horas.

## 2. Esforço: uma faixa, ainda sem calibração

Há três estimativas por peça. Todas são **hipótese até a calibração com os servidores**:

| Estimativa | Regra | Total nos 18 casos |
|---|---|---|
| Piso | horas-base da natureza + conferência da peça (0,05 h por lauda de 1.250 caracteres) | 126,5 h |
| Teto | horas-base + laudas autorais × coeficiente da complexidade + 0,25 h por insumo ancorado (regra `horas_modelo` de `comum.py`) | 262,3 h |
| Agente leitor | horas declaradas na ficha, em 255 peças da AGERGS | 276,0 h |

A estimativa do agente fica perto do teto. Por caso, a mediana é de 4,8 h no piso e 8,6 h no teto
(`coorte.caso.horas_piso` e `coorte.caso.horas_teto`). Mesmo no teto, celebrar um instrumento custa poucas dezenas de
horas, contra meses de calendário.

## 3. Onde está o trabalho

Peças da AGERGS nos 18 casos, por natureza (horas do modelo):

| Natureza | Horas piso | Horas teto | % do teto |
|---|---|---|---|
| Análise jurídica | 44,5 | 98,1 | 37,4% |
| Comunicação (ofícios, e-mails ao município e ao prestador) | 24,0 | 40,8 | 15,5% |
| Encaminhamento (despachos sem conteúdo próprio) | 12,9 | 40,1 | 15,3% |
| Instrução processual (memorandos, minutas, juntadas) | 18,9 | 34,8 | 13,3% |
| Relatoria e decisão (voto, ata, resolução, autorização) | 15,9 | 29,2 | 11,1% |
| Publicação e registro | 6,7 | 12,5 | 4,8% |
| Auditoria e conferência | 1,5 | 2,4 | 0,9% |
| Análise técnica de engenharia | 1,2 | 2,2 | 0,8% |
| Análise econômico-financeira | 1,1 | 2,2 | 0,8% |

- **O jurídico concentra o trabalho analítico.** A análise técnica quase não aparece (2,2 h no teto em 18 casos): a
  viabilidade técnica da delegação raramente é examinada nos autos.
- **Um sexto das horas é encaminhamento.** São despachos que só passam o processo adiante, e somam 15,3% do teto.
- **Complexidade baixa.** Das 256 peças da AGERGS, 101 têm complexidade 1 (expediente), 102 têm complexidade 2,
  38 têm complexidade 3 e 15 têm complexidade 4. Nenhuma tem complexidade 5.
- **Insumos ancorados**: documento do próprio processo (200), norma ou contrato (45), documento do município (24),
  sistema interno (14), base externa (9) e precedente (6). 65 peças citam norma com trecho ancorado.

## 4. Sinais de perda nas peças

Sinais ancorados em trecho literal, nos 18 casos (ocorrências / processos):

| Sinal | Ocorrências | Processos |
|---|---|---|
| Aguardando outra unidade | 10 | 5 |
| Reiteração | 8 | 7 |
| Sobrestamento (retirada de pauta, suspensão) | 6 | 2 |
| Pedido de complementação | 6 | 4 |
| Refazimento (minuta refeita, errata, nova versão) | 5 | 2 |
| Diligência externa | 3 | 3 |
| Prazo concedido | 3 | 1 |

Prazos registrados nas peças: 32 (15 ao município, 11 ao prestador, 4 a órgão externo, 2 a unidade interna).

## 5. Leitura para o AS-IS

1. O processo é jurídico e de expediente. O trabalho analítico está na DAJ e na PSE, e o resto é comunicação,
   encaminhamento e registro, que é a matéria-prima das fases 1 e 2 do TO-BE (padronização e modelos).
2. Os sinais de perda se concentram nos casos longos (Passo Fundo, Minas do Leão, Mampituba) e nos pedidos sem
   resposta: retirada de pauta, minuta refeita, reiteração ao município e ao prestador, e o município reiterando o
   próprio pedido (Unistalda).
3. Erros materiais aparecem em várias peças e se repetem entre instrumentos: "Lei n. 11.445/2027", foro divergente ou
   de outro município (Salvador do Sul: minuta com foro do município, convênio com a Comarca de Montenegro; Unistalda:
   foro de Santiago), número de lei municipal divergente (Salvador do Sul; Campinas das Missões), "Município de Xxx",
   CNPJ divergente, súmula publicada antes da assinatura. São defeitos que a minuta padrão e a checagem automática
   eliminam.
