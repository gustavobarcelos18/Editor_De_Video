# Cronista — Plano Mestre

> Nome provisório. Aplicação pessoal que transforma dezenas de horas de gameplay gravada no OBS em uma
> **timeline pré-montada no DaVinci Resolve** + **roteiro de narração** para vídeos de "100 dias".

Data: 2026-11-12 · Status: rascunho para aprovação

---

## 0. Como retomar (em outro PC ou nova sessão)

Clone o repositório, abra o Claude Code na pasta e cole:

```
Estou retomando o projeto Cronista (app pessoal de edição de gameplays de 100 dias).
Leia docs/00-plano-mestre.md inteiro, que é a fonte de verdade de tudo que já decidimos.
Depois vamos responder as decisões em aberto (seção 9) e detalhar a Fase 1 em
docs/fase-1-fundacao.md, com tarefas, critérios de aceite e testes (use a skill criar-plano).
```

Checklist do PC de casa:
- [ ] DaVinci Resolve (gratuito), Python 3.12 + uv, Node.js LTS + pnpm, FFmpeg, Ollama, Git
- [ ] Drivers NVIDIA/CUDA da RTX 3060 atualizados
- [ ] OBS com faixas de áudio separadas (seção 2)
- [ ] Responder as decisões em aberto (seção 9)

## 0.1 Requisitos do criador (respostas da conversa inicial)

| Tema | Decisão |
|---|---|
| Jogos | Minecraft, Valheim, Terraria, EA FC (modo carreira), GTA V com mods e outros |
| Gravação | OBS, 1920×1080 a 60 fps; narra ao vivo parte do tempo; faixas de áudio separadas |
| Hardware | RTX 3060 12 GB, 32 GB RAM, HD 2,5 TB, SSD 450 GB |
| Custo | Zero: modelos locais + Claude Code no plano Pro |
| Saída | Timeline pré-montada no DaVinci Resolve gratuito + Shorts/Reels |
| Roteiro | Só roteiro (sem voz de IA), humanizado, no estilo de fala do criador |
| Estilo | Storytelling: mortes e falhas (sofrimento + humor), conquistas, chefes, construções |
| Referências | Baronismo, Xedou, Trousy, Promptz (estudar o ritmo, não o conteúdo) |
| Marcadores | Aceita apertar hotkeys durante o jogo |
| Usuários | Só o criador, mas estruturado para escalar |
| Stack conhecida | C#, Python, Next.js, React, NestJS, JavaScript, TypeScript |
| Entrega | Versão completa em fases grandes; cada fase vira um plano de execução próprio |

---

## 1. Objetivo e escopo

**Entrada:** gravações do OBS (1080p60, áudio em faixas separadas) + marcadores feitos por hotkey durante o jogo
+ (opcional) logs/eventos emitidos por mods do jogo.

**Saída:**
1. Timeline para o DaVinci Resolve (cortes, trechos de farm em timelapse, marcadores coloridos por tipo de momento).
2. Roteiro de narração sugerido, no estilo de fala do próprio criador, sem "cara de IA".
3. Candidatos a Shorts/Reels (trechos verticais 9:16 + gancho sugerido).

**Fora de escopo (por enquanto):** renderizar o vídeo final, gerar voz sintética, multiusuário/SaaS.

**Restrições:**
- Custo zero: tudo local (RTX 3060 12 GB, 32 GB RAM). Claude entra apenas via **Claude Code com o plano Pro**
  (headless `claude -p` ou skill rodada manualmente), sempre com entradas compactas por causa dos limites de uso.
- Jogos variados: Minecraft, Valheim, Terraria, EA FC (modo carreira), GTA V com mods e outros → o núcleo é
  **agnóstico de jogo**, e as especificidades ficam em **adaptadores**.

---

## 2. Quanto gravar

| Referência | Conta |
|---|---|
| Minecraft: 1 dia do jogo = 20 min reais | 100 dias ≈ 33 h (pulando noites dormindo: ~17–25 h) |
| Taxa de compressão típica do formato | 30:1 a 50:1 |
| Vídeo final de 30–50 min | **≈ 20–35 h de gravação bruta** |

Recomendação: mirar **25 h** e usar a Fase 4 para medir a taxa real das suas sessões. Abaixo de ~15 h o vídeo
tende a ficar sem "respiro" de farm/timelapse e com poucas falhas para gerar humor.

**Armazenamento:** 1080p60 em NVENC CQP ~22 fica em ~10–20 GB/h → 25 h ≈ 250–500 GB.
→ **Masters no HD de 2,5 TB**. **Proxies 360p (~0,5 GB/h), cache e banco no SSD** (é ali que a análise lê o tempo todo).

**Configuração do OBS sugerida:**
- Contêiner: MKV ou Hybrid MP4 (sobrevive a quedas e suporta marcadores de capítulo).
- Faixa 1 = mix · Faixa 2 = **jogo** · Faixa 3 = **microfone** · Faixa 4 = Discord/amigos (se houver).
- Microfone com supressão de ruído do OBS (RNNoise) **só na faixa de mix**. A faixa 3 fica crua, e o pipeline faz o próprio tratamento.

---

## 3. O problema do ruído (teclado, respiração, pisadas)

Volume absoluto não serve como sinal. A estratégia tem quatro camadas:

1. **Separação física por faixa.** Teclado e respiração só existem na faixa do microfone. Pisadas, música e
   combate só existem na faixa do jogo. Nunca se analisa o mix.
2. **Microfone → só voz conta.**
   - VAD neural (Silero VAD) separa fala de não-fala. Clique de teclado e respiração são não-fala e são descartados.
   - Supressão de ruído (DeepFilterNet) antes da transcrição.
   - Características usadas: fala, risada, grito, aumento súbito de tom/energia **em relação à sua média da sessão**.
3. **Jogo → classificar o som, não medir o volume.**
   - Classificador de eventos sonoros pré-treinado (PANNs/BEATs/CLAP), com rótulos como explosão, música, impacto, multidão.
   - **Linha de base adaptativa:** mediana móvel por sessão e por "contexto" (bioma, menu, cidade). Pisada em pedra
     é repetitiva e periódica, então gera **baixa novidade**. O que pontua é a *mudança* em relação ao baseline
     (novidade espectral), não a altura do som.
   - Detecção de periodicidade: sons rítmicos e constantes (passos, mineração, corte de árvore) são sinal de **rotina/farm**.
4. **Calibração por jogo.** Cada adaptador define pesos e rótulos ignorados (ex.: no Minecraft, "som de bloco
   quebrando" vale farm). O feedback da revisão (aceito/rejeitado) recalibra esses pesos (Fase 7).

---

## 4. Marcadores por hotkey

**Um toque já basta.** Ele quer dizer "aqui teve algo". Normalmente você aperta *depois* do acontecimento, então
o sistema olha para trás (janela padrão de 60–90 s, ajustável por jogo) e encontra os limites reais do momento
usando mudança de cena, picos de áudio e fala.

Hotkeys sugeridas (todas opcionais, exceto a primeira):

| Hotkey | Significado | Uso |
|---|---|---|
| `Momento` | Algo legal aconteceu | Toque único, a IA decide os limites |
| `Morte/Falha` | Falha ou morte | Alimenta o humor e o "sofrimento" do desafio |
| `Engraçado` | Momento cômico | Prioridade para Shorts |
| `Conquista` | Chefe, objetivo, item raro | Pico da narrativa |
| `Início Dia N` | Marca o começo de um novo dia | Estrutura os capítulos (sem depender de OCR) |
| `Construção ▶/■` | Início e fim de uma construção | **Único caso com início e fim**: vira timelapse antes/depois |
| `Foto de progresso` | Tomada do ponto de câmera fixo | Alinhada com as anteriores para o timelapse de construção (ver 6.2) |
| `Cinemática` | Tomada bonita/intencional | Vai direto para a biblioteca de B-roll |

**Implementação:** script Python do OBS que registra as hotkeys e grava um arquivo `.markers.jsonl` ao lado da
gravação (timestamp relativo ao início da gravação + tipo + nº do dia). Como redundância, a hotkey também cria
um marcador de capítulo do OBS (Hybrid MP4).

---

## 5. Arquitetura

### 5.1 Visão geral

```
 OBS ──► gravação (.mkv) + .markers.jsonl          Mods do jogo ──► eventos (.jsonl) [opcional]
              │                                                   │
              ▼                                                   ▼
 ┌──────────────────────────── ENGINE (Python) ─────────────────────────────┐
 │ Ingestão → Proxies → Análise Áudio → Análise Vídeo → Adaptador do Jogo   │
 │        → Fusão de Sinais → Segmentos+Nota → Narrativa → Montagem → Export │
 │   (cada etapa: idempotente, com cache por hash, retomável)               │
 └──────────────┬──────────────────────────────────────────┬────────────────┘
                │ API (FastAPI) + eventos de progresso      │ story-pack.json
                ▼                                            ▼
     STUDIO (Next.js) — revisão,                  Claude Code (plano Pro)
     aceitar/rejeitar, editar roteiro             skills: /roteirizar, /humanizar
                │                                            │
                └──────────────► Export: FCPXML/OTIO + SRT do roteiro ──► DaVinci Resolve
```

### 5.2 Decisões de tecnologia

| Camada | Escolha | Por quê |
|---|---|---|
| Processamento | **Python 3.12 + uv** | Ecossistema de áudio/vídeo/ML; roda nativo no Windows com CUDA |
| Vídeo | **FFmpeg** (NVDEC/NVENC) + PySceneDetect + OpenCV | Padrão da indústria; usa a GPU |
| Transcrição | faster-whisper (large-v3-turbo, int8) | Roda bem em 12 GB; só nos trechos de fala |
| Áudio | Silero VAD, DeepFilterNet, PANNs/BEATs/CLAP, librosa | Fala × ruído × eventos sonoros |
| Visão | SigLIP/CLIP (embeddings a 1–2 fps), OCR (PaddleOCR), VLM local via Ollama (Qwen-VL) **só em candidatos** | Barato no volume, inteligente onde importa |
| LLM local | Ollama (Qwen ~14B quantizado) | Classificação e resumos em massa sem custo |
| LLM de roteiro | **Claude Code (Pro)** via skills do repositório | Melhor qualidade de escrita, custo zero extra |
| API/Jobs | FastAPI + fila de jobs persistida no banco | Simples para um usuário; troca por Redis depois, se precisar |
| Banco | SQLite (SQLAlchemy + Alembic) | Zero infraestrutura; migração para Postgres sem reescrever |
| Contratos | JSON Schema → Pydantic (Py) e TypeScript (gerados) | Uma fonte de verdade entre engine e UI |
| UI | **Next.js + React + TypeScript** | Stack que você já domina; player com waveform e timeline |
| Export | OpenTimelineIO → FCPXML (+ EDL de reserva) + SRT | Importa no Resolve **gratuito** (não depende da API do Studio) |

> Versões e modelos exatos serão confirmados com benchmark na Fase 1. O que vale aqui é a *categoria* da ferramenta.

**Por que não NestJS/C# agora:** para um usuário, um backend único em Python evita uma ponte entre linguagens.
A arquitetura em portas/adaptadores permite colocar um gateway Nest depois, se o projeto virar produto.

### 5.3 Princípios

- **Pipeline de etapas puras:** cada etapa recebe artefatos e produz artefatos versionados.
  Chave de cache = hash(entrada + parâmetros + versão do modelo). Mudou um peso? Só as etapas seguintes rodam de novo.
- **Retomável:** 30 h de vídeo não podem recomeçar do zero por causa de uma queda.
- **Plugins por jogo:** `GameAdapter` (perfil de pesos, regiões de HUD para OCR, rótulos ignorados, leitor de logs do mod).
- **Humano no circuito:** a IA propõe e você decide. Toda decisão vira dado de treino.
- **Explicável:** cada segmento guarda *por que* recebeu aquela nota (quais sinais contribuíram).

### 5.4 Modelo de domínio

```
Projeto (ex.: "100 dias Valheim Hardcore", jogo, adaptador)
 └─ Sessão (uma gravação; arquivos master/proxy; faixas)
     ├─ Marcador (hotkey: tipo, t, dia)
     ├─ Sinal (série temporal: energia_fala, novidade_audio_jogo, movimento, similaridade_cena…)
     ├─ Evento (pontual: morte, risada, chefe, mudança de cena, evento do mod)
     └─ Segmento (intervalo + classe [farm, combate, exploração, construção, falha, humor, conquista, menu/loading]
                  + nota + explicação + decisão humana)
Narrativa
 └─ Capítulo/Dia → Beat (setup, conflito, falha, virada, conquista) → Segmentos + Fala sugerida
Timeline (versão exportável: clipes, velocidades/timelapse, marcadores, legendas do roteiro)
```

### 5.5 Estrutura do repositório

```
cronista/
├─ apps/
│  └─ studio/                    # Next.js — revisão e edição
├─ services/
│  └─ engine/                    # Python
│     ├─ src/cronista/
│     │  ├─ domain/              # entidades e regras puras
│     │  ├─ pipeline/            # orquestrador, etapas, cache, jobs
│     │  ├─ ingest/              # OBS, marcadores, proxies
│     │  ├─ audio/               # VAD, transcrição, eventos, baseline
│     │  ├─ vision/              # cenas, embeddings, OCR, VLM
│     │  ├─ adapters/            # minecraft/, valheim/, terraria/, eafc/, gta5/, generic/
│     │  ├─ relevance/           # fusão de sinais, segmentação, nota
│     │  ├─ story/               # capítulos, beats, story-pack
│     │  ├─ assembly/            # montagem da timeline, timelapse, shorts
│     │  ├─ finishing/           # mixagem, zoom, cor, música, VFX (Fase 8)
│     │  ├─ export/              # OTIO/FCPXML/EDL/SRT
│     │  └─ api/                 # FastAPI
│     └─ tests/                  # unitários + fixtures de vídeo anotadas
├─ packages/
│  ├─ contracts/                 # JSON Schemas → tipos gerados
│  └─ vfx-templates/             # Remotion (overlays)
├─ integrations/
│  ├─ obs/                       # script de hotkeys/marcadores
│  ├─ resolve/                   # script interno do DaVinci Resolve
│  └─ game-mods/                 # emissores de eventos por jogo (quando houver)
├─ .claude/skills/               # roteirista, humanizador, perfil-de-voz
├─ docs/                         # este plano + planos por fase + ADRs
└─ data/  (fora do git)          # projects/<id>/{masters→HD, proxies, cache, exports}
```

---

## 6. Roteiro e "anti cara de IA"

- **Perfil de voz:** as transcrições das suas próprias narrações viram um guia de estilo (gírias, tamanho de frase,
  bordões, como você faz piada). O roteiro é escrito *como você fala*, não como um texto genérico.
- **Skill `/humanizar`** (inspirada no Humanizer do GitHub, mas em pt-BR e para narração gamer): proíbe padrões
  típicos de IA (tríades, "não é só X, é Y", conclusões motivacionais, travessões em excesso, vocabulário inflado,
  frases simétricas) e reescreve com ritmo de fala.
- **Ritmo de referência:** você escolhe vídeos de criadores que admira e o sistema extrai **métricas de ritmo**
  (duração média de plano, proporção de timelapse, intervalo entre picos). Copia-se a cadência, não o conteúdo.
- **Entrega:** a narração entra como marcadores no Resolve + arquivo SRT alinhado, para você ler e gravar por cima.

---

## 6.1 Modelos locais (Ollama) — papel restrito

- O LLM local **não programa nem conversa**. Ele faz tarefas curtas e fechadas: rotular um segmento entre classes
  fixas, descrever um frame, resumir um trecho em 2 linhas.
- Saída sempre com **JSON Schema** (structured outputs do Ollama), temperatura baixa, exemplos no prompt, validação com
  Pydantic + nova tentativa. Se continuar inválido, o segmento cai para "revisão humana".
- Porta `LLMProvider` com adaptadores `OllamaProvider`, `ClaudeCodeProvider` (`claude -p`) e `NullProvider` (só heurística).
  Cada tarefa declara qual provedor usa, e a troca é por configuração.
- 12 GB de VRAM: um modelo por vez. O orquestrador agenda as etapas por modelo e descarrega com `keep_alive: 0`.
- A Fase 1 inclui um benchmark contra o gabarito. A tarefa só fica no modelo local se atingir a precisão mínima.

## 6.2 Cenas cinematográficas e timelapse de construção

- **Detectar** (Fase 3): movimento de câmera (fluxo óptico: parada, panorâmica, órbita), HUD oculto, beleza visual
  (preditor de estética sobre embeddings CLIP) e cenas por texto ("pôr do sol", "vista da base").
  O resultado vai para uma **biblioteca de B-roll** com tags, usada em aberturas, transições de dia e respiros.
- **Timelapse de construção** (Fase 6), em três níveis de qualidade:
  1. *Automático*: pega frames da gravação normal em que a construção aparece de ângulo parecido
     (similaridade + feature matching/homografia para alinhar) e monta um "progresso". Qualidade variável.
  2. *Ponto de câmera* (recomendado): você marca um local fixo no mundo e, ao fim de cada sessão de construção, volta
     lá e aperta a hotkey `Foto de progresso`. O sistema alinha as tomadas e gera um antes→depois suave.
  3. *Ferramenta do jogo*: Replay Mod (Minecraft), câmera livre (Valheim devcommands), Rockstar Editor (GTA V),
     replays (EA FC). Nesse caso a IA cataloga e encaixa as tomadas, mas a captura é sua.

## 6.3 Edição — divisão de trabalho

**O app gera um rough cut ("primeiro corte") rico. O acabamento é seu no Resolve.** O caminho é de mão única
(app → Resolve), e as mudanças feitas no Resolve não voltam para o app.

Regras de montagem automática:
- Corte na ação, com folga de 1–2 s antes e depois; nunca corta no meio de uma palavra (limites ajustados pelos timestamps de palavra do Whisper).
- Remoção de silêncio morto na sua fala; cortes J/L usando os limites da fala.
- Farm vira timelapse 4×–50× **pré-renderizado com FFmpeg/NVENC**, com o áudio do jogo removido
  (mais confiável que retime em massa no Resolve).
- Orçamento de tempo por dia/capítulo e ritmo guiado pelas métricas de referência.

Trilhas da timeline exportada:

| Trilha | Conteúdo |
|---|---|
| V1 | Gameplay cortada + timelapses |
| V2 | B-roll / cinemáticas |
| V3 | Cartelas "Dia N" (PNG/MOV com transparência, geradas pelo app) |
| A1 | Áudio do jogo |
| A2 | Sua narração ao vivo (microfone) |
| A3 | Vazia — narração nova gravada a partir do roteiro |
| A4 | Vazia — música |
| Legendas | Roteiro (SRT importado à parte) |

Marcadores coloridos: tipo do momento, fala sugerida e **sugestões de edição** (zoom aqui, efeito sonoro, freeze-frame + texto, meme).

Fica com você: gravar a narração, revisar o acabamento automático (6.4), ajustes finos e render.

## 6.4 Acabamento automático (zoom, VFX, cor, mixagem)

Cada efeito tem três modos, configuráveis por projeto:
`sugerir` (só marcador) · `aplicar editável` (via FCPXML/script do Resolve) · `aplicar renderizado` (feito pelo app).

**Não destrutivo:** todo efeito renderizado fica numa trilha **acima** do clipe original. Para desfazer, basta apagar ou desativar o clipe.

| Efeito | Como | Confiabilidade |
|---|---|---|
| Mixagem | Ducking do jogo sob a voz (sidechain calculado no app), normalização EBU R128 (−14 LUFS), cadeia de voz (redução de ruído, EQ, compressor), stems mixados + stems crus abaixo | Alta |
| Música | Biblioteca local sem direitos autorais, com tags de humor/BPM; escolha por clima do capítulo, cortes no beat, ducking | Média-alta |
| Zoom/punch-in | Em picos (grito, morte, risada), centrado na região de ação (saliência), com easing | Alta |
| Cor | LUT de "look" por série + normalização de exposição entre sessões | Alta (games quase não precisam) |
| VFX com template | **Remotion** (React/TSX) gerando overlays com transparência: contador de mortes, cartelas de dia, freeze-frame + texto, barra de progresso; shake em explosões; SFX de meme da sua biblioteca | Média — exige orçamento por minuto para não ficar repetitivo |

Regras anti-"cara de template": limite de efeitos por minuto, variação entre presets, intensidade ligada à nota do momento e
revisão no Studio. O que a IA decidir com baixa confiança fica só como `sugerir`.

## 6.5 Integração com o DaVinci Resolve gratuito

Levantamento feito de memória, **ainda não verificado** no software instalado. ✅ = alta confiança · ⚠️ = testar no spike.

**Disponível na versão gratuita:**
- ✅ Importar timeline de FCPXML/EDL/AAF (e OTIO nas versões recentes): cortes, várias trilhas, velocidade constante, marcadores.
- ⚠️ Transformações (zoom/posição), opacidade, transições, volume e **keyframes** via FCPXML: suporte parcial.
- ✅ Scripts Python/Lua **rodando de dentro do Resolve** (menu Workspace → Scripts e console).
  ⚠️ Scripts *externos* (o app controlando o Resolve de fora) costumam ser exclusivos do Studio.
- ✅ API de scripts: criar projeto, importar mídia, `ImportTimelineFromFile`, `AppendToTimeline`, `AddMarker` (cor, nome, nota),
  `SetProperty` (zoom/pan/crop **estáticos**), cor do clipe, LUT, fila de render. A API não cria keyframes.
- ✅ Fusion (Text+, keyframes), LUTs, color page, Fairlight (EQ, dinâmica, normalização de áudio), importar legendas SRT.
- ✅ 1080p60 sem limitação (o limite da versão gratuita é UHD 60 fps).

**Exclusivo do Studio (impacta o projeto):**
- ⚠️ Decodificação **e** codificação por GPU de H.264/HEVC no Windows → timeline pesada com gravações do OBS e render pela CPU.
- ✅ Recursos de IA (Voice Isolation, Magic Mask, legendas automáticas), redução de ruído de vídeo e parte dos Resolve FX.
  Nenhum é essencial: o app cobre voz, legendas e máscaras não são necessárias.

**Estratégia:**
- **Rota A (base):** o app gera FCPXML/OTIO + SRT e você importa pelo menu File → Import.
- **Rota B (quase um clique):** script interno do Cronista instalado na pasta de scripts do Resolve, executado pelo menu.
  Ele lê o pacote exportado pelo app e cria o projeto, importa a mídia e a timeline, adiciona marcadores coloridos com notas,
  aplica a LUT e configura o preset de render.
- Zooms animados e VFX: **renderizados pelo app** na trilha acima do original (ou composição Fusion importada, se o spike aprovar).
- Desempenho: o app gera **mídia intermediária DNxHR LQ/ProRes Proxy só dos trechos usados**, para a timeline rodar leve sem
  decodificação por GPU. O render final em H.264 sai pela CPU no Resolve, ou o app renderiza com NVENC a partir de um export intermediário.

**Checklist do spike (antes da Fase 6):** importar um FCPXML de teste com corte, velocidade, zoom com keyframe, transição,
volume e marcador; rodar um script interno de teste; medir a fluidez da timeline com master H.264 × proxy DNxHR.

Antes da Fase 6: **spike** de validação do que o Resolve gratuito importa de FCPXML (velocidade, transições,
volume, marcadores, relink) e do desempenho de decodificação dos masters. Se necessário, gerar mídia
intermediária só dos trechos usados.

---

## 7. Fases

Cada fase vira um plano de execução próprio (`docs/fase-N-*.md`), com tarefas, critérios de aceite e testes.
Só se avança com os critérios da fase anterior cumpridos.

### Fase 1 — Fundação e ingestão
- Monorepo, tooling (uv, ruff, mypy, pytest; pnpm, eslint), contratos, banco + migrações.
- Orquestrador de pipeline com cache por hash, jobs persistidos, retomada e logs estruturados.
- Script do OBS (hotkeys → `.markers.jsonl`) e guia de configuração do OBS.
- Ingestão: leitura das faixas, validação, proxy 360p no SSD, extração de áudio por faixa.
- CLI: `cronista ingest <pasta>` / `cronista status`.
- **Benchmark** dos modelos na RTX 3060.
- **Conjunto de referência:** 2–3 h de gameplay anotadas por você à mão (o que é farm e o que é legal). É o "gabarito" das fases seguintes.
- ✅ Aceite: ingerir 10 h sem intervenção, retomar após interrupção, proxies e marcadores corretos.

### Fase 2 — Análise de áudio
- Microfone: DeepFilterNet → Silero VAD → faster-whisper (com timestamps por palavra) → risada, grito, picos relativos.
- Jogo: classificação de eventos sonoros, baseline adaptativo, novidade espectral, detector de periodicidade (rotina).
- Saída: sinais e eventos de áudio no banco + relatório HTML da sessão (gráfico de sinais × tempo).
- ✅ Aceite: no gabarito, teclado e respiração **não** geram eventos; fala transcrita com WER aceitável; trechos rítmicos detectados como rotina.

### Fase 3 — Análise de vídeo e adaptadores de jogo
- Detecção de cena, movimento, embeddings de frames, detecção de menu/loading/pausa/idle.
- OCR em regiões de HUD definidas por adaptador (placar no EA FC, dia/hora quando visível).
- Interface `GameAdapter` + adaptador genérico + primeiro adaptador completo (Minecraft sugerido; mods de eventos opcionais).
- VLM local descrevendo apenas trechos candidatos.
- ✅ Aceite: menus/loading/idle detectados com alta precisão no gabarito; adaptador plugável sem tocar no núcleo.

### Fase 4 — Motor de relevância
- Fusão de sinais (áudio + vídeo + marcadores + eventos de mod) → segmentação → classificação → nota explicável.
- Lookback dos marcadores e refino dos limites dos segmentos.
- Métricas contra o gabarito (precisão/revocação de "farm" e de "momento legal") e medição da taxa de compressão real.
- ✅ Aceite: ≥ 85% dos momentos do gabarito aparecem no top de candidatos; farm identificado como farm.

### Fase 5 — Narrativa e roteiro
- Estrutura por dia/capítulo, arco (setup → sofrimento → virada → conquista), alocação de tempo por capítulo.
- `story-pack.json` compacto (eventos, resumos, citações suas, frames-chave) dentro do limite do plano Pro.
- Skills Claude Code: `/roteirizar`, `/humanizar`, perfil de voz. Fallback com LLM local.
- ✅ Aceite: roteiro de uma sessão real lido por você sem soar artificial; cada fala ligada a um segmento.

### Fase 6 — Montagem e exportação
- Montagem automática: cortes, timelapse/aceleração do farm, transições de dia, ritmo de referência.
- Exportação OTIO → FCPXML (+ EDL), marcadores coloridos por tipo, SRT do roteiro, relink para os masters do HD.
- Candidatos a Shorts (9:16, gancho nos 2 primeiros segundos).
- Mixagem automática básica: ducking + normalização de loudness + cadeia de voz (ganho alto com baixo risco).
- ✅ Aceite: importar no DaVinci Resolve gratuito sem erro, com mídia linkada e marcadores visíveis.

### Fase 7 — Studio de revisão e aprendizado
- App Next.js: lista de segmentos com player, waveform e sinais; aceitar/rejeitar/ajustar limites; editar roteiro; re-exportar.
- Progresso dos jobs em tempo real.
- Aprendizado: suas decisões recalibram os pesos por jogo (modelo simples e explicável primeiro).
- ✅ Aceite: um episódio completo produzido de ponta a ponta pelo fluxo Studio → Resolve.

### Fase 8 — Acabamento automático
- Zooms/punch-ins, LUT de série, música da biblioteca com corte no beat.
- Pacote de templates Remotion (contador de mortes, cartelas, freeze-frame + texto, barra de progresso) + SFX.
- Modos sugerir / editável / renderizado por efeito, controlados no Studio; orçamento de efeitos por minuto.
- ✅ Aceite: episódio exportado precisando só de narração gravada e ajustes finos; efeitos reversíveis no Resolve.

> O relatório HTML da Fase 2 garante visibilidade desde cedo. O Studio completo vem na Fase 7, quando já há dados reais para revisar.

---

## 8. Riscos

| Risco | Mitigação |
|---|---|
| Limites de uso do Claude Pro | Story-pack compacto; trabalho pesado no LLM local; Claude só no roteiro final |
| Processamento lento em 25+ h | Proxies, análise de frames em baixa taxa, VLM só em candidatos, cache por etapa |
| Jogos muito diferentes entre si | Adaptadores + perfil genérico; um jogo por vez |
| "Legal" é subjetivo | Marcadores + gabarito + aprendizado com o feedback |
| SSD cheio | Masters no HD; política de limpeza de cache por projeto |

## 9. Decisões em aberto

1. Jogo da calibração inicial (sugestão: Minecraft).
2. Há voz de amigos/Discord nas gravações? (afeta a Fase 2)
3. Nome definitivo do projeto.
4. Verificar na prática os itens ⚠️ da seção 6.5 (Resolve gratuito), com o Resolve instalado no PC de casa.
