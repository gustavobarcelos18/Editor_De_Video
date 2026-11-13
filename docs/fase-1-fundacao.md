# Fase 1 — Fundação, ingestão e esqueleto de ponta a ponta

Plano de execução. Fonte de verdade do produto: [00-plano-mestre.md](00-plano-mestre.md) (seção 7, Fase 1).
Decisão de dividir a fase: [histórico §25](01-historico-de-decisoes.md).

Status: aprovado (D1–D4 confirmadas, histórico §26) · Branch: `fase/1-fundacao` (sub-etapas em commits/PRs menores, ver "Fluxo git").

## Divisão

A Fase 1 original era grande demais. Ela fica em três sub-etapas, nesta ordem:

| Sub-etapa | Onde roda | Entrega |
|---|---|---|
| **1A – Esqueleto e ingestão** | `dev` (PC do trabalho, sem GPU) | Monorepo, CI, config, banco, contratos, orquestrador com cache e retomada, ingestão completa sobre fixtures sintéticas |
| **1B – Marcadores e prévia** | `dev` (testes com mocks); validação final em `prod` | Gravador de marcadores (opção A), diário `.markers.jsonl`, reconciliação, CLI `ingest/status/preview`, prévia MP4, FCPXML mínimo |
| **1C – Itens do PC de casa** | `prod` (kit montado em `dev`) | Kit de teste do Resolve, spike da FIFINE, guia do OBS, benchmark de desempenho na RTX 3060, gabarito (formato) |

1A não depende de nada em aberto. 1B depende das decisões D1–D3 abaixo. 1C depende de o criador estar no PC de casa.
Cada sub-etapa só começa com os critérios da anterior cumpridos, exceto 1C, que pode ser executada em paralelo assim
que o kit existir.

## Decisões D1–D4 (confirmadas pelo criador em 2026-11-12)

Todas aprovadas como propostas; registradas no plano mestre (seção 9) e no histórico (§26). A coluna "Proposta" é a decisão.

| # | Dúvida | Proposta | Motivo |
|---|---|---|---|
| D1 | Linguagem do gravador de marcadores e quem dispara o processamento | **Python**, como processo separado do engine, que escuta as hotkeys e fala com o obs-websocket. O disparo do processamento ao fim da gravação é do **engine** (serviço sempre aberto que observa o evento `recording_stopped` no diário) | Uma linguagem só; o gravador fica pequeno e o engine continua dono da política de GPU. ⚠️ Bibliotecas de hotkey global e de obs-websocket para Python: confirmar versões |
| D2 | Direção dos contratos | **Pydantic → JSON Schema (e OpenAPI do FastAPI) → tipos TypeScript gerados** | Pydantic já é a fonte no engine (exemplo da seção 6.1) e o FastAPI gera o OpenAPI sem esforço. Muda o texto da seção 5.2 ("JSON Schema → Pydantic") |
| D3 | Ferramenta de anotação do gabarito | **CSV/planilha** (`inicio, fim, classe, nota`) + um script que valida o arquivo e mostra a prévia dos trechos | Zero UI; o Studio só chega na Fase 7. Basta para a Fase 2 |
| D4 | Fase 1.5 (rough cut só de marcadores) | **Não criar**: a prévia MP4 da 1B já cumpre esse papel | Evita mais uma fase |

## 1A — Esqueleto e ingestão

### Tarefas

1. **Monorepo e tooling**
   - Estrutura da seção 5.5 do plano (só as pastas que terão conteúdo; as demais entram nas fases seguintes).
   - `services/engine`: Python 3.12, uv, pacote `cronista` em `src/`, ruff, mypy (estrito no `domain/` e `pipeline/`), pytest com marcas `gpu` e `media`.
   - `apps/studio`: só o esqueleto Next.js + pnpm + eslint + tsc (sem telas). Serve para o CI cobrir os dois lados.
   - `.gitignore` conferido contra a seção 9 (mídia ignorada; exceção para `services/engine/tests/fixtures/`).
2. **CI (GitHub Actions)**: ruff, mypy, pytest (CPU, sem as marcas `gpu`/`media`), eslint, tsc; matriz Ubuntu + Windows; FFmpeg instalado no job.
3. **Configuração**: `config/dev.yaml` e `config/prod.yaml` versionados, sem caminhos pessoais; `config/*.local.yaml` por cima, fora do git. Carregador com validação Pydantic. Caminhos de mídia nunca fixos no código.
4. **Banco**: SQLite com SQLAlchemy 2 + Alembic. Tabelas iniciais: `project`, `session`, `media_file`, `job`, `artifact` (com hash de cache), `marker`. Sem `day_number` em lugar nenhum (seção 4).
5. **Contratos**: modelos Pydantic em `domain/` e geração do schema + tipos TS por script (`pnpm gen:contracts` / `uv run`), conferido no CI (falha se o gerado divergir do versionado). Depende de D2.
6. **Orquestrador de pipeline** (`pipeline/`)
   - Etapa = função pura: recebe artefatos, produz artefatos versionados.
   - Chave de cache = hash(entrada + parâmetros + versão da etapa/modelo).
   - Jobs persistidos no banco; estados `pending/running/done/failed`; retomada após interrupção (um job `running` órfão volta para `pending` ao iniciar).
   - Logs estruturados (JSON) com `session_id`, `stage`, `job_id`.
   - Política de GPU como porta (`GpuGate`): em `dev` é um mock sempre livre; a implementação real (OBS gravando / jogo em tela cheia) fica para a 1B/1C.
7. **Fixtures sintéticas** (`data/fixtures/`, geradas por script FFmpeg, nunca versionadas): vídeo 1080p60 H.264 8-bit NV12 Rec. 709 com **três faixas de áudio** (mix, jogo, microfone: tons e ruídos distintos), em quatro variantes: normal; com pausa; com divisão de arquivo; interrompida (arquivo sem finalização). Mais uma variante 10-bit e uma 59,94 fps para os testes de validação.
8. **Ingestão** (`ingest/`)
   - Leitura das faixas e validação com `ffprobe`: 8-bit, 60 fps exatos, H.264, três faixas. 10-bit: avisa e converte para 8-bit (seção 2). Outro fps: erro claro (não converte em silêncio).
   - Remux de arquivo interrompido com `ffmpeg -map 0 -c copy`, conferindo que as três faixas continuam.
   - Proxy 360p no SSD: H.264 + AAC com **uma faixa só (o mix, faixa 1)** e `faststart`.
   - Extração de WAV por faixa (jogo e microfone) no cache do SSD; regenerável do master.
   - Tudo como etapas do orquestrador (idempotentes e retomáveis).
9. **Projeto incremental por sessão**: `cronista ingest <pasta>` cria o projeto se não existir e acrescenta a sessão; reingerir a mesma pasta não duplica nada (cache).
10. **CLI base**: `cronista ingest <pasta>` e `cronista status` (sessões, etapas, jobs). `preview` fica para a 1B.

### Critérios de aceite (1A)

- [ ] `uv run pytest` e `pnpm lint && pnpm typecheck` passam em `dev` sem GPU; CI verde em Ubuntu **e** Windows.
- [ ] `cronista ingest` sobre cada variante de fixture termina sem intervenção; sobre a interrompida, o remux preserva as 3 faixas (`ffprobe`).
- [ ] Matar o processo no meio da ingestão e rodar de novo termina sem refazer as etapas concluídas (teste automatizado conferindo as contagens de execução por etapa).
- [ ] Reingerir a mesma pasta não cria sessão nem artefatos novos.
- [ ] Mudar um parâmetro de uma etapa invalida só ela e as seguintes.
- [ ] Arquivo 10-bit gera aviso e saída 8-bit; arquivo 59,94 fps é rejeitado com mensagem clara.
- [ ] Nenhum caminho pessoal versionado (checagem no CI: `grep` por `C:\Users`/`/home/`).

### Testes (1A)

Unitários do cache por hash e da máquina de estados dos jobs; integração da ingestão com as fixtures; teste de retomada (interrupção forçada); teste do carregador de config (camada local sobrepõe a versionada); teste de que o schema/tipos gerados estão em dia.

## 1B — Marcadores e prévia

### Tarefas

1. **Diário `.markers.jsonl`**: eventos `recording_started`, `paused`, `unpaused`, `file_changed` (com caminho), `recording_stopped` e `marker` (tipo, id), cada um com relógio monotônico + UTC. Esquema Pydantic, escrita com flush a cada linha (sobrevive a queda).
2. **Reconstrução do tempo de mídia** a partir do diário (tempo do toque − início − pausas acumuladas, dentro do arquivo vigente) e **reconciliação** com os marcadores do arquivo, pelo `id`, com as regras da seção 4 (bate em ~1 s → arquivo; só diário → reconstruído; diverge → arquivo + aviso; fora de gravação → ignorado com aviso). Pendência da seção 9, item 9: marcador que existe só no arquivo → proposta: tratar como `Momento` com aviso (confirmar).
3. **Gravador de marcadores (opção A)**: programa Python ao lado do OBS (depende de D1). Hotkeys obrigatórias `Momento` e `Novo dia`, opcionais `Morte/Falha`, `Engraçado`, `Conquista`, `Construção ▶/■` (alterna; o programa guarda o estado de construção aberta), `Foto de progresso`, `Cinemática`. Cria o marcador do OBS com nome `tipo|id` (⚠️ requisição `CreateRecordChapter`: confirmar nome e versão mínima do OBS) e escreve o diário. Feedback sonoro ou visual discreto a cada toque (resolve a dúvida de saber se o toque foi registrado). Testado contra um **servidor obs-websocket falso**; a validação com o OBS real é da 1C.
4. **Ingestão de marcadores**: etapa nova no pipeline que lê o diário + chapters do arquivo (`ffprobe -show_chapters`) e grava `marker` no banco com o tempo de mídia final e os avisos. `Construção ▶` sem `■` é fechada no fim da sessão, com aviso. Sessão sem `Novo dia` continua o dia anterior; a primeira sessão do projeto sem `Novo dia`: proposta, abrir um dia implícito no início (confirmar, seção 9 item 8).
5. **Prévia MP4**: `cronista preview <sessão>`: para cada marcador, corta uma janela ao redor (proposta: 20 s antes e 10 s depois; sem lookback inteligente, que é da Fase 4), concatena com FFmpeg em 1080p60 H.264 (CPU em `dev`, NVENC em `prod`), mudando o áudio para o mix. Sem recursos do Studio.
6. **FCPXML mínimo**: timeline 60 fps exatos, um clipe por marcador na V1, áudio nas trilhas A1/A2, referências aos masters. Sem keyframes, sem cor de marcador (seção 6.3). Gerado primeiro pelo caminho OTIO → FCPXML, para já medir o limite do adaptador (spike, seção 6.5). Validação contra o Resolve só na 1C.

### Critérios de aceite (1B)

- [ ] Fixtures de diário (simples, com pausas, com divisão de arquivo, com queda) produzem o tempo de mídia esperado (erro < 100 ms nos sintéticos).
- [ ] Reconciliação cobre os quatro casos da seção 4, cada um com teste e aviso no relatório.
- [ ] O gravador, contra o servidor falso, cria o marcador com nome `tipo|id` e escreve o diário; reabrir após queda não corrompe o diário.
- [ ] `cronista preview` gera um MP4 reproduzível, com N trechos para N marcadores, duração dentro de ±1 s do esperado.
- [ ] O FCPXML mínimo é gerado e passa em validação estrutural (esquema/DTD, se disponível); a importação real é item da 1C.
- [ ] CI verde.

## 1C — Itens do PC de casa

### Tarefas

1. **Kit de teste do Resolve gratuito** (montado em `dev`, rodado em `prod`; seção 6.5): FCPXML com corte, velocidade, zoom com keyframe, transição, volume, marcador e relink; script interno mínimo (criar projeto, importar, marcadores, LUT); clipes H.264 e HEVC 8-bit gerados por FFmpeg (scripts, não versionados); **roteiro de checagem** em Markdown com campos para anotar o resultado de cada item do checklist da seção 6.5.
2. **Spike da FIFINE SC3** (seção 4): script que escuta HID e MIDI e imprime os eventos; ordem: HID/MIDI → marcador por áudio → F13–F24/mouse/macropad.
3. **Guia de configuração do OBS** (`integrations/obs/`): Hybrid MP4, 60 fps exatos, NVENC H.264 NV12 Rec. 709, microfone em duas fontes, faixas 1/2/3, servidor WebSocket, jogo/OBS como administrador. Inclui o teste de que o OBS aceita o mesmo dispositivo em duas fontes e a versão mínima para marcadores.
4. **Benchmark de desempenho** (RTX 3060): velocidade e VRAM de faster-whisper, Silero, classificador de eventos, embeddings e Ollama; confere a convivência de cuBLAS/cuDNN do CTranslate2 com o PyTorch (⚠️ seção 5.2). Marcado `@pytest.mark.gpu`.
5. **Gabarito**: formato (CSV, D3) + script de validação documentados. A anotação em si (2–3 h) é do criador, quando puder.
6. **Validação em `prod`** do que a 1A/1B só testaram com mocks: gravação real com marcadores via gravador, ingestão, prévia e importação do FCPXML.

### Critérios de aceite (1C)

- [ ] Roteiro de checagem do Resolve preenchido (itens que o plano marca como ⚠️ ganham resposta e são movidos para a seção 6.5).
- [ ] Resultado da FIFINE registrado (qual dos três caminhos vale).
- [ ] Guia do OBS seguido do zero produz uma gravação que passa na validação da ingestão.
- [ ] Tabela de desempenho (velocidade e VRAM por modelo) salva em `docs/`.

## Aceite da Fase 1 (do plano mestre)

Ingerir sem intervenção uma gravação de qualquer duração (gameplay de teste ou fixtures), retomar após interrupção,
proxies e marcadores corretos, prévia MP4 gerada a partir dos marcadores, CI verde. Equivale a: **1A + 1B completas**.
A 1C não bloqueia o merge da Fase 1, mas bloqueia o início da Fase 6 (spike do Resolve) e da Fase 2 (benchmark e gabarito).

## Fluxo git

Branch `fase/1-fundacao`; um commit (ou PR de sub-etapa) por bloco de tarefas, Conventional Commits em pt-BR; `/code-review`
antes do merge na `main`. Se a 1C atrasar por depender do PC de casa, a 1A+1B podem ir para a `main` e a 1C vira uma branch
curta própria (`fase/1c-pc-de-casa`).

## Riscos específicos da fase

| Risco | Mitigação |
|---|---|
| Fixtures do FFmpeg não reproduzem o Hybrid MP4 do OBS (marcadores, fragmentação) | A 1C valida com gravação real; testes da 1B isolam o leitor de chapters atrás de uma interface |
| Hotkeys globais não funcionam com o jogo elevado | Já previsto: administrador ou dispositivo físico; testado na 1C |
| Biblioteca de hotkey/obs-websocket sem manutenção ou incompatível com Python 3.12 | ⚠️ Confirmar antes de iniciar a 1B; porta/adaptador para trocar |
| CI no Windows lento ou com FFmpeg diferente | Fixar a versão do FFmpeg no CI; testes de mídia com fixtures curtas (poucos segundos) |
