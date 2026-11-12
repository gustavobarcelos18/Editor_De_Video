# Cronista — Plano Mestre

> Nome provisório. Aplicação pessoal que transforma dezenas de horas de gameplay gravada no OBS em uma
> **timeline pré-montada no DaVinci Resolve** + **roteiro de narração** para vídeos de "100 dias".

Criado em 2026-11-12 · Status: planejamento aprovado em linhas gerais; próxima etapa = detalhar a Fase 1.

Documentos relacionados:
- [01-historico-de-decisoes.md](01-historico-de-decisoes.md): cada pergunta feita durante o planejamento e a resposta/decisão tomada.

---

## 0. Como retomar (em outro PC ou nova sessão)

Clone o repositório, abra o Claude Code na pasta e cole:

```
Estou retomando o projeto Cronista (app pessoal de edição de gameplays de 100 dias).
Leia docs/00-plano-mestre.md inteiro, que é a fonte de verdade de tudo que já decidimos,
e docs/01-historico-de-decisoes.md para o contexto de cada decisão.
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
| Jogos | Minecraft, Valheim, Terraria, EA FC (modo carreira), GTA V com mods e outros. **O sistema deve ser universal**: nada calibrado para um jogo específico |
| Gravação | OBS, 1920×1080 a 60 fps; narra ao vivo parte do tempo; faixas de áudio separadas |
| Vozes | Só a voz do criador (sem Discord/amigos) |
| Processamento | **A cada sessão de gravação**, para acompanhar quanto "produto final" já existe ao longo da série |
| Ambientes | Código pode ser feito no PC do trabalho; produção (gravação, OBS, GPU, Resolve) no PC de casa |
| Marcador físico | Mesa de som FIFINE SC3: verificar se um botão pode virar marcador |
| Identidade | Identidade visual **e** sonora consistente; música da Biblioteca de Áudio do YouTube ou gerada por IA |
| Thumbnail | Sugestão de thumbnail a partir de um modelo do canal; formato a decidir junto |
| Shorts | Para todas as plataformas, edição genérica; **máximo 13 s**, prender em 3 s; começo, gancho e fim dentro dos 13 s |
| Backup | Por enquanto um HD; depois nuvem ou NAS, se o projeto funcionar |
| Fluxo git | Branch por fase, commits no nome do criador, revisão com Opus, CI no GitHub Actions |
| Hardware | RTX 3060 12 GB, 32 GB RAM, HD 2,5 TB, SSD 450 GB |
| Custo | Zero: modelos locais + Claude Code no plano Pro |
| Saída | Timeline pré-montada no DaVinci Resolve gratuito + Shorts/Reels |
| Produto | **Um único vídeo de 30–50 min** por série de 100 dias, montado a partir de várias sessões de gravação de duração variável (ex.: 3 h, 6 h, 10 h) |
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
1. Timeline para o DaVinci Resolve (cortes, trechos de farm em timelapse, B-roll, cartelas "Dia N", marcadores coloridos por tipo de momento).
2. Roteiro de narração sugerido, no estilo de fala do próprio criador, sem "cara de IA".
3. Acabamento automático e reversível: mixagem, zooms, cor, música e VFX de template (seção 6.4).
4. Candidatos a Shorts/Reels (trechos verticais 9:16 + gancho sugerido), para divulgar o canal em outras plataformas.

**Modelo de trabalho:** a máquina faz o trabalho braçal (assistir 25 h e separar o que presta), e o toque criativo
final fica com o criador no Resolve. É assim que os grandes criadores do formato trabalham: gravam boa parte da
jornada e compactam com edição e storytelling.

**Produto:** um único vídeo de 30–50 min por série de 100 dias. Ele sai de várias sessões de gravação de tamanhos
diferentes (ex.: 3 h, 6 h, 10 h), processadas uma a uma e montadas juntas no fim (seção 4.1).

**Fora de escopo (por enquanto):** substituir o Resolve como editor (a edição final e o acabamento criativo são do
criador, no Resolve), voz sintética, multiusuário/SaaS. O app **pode codificar vídeo** quando isso é só execução:
prévia MP4, timelapses, efeitos renderizados na trilha acima do original, Shorts finalizados e, como opção, a
codificação final com NVENC de um intermediário exportado pelo Resolve (seção 6.5). A arquitetura precisa permitir
crescer depois.

**Restrições:**
- Custo zero: tudo local (RTX 3060 12 GB, 32 GB RAM). Claude entra apenas via **Claude Code com o plano Pro**
  (headless `claude -p` ou skill rodada manualmente), sempre com entradas compactas por causa dos limites de uso.
  O plano Pro **não inclui acesso à API**, por isso o app não chama o Claude diretamente.
- Jogos variados: Minecraft, Valheim, Terraria, EA FC (modo carreira), GTA V com mods e outros → o núcleo é
  **universal (agnóstico de jogo)**. Funciona bem sem nenhuma configuração por jogo; um **perfil de jogo** declarativo
  (YAML, sem código) só refina, e é aprendido com o feedback da revisão. Mods que emitem eventos são bônus opcionais,
  nunca requisito.

---

## 2. Quanto gravar

| Referência | Conta |
|---|---|
| Taxa de compressão típica do formato | 30:1 a 50:1 |
| Vídeo final de 30–50 min | **≈ 20–35 h de gravação bruta** |
| Média por "dia" (fictício) | 25 h ÷ 100 dias ≈ **15 min de gravação por dia** |

A conta parte da duração do vídeo final, não do relógio do jogo: como o "dia" é fictício (seção 4), vale para
qualquer jogo. (Só como comparação: no Minecraft, 1 dia do jogo = 20 min reais.)

Recomendação: mirar **25 h** e usar a Fase 4 para medir a taxa real das suas sessões. Abaixo de ~15 h o vídeo
tende a ficar sem "respiro" de farm/timelapse e com poucas falhas para gerar humor.

**Armazenamento:** 1080p60 em NVENC CQP ~22 fica em ~10–20 GB/h → 25 h ≈ 250–500 GB.
→ **Masters no HD de 2,5 TB**. **Proxies 360p (~0,5 GB/h), cache e banco no SSD** (é ali que a análise lê o tempo todo).

**Sessões de duração variável:** o vídeo final é um só, mas sai de várias sessões de tamanhos diferentes
(ex.: 3 h, 6 h, 10 h). Uma sessão costuma cobrir vários "dias", e um "dia" pode começar numa sessão e terminar em
outra: o contador de dias continua de uma sessão para a seguinte (seção 4).

**Configuração do OBS sugerida:**
- Contêiner: **Hybrid MP4** (decidido): sobrevive a quedas e grava os marcadores do OBS dentro do arquivo, que o
  Cronista usa como fonte primária do tempo dos marcadores (ver seção 4). Se a gravação cair, o arquivo fica
  fragmentado e não finalizado; a ingestão faz um remux sem recodificar (`ffmpeg -c copy`) antes de usar.
  ⚠️ Confirmar no spike que o Resolve abre o arquivo remuxado.
- **60 fps exatos** (decidido): Vídeo → FPS comuns → 60, nunca 59,94. A timeline do Resolve, os timelapses, as
  cartelas e tudo que o app renderizar usam 60 fps, para os cortes não derivarem.
- **Vídeo 8-bit SDR** (o Resolve gratuito não lida bem com 10-bit/HDR, seção 6.5): encoder NVENC **H.264**,
  formato de cor **NV12**, espaço de cor **Rec. 709**, faixa parcial. Nunca P010/I010 nem HDR. HEVC 8-bit só depois
  de aprovado no spike do Resolve. A ingestão confere com `ffprobe` e avisa (ou converte) se vier 10-bit.
- Evitar pausar a gravação e a divisão automática de arquivo. O sistema tolera as duas coisas (seção 4), mas é menos
  um ponto de falha.
- Faixa 1 = mix · Faixa 2 = **jogo** · Faixa 3 = **microfone**. (Faixa 4 para Discord/amigos não é necessária:
  só a voz do criador aparece nas gravações.)
- **Microfone em duas fontes no OBS.** No OBS o filtro fica na fonte, não na faixa, e vale para todas as faixas que
  a fonte alimenta. Por isso o mesmo microfone entra duas vezes: uma fonte com supressão de ruído (RNNoise) roteada
  só para a faixa 1 (mix) e outra sem filtro roteada só para a faixa 3 (em Propriedades avançadas de áudio,
  desmarcar as demais faixas de cada fonte). A faixa 3 fica crua, e o pipeline faz o próprio tratamento.
  ⚠️ De memória: confirmar no PC de casa que o OBS aceita o mesmo dispositivo em duas fontes (guia da Fase 1).

---

## 3. O problema do ruído (teclado, respiração, pisadas)

Volume absoluto não serve como sinal. A estratégia tem quatro camadas:

1. **Separação física por faixa.** Teclado e respiração só existem na faixa do microfone. Pisadas, música e
   combate só existem na faixa do jogo. Nunca se analisa o mix.
2. **Microfone → só voz conta.**
   - VAD neural (Silero VAD) separa fala de não-fala. Clique de teclado e respiração são não-fala e são descartados.
   - Supressão de ruído (DeepFilterNet) antes da transcrição **só se o benchmark da Fase 1 mostrar que melhora o WER**:
     o Whisper já é robusto a ruído, e áudio filtrado às vezes piora a transcrição.
   - Características usadas: fala, risada, grito, aumento súbito de tom/energia **em relação à sua média da sessão**.
3. **Jogo → classificar o som, não medir o volume.**
   - Classificador de eventos sonoros pré-treinado (PANNs/BEATs/CLAP), com rótulos como explosão, música, impacto, multidão.
   - **Linha de base adaptativa:** mediana móvel por sessão e por "contexto visual" (descoberto automaticamente agrupando cenas parecidas, ex.: menu, área aberta, cidade, caverna; nada declarado por jogo). Pisada em pedra
     é repetitiva e periódica, então gera **baixa novidade**. O que pontua é a *mudança* em relação ao baseline
     (novidade espectral), não a altura do som.
   - Detecção de periodicidade: sons rítmicos e constantes (passos, mineração, corte de árvore) são sinal de **rotina/farm**.
4. **Calibração universal, refinada pelo uso.** Os pesos padrão valem para qualquer jogo (o perfil genérico).
   O feedback da revisão (aceito/rejeitado) recalibra primeiro os pesos do perfil genérico e, quando houver dados
   suficientes de um jogo, gera um **perfil de jogo declarativo** (YAML) com ajustes finos, por exemplo "neste jogo,
   som repetitivo de impacto = farm". O perfil é aprendido, não escrito à mão, e nunca é requisito (Fase 7).

---

## 4. Marcadores por hotkey

**Um toque já basta.** Ele quer dizer "aqui teve algo". Normalmente você aperta *depois* do acontecimento, então
o sistema olha para trás (janela padrão de 60–90 s, ajustável no perfil) e encontra os limites reais do momento
usando mudança de cena, picos de áudio e fala.

Hotkeys sugeridas (obrigatórias: `Momento` e `Início Dia N`; as demais são opcionais):

> **O "dia" é fictício.** É só a unidade de progresso e passagem de tempo da série, e não precisa corresponder a
> um dia do jogo (no EA FC ou no GTA V, por exemplo, não existe dia natural). Por isso a hotkey `Início Dia N` é
> obrigatória: ela é a única fonte universal de capítulos. OCR de dia/hora, quando o jogo mostra, serve só para conferência.
> A divisão gravada é uma proposta: a contagem que aparece na tela é decidida na edição (ver "Dias na tela" abaixo).

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

**Implementação:** a cada toque, o marcador é gravado por **dois caminhos independentes**:

1. **Marcador do OBS dentro do arquivo (fonte primária).** O OBS tem marcadores próprios para gravações em Hybrid
   MP4. Tecnicamente o formato chama isso de "capítulo", mas é só um ponto no tempo dentro do arquivo, com um nome:
   **não cria capítulo no vídeo final**, serve para indicar "aconteceu algo aqui". Os capítulos do vídeo (os dias) vêm
   só da hotkey `Início Dia N`. O OBS grava o marcador **no tempo da mídia**, então pausas já ficam descontadas, e ele
   vai dentro do arquivo certo, mesmo com divisão automática. Nome: `tipo|dia|id`.
2. **Diário `.markers.jsonl` (redundância e fonte da verdade dos detalhes).** Não grava "segundos desde o início",
   e sim um **diário de eventos** com relógio monotônico + UTC: `recording_started`, `paused`, `unpaused`,
   `file_changed` (com o caminho do novo arquivo), `recording_stopped` e cada `marker` (tipo, dia, id).

Na ingestão, o engine **reconstrói o tempo de mídia** a partir do diário (tempo do toque − início − pausas acumuladas,
dentro do arquivo vigente) e **reconcilia** com os marcadores do arquivo pelo `id`:
- os dois batem (tolerância ~1 s) → usa o marcador do arquivo;
- só existe o diário (arquivo sem marcadores, versão antiga do OBS) → usa o tempo reconstruído;
- divergem → usa o marcador do arquivo e registra um aviso no relatório da sessão;
- toque fora de gravação → ignorado com aviso.

Testes com fixtures sintéticas cobrem: gravação simples, com pausas, com divisão de arquivo e com queda (arquivo sem
`recording_stopped`). Um erro de algumas centenas de ms não importa, porque o lookback de 60–90 s absorve.
A versão mínima do OBS e o nome exato da API de marcadores serão confirmados na Fase 1.

**Quem cria o marcador (em aberto, seção 9).** ⚠️ De memória: o OBS 30.2+ tem uma hotkey nativa ("Adicionar marcador
de capítulo") que funciona sem instalar nada, mas é **uma tecla só e não guarda tipo nem dia**: todo toque viraria
`Momento`, e o `Início Dia N` ficaria indistinguível. Para ter tipo e dia, algo precisa criar o marcador com nome:
- **A (recomendada): programa do Cronista ao lado do OBS, via obs-websocket.** Cria o marcador do OBS com nome
  (⚠️ requisição `CreateRecordChapter`; versão mínima a confirmar), escreve o diário a partir dos eventos de
  gravação, pausa e troca de arquivo do próprio OBS, guarda o contador de dias e escuta num lugar só as hotkeys
  globais, as teclas F13–F24 e a FIFINE (MIDI/HID). Precisa estar aberto durante a gravação.
- **B: script Lua dentro do OBS.** Não exige instalar nada. ⚠️ Confirmar se a função de marcador com nome está
  exposta ao Lua. A FIFINE ficaria à parte. (Script Python dentro do OBS foi descartado: exige uma versão específica
  do Python instalada e configurada no OBS, e não há certeza de que a função de marcador esteja exposta.)
- **C: só a hotkey nativa.** Zero instalação; tipo e dias seriam marcados depois, no Studio. Quebra a regra de
  `Início Dia N` por hotkey.

**Contador de dias.** Uma tecla não carrega número: `Início Dia N` incrementa um contador guardado por projeto, que
continua de uma sessão para a outra (o "dia" pode atravessar sessões). Uma sessão que começa sem `Início Dia N`
continua o dia vigente.

**Dias na tela são decididos na edição** (decisão do criador). A contagem de dias aparece na tela do vídeo, mas o
número final e onde cada dia começa são decididos na hora da edição. O que é gravado com `Início Dia N` é uma
**proposta** de divisão: o app usa para montar a narrativa, as cartelas e o painel da série, e o criador ajusta no
Studio ou no Resolve. Por isso não há tecla de correção, e as cartelas/contador de dias saem editáveis (seção 6.3).
`Construção ▶` sem o `■` correspondente é fechada no fim da sessão, com aviso.

**Jogo rodando como administrador.** ⚠️ De memória: se o jogo roda elevado (ou o anti-cheat bloqueia teclas), um
programa sem elevação não recebe as hotkeys. Saídas: rodar o OBS/programa de marcadores também como administrador ou
usar um dispositivo físico (FIFINE via MIDI/HID, macropad). Verificar no PC de casa com os jogos da série.

**Dispositivo de marcação (a testar no PC de casa):** a mesa de som FIFINE SC3 é uma interface de áudio, e não se
sabe se os botões dela enviam algum evento ao PC. Teste na Fase 1 com um script que escuta eventos HID/MIDI:
1. Se algum botão gerar evento HID/MIDI → o Cronista mapeia esse botão para um marcador.
2. Se não gerar, mas a mesa tiver pads de efeito sonoro que tocam na saída → o app pode reconhecer aquele som
   específico na gravação como marcador (marcador por áudio). Funciona só se o som cair numa faixa gravada.
3. Se nada funcionar → teclas F13–F24 via software de macro, botões extras do mouse ou um macropad USB barato.

## 4.1 Processamento por sessão e painel da série

Cada sessão (de duração variável: 3 h, 6 h, 10 h…) é processada assim que a gravação termina (ingestão → análise →
nota). A narrativa completa do vídeo único é montada no fim, mas o app mantém um **painel da série** atualizado a cada
sessão:
- minutos estimados de "produto final" por sessão e acumulados × meta do vídeo (30–50 min);
- distribuição por tipo de momento (mortes/falhas, conquistas, chefes, construções, humor, farm);
- dias cobertos e capítulos que ainda estão "magros" (pouco material bom).

Isso responde, durante a série, "já tenho material suficiente?" e "o que está faltando gravar?". Arquiteturalmente,
o projeto é incremental: cada sessão é independente e cacheada, e só as etapas de narrativa e montagem consideram
todas as sessões juntas.

**Uso da GPU (decidido):** o processamento começa sozinho ao fim da gravação, mas **pausa** enquanto o OBS estiver
gravando ou um jogo em tela cheia estiver aberto (a RTX 3060 é a mesma), e retoma de onde parou quando o PC ficar
livre. Como o pipeline é retomável, pausar não perde trabalho.

---

## 5. Arquitetura

### 5.1 Visão geral

```
 OBS ──► gravação (Hybrid MP4) + .markers.jsonl   Mods do jogo ──► eventos (.jsonl) [opcional]
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
| Áudio | Silero VAD (o mesmo que o faster-whisper usa no filtro de VAD), DeepFilterNet **só se melhorar o WER no benchmark**, PANNs/BEATs/CLAP, librosa | Fala × ruído × eventos sonoros |
| Visão | SigLIP/CLIP (embeddings a 1–2 fps), OCR (**RapidOCR**, ONNX) **em frames do master**, VLM local via Ollama (Qwen-VL) **só em candidatos** | Barato no volume, inteligente onde importa |
| LLM local | Ollama (Qwen ~14B quantizado) | Classificação e resumos em massa sem custo |
| LLM de roteiro | **Claude Code (Pro)** via skills do repositório | Melhor qualidade de escrita, custo zero extra |
| API/Jobs | FastAPI + fila de jobs persistida no banco | Simples para um usuário; troca por Redis depois, se precisar |
| Banco | SQLite (SQLAlchemy + Alembic) | Zero infraestrutura; migração para Postgres sem reescrever |
| Contratos | JSON Schema → Pydantic (Py) e TypeScript (gerados) | Uma fonte de verdade entre engine e UI |
| UI | **Next.js + React + TypeScript** | Stack que você já domina; player com waveform e timeline |
| Export | OpenTimelineIO → FCPXML (+ EDL de reserva) + SRT | Importa no Resolve **gratuito** (não depende da API do Studio) |

> Versões e modelos exatos serão confirmados com benchmark na Fase 1. O que vale aqui é a *categoria* da ferramenta.
>
> Frameworks de ML padronizados em **PyTorch + ONNX Runtime**, para evitar um segundo framework de GPU com CUDA
> próprio no Windows. Por isso o OCR é RapidOCR (ONNX) e não PaddleOCR. O DeepFilterNet está sem atualização desde
> 2023 e pode não instalar com Python 3.12 e PyTorch recentes (⚠️ verificar); como ele só entra se melhorar o WER, a
> falta dele não bloqueia nada.

**Por que não NestJS/C# agora:** para um usuário, um backend único em Python evita uma ponte entre linguagens.
A arquitetura em portas/adaptadores permite colocar um gateway Nest depois, se o projeto virar produto.

### 5.3 Princípios

- **Pipeline de etapas puras:** cada etapa recebe artefatos e produz artefatos versionados.
  Chave de cache = hash(entrada + parâmetros + versão do modelo). Mudou um peso? Só as etapas seguintes rodam de novo.
- **Retomável:** 30 h de vídeo não podem recomeçar do zero por causa de uma queda.
- **Universal primeiro:** o perfil genérico tem que funcionar sozinho. `GameAdapter` / perfil de jogo (pesos, regiões
  de HUD para OCR, rótulos ignorados, leitor de logs de mod) é refinamento opcional, preferencialmente declarativo.
- **Humano no circuito:** a IA propõe e você decide. Toda decisão vira dado de treino.
- **Explicável:** cada segmento guarda *por que* recebeu aquela nota (quais sinais contribuíram).

### 5.4 Modelo de domínio

```
Projeto (uma série de 100 dias = um vídeo de 30–50 min; ex.: "100 dias Valheim Hardcore", jogo, perfil, contador de dias)
 └─ Sessão (uma gravação de duração variável: 3 h, 6 h, 10 h…; arquivos master/proxy; faixas)
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
│     │  ├─ profiles/            # perfil genérico (padrão) + carregador de perfis de jogo (YAML)
│     │  ├─ adapters/            # interface GameAdapter para leitores de mods (opcional, só se valer a pena)
│     │  ├─ relevance/           # fusão de sinais, segmentação, nota
│     │  ├─ story/               # capítulos, beats, story-pack
│     │  ├─ assembly/            # montagem da timeline, timelapse, shorts
│     │  ├─ finishing/           # mixagem, zoom, cor, música, VFX (Fase 8)
│     │  ├─ export/              # OTIO/FCPXML/EDL/SRT
│     │  └─ api/                 # FastAPI
│     └─ tests/                  # unitários + fixtures de vídeo anotadas
├─ packages/
│  ├─ contracts/                 # JSON Schemas → tipos gerados
│  ├─ brand-kit/                 # configuração e assets do brand kit (versionados; Git LFS se crescerem)
│  └─ vfx-templates/             # Remotion (overlays)
├─ integrations/
│  ├─ obs/                       # gravador de marcadores (mecanismo em aberto, seção 4) + guia do OBS
│  ├─ resolve/                   # script interno do DaVinci Resolve
│  └─ game-mods/                 # emissores de eventos por jogo (quando houver)
├─ profiles/                     # perfis de jogo declarativos (YAML), gerados/ajustados pelo feedback
├─ config/                       # dev.yaml / prod.yaml (versionados, sem caminhos pessoais) + *.local.yaml (fora do git)
├─ .claude/skills/               # /roteirizar, /humanizar (o perfil de voz é um guia de estilo usado por elas)
├─ docs/                         # este plano + planos por fase + ADRs
└─ data/  (fora do git)          # projects/<id>/{masters→HD, proxies, cache, exports}
```

### 5.6 Ambientes, fluxo de desenvolvimento e armazenamento

**Dois ambientes:**

| Ambiente | Onde | Para quê |
|---|---|---|
| `dev` | PC do trabalho | Escrever código, testes unitários, CI. Tudo precisa rodar **sem GPU** (fallback CPU, modelos pequenos ou mocks) |
| `prod` | PC de casa (RTX 3060) | Gravação, OBS, processamento real com GPU, Resolve, benchmarks |

- Configuração por perfil (`config/dev.yaml`, `config/prod.yaml`), versionada e sem caminhos pessoais; os caminhos de
  cada máquina ficam em `config/dev.local.yaml` / `config/prod.local.yaml` (fora do git), carregados por cima.
  Caminhos de mídia nunca fixos no código.
- Testes que precisam de GPU ou de mídia real são marcados (`@pytest.mark.gpu`, `@pytest.mark.media`) e rodam só no PC de casa.
- Fixtures sintéticas geradas com FFmpeg (vídeo de teste + tons/ruídos em faixas separadas) permitem testar o pipeline
  antes de existir gameplay real.

**Fluxo git:**
- Branch por fase (`fase/1-fundacao`, `fase/2-audio`, …), merge na `main` via pull request ao fim da fase.
- Commits no nome do criador (identidade git já configurada), mensagens no padrão Conventional Commits.
- Revisão com Opus antes do merge (`/code-review` no PR).
- GitHub Actions: lint (ruff, eslint), tipos (mypy, tsc) e testes unitários em CPU a cada push/PR, em **Ubuntu e
  Windows** (a produção é Windows; caminhos e ingestão precisam ser testados lá).

**Armazenamento e backup:**
- Camada `StorageBackend` (local agora; NAS ou nuvem depois) para que a troca não mexa no restante do código.
- Itens pequenos e valiosos (banco, marcadores, decisões de revisão, roteiros) têm backup desde o início: são poucos MB.
- **Política de retenção** após publicar o vídeo da série: manter só a mídia intermediária dos trechos usados (~dezenas de GB)
  e liberar os masters brutos (~centenas de GB), se o criador quiser.

---

## 6. Roteiro e "anti cara de IA"

- **Perfil de voz:** as transcrições das suas próprias narrações viram um guia de estilo (gírias, tamanho de frase,
  bordões, como você faz piada). O roteiro é escrito *como você fala*, não como um texto genérico.
- **Skill `/humanizar`**, adaptada do [Humanizer](https://github.com/blader/humanizer) (licença MIT: pode ser
  adaptado, mantendo o aviso de licença e o crédito). O original é baseado no guia da Wikipédia sobre sinais de texto
  feito por IA e parte da ideia de que o modelo escolhe sempre a formulação mais provável. Nossa versão é em pt-BR e
  para **narração falada** de gameplay:
  - **Fluxo do original, mantido:** auditar (marcar cada sinal, do mais forte ao mais fraco) → rascunhar a reescrita →
    conferir contra os padrões e contra os fatos do trecho → versão final. Nunca muda o que aconteceu no jogo; onde o
    texto ficar genérico, troca por um detalhe concreto e verdadeiro tirado do story-pack.
  - **Padrões que valem para fala** (dos 26 do original): "não é X, é Y"; frases de efeito e fechamentos dramáticos;
    "lições" de profundidade falsa; rodeios antes de chegar ao ponto; responder a objeções que ninguém fez; tríades
    forçadas; frases começando sempre igual; vocabulário inflado; importância exagerada; tom de vendedor; autoridade
    vaga ("dizem que…"); evitar o simples "é/tem"; resíduo de chatbot; explicar o que o público acabou de ver.
    Os "fracos sozinhos" (excesso de qualificadores, voz passiva) só contam quando aparecem juntos.
  - **Padrões que não se aplicam** (o roteiro é lido em voz alta): negrito, títulos, emojis, setas e aspas curvas.
  - **Acréscimos para pt-BR falado:** muletas de texto escrito ("vale ressaltar", "nesse sentido", "em suma",
    "jornada", "épico" em toda frase), frases longas demais para dizer num fôlego, gerúndio em cascata.
  - **Combinação com o perfil de voz:** o original aceita uma amostra de escrita para imitar a voz; aqui a amostra
    são as transcrições das suas narrações ao vivo (bordões, gírias, tamanho de frase).
- **Ritmo de referência:** você escolhe vídeos de criadores que admira e o sistema extrai **métricas de ritmo**
  (duração média de plano, proporção de timelapse, intervalo entre picos). Copia-se a cadência, não o conteúdo.
- **Fala ao vivo tem prioridade.** A narração ao vivo (A2) é a reação espontânea e nunca é coberta. O roteiro é
  **complemento**: entra só nos espaços sem fala ao vivo e explica o que foi feito, o tipo de decisão, o porquê das
  coisas, o que vem a seguir e o que você estava pensando no momento. O roteirista recebe, no story-pack, os trechos
  com fala ao vivo (com transcrição) para saber onde não escrever e para dar continuidade ao que você já disse.
- **Entrega:** a narração entra como marcadores no Resolve + arquivo SRT alinhado, para você ler e gravar por cima.

---

## 6.1 Modelos locais (Ollama) — papel restrito

**Por que o Ollama falhou no code assist e por que aqui é diferente:** code assist é a tarefa mais difícil para um
modelo pequeno (muito contexto, raciocínio em várias etapas, código longo). Um modelo de 7–14B não aguenta isso.
Aqui ele só recebe tarefas curtas e de resposta fechada, e a maior parte do trabalho nem usa LLM: transcrição,
detecção de voz e classificação de áudio/imagem ficam com modelos especializados.

Exemplo de chamada com formato obrigatório:

```python
resp = ollama.chat(model=cfg.model, messages=msgs,
                   format=SegmentLabel.model_json_schema(),
                   options={"temperature": 0.1})
label = SegmentLabel.model_validate_json(resp.message.content)
```

- O LLM local **não programa nem conversa**. Ele faz tarefas curtas e fechadas: rotular um segmento entre classes
  fixas, descrever um frame, resumir um trecho em 2 linhas.
- Saída sempre com **JSON Schema** (structured outputs do Ollama), temperatura baixa, exemplos no prompt, validação com
  Pydantic + nova tentativa. Se continuar inválido, o segmento cai para "revisão humana".
- Porta `LLMProvider` com adaptadores `OllamaProvider`, `ClaudeCodeProvider` (`claude -p`) e `NullProvider` (só heurística).
  Cada tarefa declara qual provedor usa, e a troca é por configuração.
- 12 GB de VRAM: um modelo por vez. O orquestrador agenda as etapas por modelo e descarrega com `keep_alive: 0`.
- A Fase 1 inclui um benchmark contra o gabarito. A tarefa só fica no modelo local se atingir a precisão mínima.

## 6.2 Cenas cinematográficas e timelapse de construção

A IA consegue **reconhecer** uma tomada cinematográfica, mas **não consegue criar** um ângulo que não foi gravado.
A câmera em primeira pessoa durante uma construção pula de um lado para o outro, e não dá para inventar um ângulo
fixo a partir disso.

- **Detectar** (Fase 3): movimento de câmera (fluxo óptico: parada, panorâmica, órbita), HUD oculto, beleza visual
  (preditor de estética sobre embeddings CLIP) e cenas por texto ("pôr do sol", "vista da base").
  O resultado vai para uma **biblioteca de B-roll** com tags, usada em aberturas, transições de dia e respiros.
- **Timelapse de construção** (Fase 6), em três níveis de qualidade:
  1. *Automático*: pega frames da gravação normal em que a construção aparece de ângulo parecido
     (similaridade + feature matching/homografia para alinhar) e monta um "progresso". Qualidade variável.
  2. *Ponto de câmera* (recomendado): você marca um local fixo no mundo e, ao fim de cada sessão de construção, volta
     lá e aperta a hotkey `Foto de progresso`. O sistema alinha as tomadas e gera um antes→depois suave.
     Custa uns 5 segundos por sessão.
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
| V3 | Cartelas e contador "Dia N" (sugestão do app; número final decidido na edição, por isso editáveis) |
| A1 | Áudio do jogo |
| A2 | Sua narração ao vivo (microfone) |
| A3 | Vazia — narração complementar gravada a partir do roteiro (só onde A2 não tem fala) |
| A4 | Vazia — música |
| Legendas | Roteiro (SRT importado à parte) |

Timeline em **60 fps exatos**, igual à gravação (seção 2).

Cartelas e contador de dias: como o número que aparece na tela é decidido na edição (seção 4), eles não podem sair
gravados na imagem. Duas formas, a escolher no spike: (1) título editável no Resolve (Text+/macro do Fusion, gratuito)
criado pelo FCPXML ou pelo script interno; (2) PNG/MOV com transparência que o app regenera depois do ajuste dos dias
no Studio. ⚠️ Não se sabe se o FCPXML cria título editável no Resolve gratuito.

⚠️ As faixas de áudio estão todas dentro do mesmo MP4. Ainda não se sabe se o Resolve respeita, vindo do FCPXML, qual
faixa embutida vai para qual trilha (faixa 2 → A1, faixa 3 → A2). Se não respeitar, o app passa a referenciar os
WAVs extraídos de cada faixa na ingestão, alinhados ao vídeo pelo tempo do arquivo. Teste no spike (seção 6.5).

Marcadores coloridos: tipo do momento, fala sugerida e **sugestões de edição** (zoom aqui, efeito sonoro, freeze-frame + texto, meme).
⚠️ O FCPXML não tem campo de cor de marcador, então a cor vem por outro caminho: EDL de marcadores no formato do
Resolve ou script interno (Rota B), conforme o spike (seção 6.5).
Piadas visuais ficam como sugestão, não como efeito aplicado: feitas automaticamente, são o que mais denuncia vídeo feito por IA.

Como o caminho é de mão única, a revisão no Studio (Fase 7) acontece **antes** de exportar.

Fica com você: gravar a narração (o Fairlight do Resolve grava direto na trilha A3), revisar o acabamento automático (6.4),
ajustes finos e render.

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

Regras anti-"cara de template": limite de efeitos por minuto, variação entre presets, intensidade ligada à nota do momento
(uma morte boba ganha um zoom leve; a morte para um chefe ganha o pacote completo) e revisão no Studio.
O que a IA decidir com baixa confiança fica só como `sugerir`.

A mixagem básica foi antecipada para a Fase 6 (ganho alto, risco baixo); o restante fica na Fase 8, porque só vale
polir quando o primeiro corte já estiver bom e o Studio permitir controlar os efeitos.

**Kit de identidade do canal (brand kit):** uma única configuração versionada, consumida por VFX, cartelas, shorts e
thumbnails, para o canal ter identidade visual **e** sonora:
- Visual: paleta, fontes, LUT de série, estilo de cartela "Dia N", contador de mortes, molduras.
- Sonora: vinheta de abertura, som de transição de dia, "som de morte" recorrente, loudness padrão, trilhas-tema por clima.
- Música: Biblioteca de Áudio do YouTube ou música gerada por IA. ⚠️ Antes de monetizar, verificar a licença de uso
  comercial de cada gerador de IA; vários planos gratuitos e alguns modelos locais proíbem uso comercial.

## 6.5 Integração com o DaVinci Resolve gratuito

Status: parcialmente verificado. Em 2026-11-12 o criador pesquisou as limitações do Resolve gratuito (v19/20) em
fontes públicas (página oficial do Resolve 20, Toolfarm, CineD, Motion Array, Artlist e fórum da Blackmagic).
A pesquisa confirma os limites de saída, codec e recursos; **não cobre** importação de FCPXML nem a API de scripts,
que continuam para o spike prático no PC de casa. ✅ = confirmado pela pesquisa · ☑️ = alta confiança, não
verificado · ⚠️ = testar no spike.

**Confirmado pela pesquisa (impacto no projeto):**
- ✅ Saída até UHD (3840×2160) a 60 fps, **sem marca d'água** e sem limite de tempo de uso. Vale também na vertical
  (o limite de 2160 fica na altura) → vídeo 1080p60 e shorts 1080×1920 cabem com folga.
- ✅ Fairlight (áudio) e Fusion (VFX, Text+, keyframes) completos na versão gratuita.
- ✅ **Formatos 10-bit não funcionam direito** (ex.: H.264 10-bit 4:2:2), nem HDR10+/Dolby Vision. Na prática, o
  gratuito trabalha bem com 8-bit → **o OBS grava em 8-bit SDR** (seção 2). Se algum arquivo vier 10-bit/HDR, a
  ingestão converte com FFmpeg antes de exportar.
- ✅ **Sem encoding acelerado por hardware**: o render sai pela CPU, mais lento. Com um vídeo de 30–50 min e vários
  renders de teste até a versão final, isso pesa (tempo a medir no spike).
- ✅ Uma única GPU de processamento no Windows (suficiente: só existe a RTX 3060).
- ✅ Exclusivos do Studio: Neural Engine (Super Scale, **Speed Warp**, Object Isolation, Magic Mask), redução de ruído
  de vídeo por IA, film grain, optical blur, edição por texto, vários Resolve FX, Dolby Atmos, Camera Tracker do Fusion.
- ✅ **Efeitos do Studio usados no gratuito não travam, mas deixam marca d'água** (ex.: correção de lente).
  → Regra do projeto: o app e os templates **nunca** aplicam efeitos exclusivos do Studio. Timelapse e aceleração
  saem prontos do FFmpeg (sem Speed Warp); limpeza de voz e legendas ficam com o app.

**Ainda não verificado (spike no PC de casa):**

Pesquisa na web acrescenta pouco aqui: FCPXML e scripting quase não aparecem nos comparativos free × Studio.
As fontes são a documentação oficial e o teste prático:
- **API de scripts:** o `README.txt` instalado com o Resolve, em
  `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\`. Ele corresponde exatamente à
  versão instalada e responde se o scripting externo funciona no gratuito. Cópias não oficiais na web servem só para
  adiantar o kit de teste, nunca como resposta final.
- **FCPXML:** notas de versão e manual oficial como preparação; a resposta vem da importação real.
- **Decodificação por GPU e HEVC:** só o teste responde (tocar uma gravação real observando o uso da GPU; importar,
  tocar e renderizar um HEVC 8-bit).

- ☑️ Importar timeline de FCPXML/EDL/AAF (e OTIO nas versões recentes): cortes, várias trilhas, velocidade constante, marcadores.
- ⚠️ Transformações (zoom/posição), opacidade, transições, volume e **keyframes** via FCPXML: suporte parcial.
- ☑️ Scripts Python/Lua **rodando de dentro do Resolve** (menu Workspace → Scripts e console).
  ⚠️ Scripts *externos* (o app controlando o Resolve de fora) costumam ser exclusivos do Studio.
- ☑️ API de scripts: criar projeto, importar mídia, `ImportTimelineFromFile`, `AppendToTimeline`, `AddMarker` (cor, nome, nota),
  `SetProperty` (zoom/pan/crop **estáticos**), cor do clipe, LUT, fila de render. A API não cria keyframes.
- ☑️ LUTs, color page e importação de legendas SRT.
- ⚠️ Decodificação de H.264/HEVC por GPU no Windows: a pesquisa só fala de *encoding*. Se o gratuito também não
  decodificar pela GPU, a timeline com as gravações do OBS fica pesada (daí a mídia intermediária abaixo).
- ⚠️ HEVC (H.265) 8-bit no Windows: a própria pesquisa recomenda confirmar nas notas de versão; por isso o padrão é H.264.
- ⚠️ **Cor dos marcadores:** o FCPXML não carrega cor. Alternativas no gratuito: importar marcadores por EDL no formato
  do próprio Resolve (de memória: menu de importação de marcadores de timeline a partir de EDL, com linhas
  `|C:ResolveColorBlue |M:nome |D:duração`) ou criar pelo script interno (`AddMarker` com cor).
- ⚠️ **Faixas de áudio embutidas:** se o FCPXML consegue mandar a faixa 2 do MP4 para A1 e a faixa 3 para A2. Se não,
  usar os WAVs extraídos de cada faixa (seção 6.3).
- ⚠️ **Hybrid MP4 após queda:** se o Resolve abre o arquivo remuxado sem recodificar (seção 2).

**Estratégia:**
- **Rota A (base):** o app gera FCPXML/OTIO + SRT e você importa pelo menu File → Import.
- **Rota B (quase um clique):** script interno do Cronista instalado na pasta de scripts do Resolve, executado pelo menu.
  Ele lê o pacote exportado pelo app e cria o projeto, importa a mídia e a timeline, adiciona marcadores coloridos com notas,
  aplica a LUT e configura o preset de render.
- Zooms animados e VFX: **renderizados pelo app** na trilha acima do original (ou composição Fusion importada, se o spike aprovar).
- Desempenho: o app gera **mídia intermediária DNxHR LQ/ProRes Proxy só dos trechos usados**, para a timeline rodar leve sem
  decodificação por GPU.
- **Render final (encoding sem GPU no gratuito)**, em duas rotas, escolhidas pela medição do spike:
  1. *Direto no Resolve pela CPU* (H.264): mais simples. Serve se o vídeo de 30–50 min renderizar em tempo aceitável.
  2. *Resolve exporta um intermediário (DNxHR SQ ou ProRes 422) e o app codifica com NVENC* (`cronista render`):
     usa a RTX 3060 e deixa o render bem mais rápido. Custo: o intermediário ocupa dezenas de GB por render
     (vai para o HD e é apagado após o upload).
- Antes de cogitar o Studio (US$ 295), medir as duas rotas. O plano não depende de nenhum recurso do Studio.

**Checklist do spike** (o kit de teste é montado na Fase 1, no PC do trabalho; roda no PC de casa assim que o Resolve
for instalado, e obrigatoriamente antes da Fase 6):
- Copiar o `README.txt` de scripting para `docs/referencias/` (para consulta em qualquer PC).
- Importar um FCPXML de teste com corte, velocidade, zoom com keyframe, transição, volume, marcador e relink para os masters,
  numa timeline de 60 fps exatos.
- Conferir se o FCPXML manda a faixa 2 do MP4 para A1 e a faixa 3 para A2; se não, repetir com os WAVs extraídos.
- Importar marcadores coloridos por EDL de marcadores no formato do Resolve e conferir cor, nome e duração.
- Abrir um Hybrid MP4 de uma gravação interrompida de propósito, depois do remux com `ffmpeg -c copy`.
- Criar uma cartela "Dia N" editável (título Text+/macro do Fusion) pelo FCPXML e pelo script interno, e trocar o número no Resolve.
- Rodar um script interno de teste (criar projeto, importar, marcadores, LUT).
- Medir a fluidez da timeline com master H.264 × proxy DNxHR (confirma se há decodificação por GPU).
- Testar um arquivo HEVC 8-bit gravado pelo OBS.
- Medir o tempo de render de 10 min de timeline pela CPU e pela rota intermediário + NVENC.
- Se o desempenho for ruim, gerar mídia intermediária só dos trechos usados.

## 6.6 Shorts (todas as plataformas)

Formato genérico que funciona em YouTube Shorts, TikTok e Reels:
- 1080×1920 (9:16), **duração máxima de 13 s**, legenda gravada no vídeo e conteúdo fora das áreas cobertas pela
  interface das plataformas (margens seguras).
- Estrutura: **0–3 s gancho** (o pico do momento ou a pergunta) → **3–10 s desenvolvimento** → **10–13 s desfecho**,
  com final que facilita o loop.
- Sem facecam: a tela inteira é gameplay.
- Reenquadramento 16:9 → 9:16 seguindo a região de ação (saliência); alternativa: gameplay no centro com fundo desfocado.
- Fontes de candidatos: marcadores `Engraçado`, mortes/falhas e conquistas com nota alta.

## 6.7 Thumbnails e títulos

Formato a decidir junto (ver decisões em aberto). Proposta inicial:
- Sem facecam: a thumbnail se apoia em frames do jogo, texto curto e elementos do brand kit (não em expressão do rosto).
- O app sugere frames candidatos (momentos de pico, antes/depois de construções, chefes) com boa composição.
- Um **modelo de thumbnail** do canal (layout, fontes, cores do brand kit, texto curto de 2–4 palavras) é preenchido
  automaticamente, gerando 2–3 variações para teste A/B no YouTube.
- O app também sugere títulos, passando pela mesma skill de humanização.

---

## 7. Fases

Cada fase vira um plano de execução próprio (`docs/fase-N-*.md`), com tarefas, critérios de aceite e testes.
Só se avança com os critérios da fase anterior cumpridos.

### Fase 1 — Fundação, ingestão e esqueleto de ponta a ponta
- Monorepo, tooling (uv, ruff, mypy, pytest; pnpm, eslint), contratos, banco + migrações.
- Ambientes `dev` (sem GPU) e `prod` (RTX 3060); fixtures sintéticas com FFmpeg; GitHub Actions (lint, tipos, testes,
  em Ubuntu e Windows).
- Orquestrador de pipeline com cache por hash, jobs persistidos, retomada e logs estruturados; projeto incremental por
  sessão; política de GPU (pausa com o OBS gravando ou jogo em tela cheia, seção 4.1).
- Gravador de marcadores (mecanismo da seção 4, decisão em aberto) com diário `.markers.jsonl` e contador de dias por
  projeto; guia de configuração do OBS (Hybrid MP4, 60 fps exatos, H.264 8-bit, microfone em duas fontes, jogo como
  administrador).
- Spike do dispositivo de marcação (FIFINE SC3: HID/MIDI ou marcador por áudio; senão, alternativas).
- **Kit de teste do Resolve gratuito** (seção 6.5): FCPXML de exemplo (corte, velocidade, zoom com keyframe,
  transição, volume, marcadores, relink), script interno mínimo, clipes 8-bit H.264 e HEVC gerados com FFmpeg e um
  roteiro de checagem com campos para anotar o resultado. Montado no PC do trabalho, executado no PC de casa.
- Ingestão: leitura das faixas, validação (8-bit, 60 fps), remux de arquivo interrompido, proxy 360p no SSD
  (H.264 + AAC com uma faixa só e `faststart`, para tocar no navegador, que só reproduz a primeira faixa de áudio),
  extração de áudio por faixa em WAV (alimenta a análise e o waveform do Studio).
- **Esqueleto de ponta a ponta:** gravação + marcadores → cortes simples ao redor de cada marcador → **prévia MP4
  renderizada com FFmpeg** (valida o fluxo sem depender do Resolve) + FCPXML mínimo (validado no Resolve quando possível).
- CLI: `cronista ingest <pasta>` / `cronista status` / `cronista preview`.
- **Benchmark** dos modelos na RTX 3060 (no PC de casa), incluindo o WER do Whisper com e sem DeepFilterNet.
- **Gabarito:** formato e ferramenta de anotação prontos. A anotação (2–3 h, começando pela gameplay de teste de ~30 min)
  acontece quando o criador puder; ela é obrigatória a partir da Fase 2.
- ✅ Aceite: ingerir 10 h sem intervenção, retomar após interrupção, proxies e marcadores corretos, prévia MP4 gerada
  a partir dos marcadores, CI verde.

### Fase 2 — Análise de áudio
- Microfone: (DeepFilterNet, se aprovado no benchmark) → Silero VAD → faster-whisper (com timestamps por palavra) → risada, grito, picos relativos.
- Jogo: classificação de eventos sonoros, baseline adaptativo, novidade espectral, detector de periodicidade (rotina).
- Saída: sinais e eventos de áudio no banco + relatório HTML da sessão (gráfico de sinais × tempo).
- ✅ Aceite: no gabarito, teclado e respiração **não** geram eventos; fala transcrita com WER aceitável; trechos rítmicos detectados como rotina.

### Fase 3 — Análise de vídeo e perfis de jogo
- Detecção de cena, movimento, embeddings de frames, detecção de menu/loading/pausa/idle — tudo universal.
- Tomadas cinematográficas e biblioteca de B-roll (seção 6.2).
- OCR (RapidOCR) em regiões de HUD opcionais, definidas no perfil do jogo (placar no EA FC, dia/hora quando visível),
  lido em frames do master (no proxy 360p o texto fica ilegível).
- **Perfil genérico universal** como padrão + perfis de jogo declarativos (YAML) opcionais; interface `GameAdapter`
  para leitores de mods, se algum dia valer a pena.
- VLM local descrevendo apenas trechos candidatos.
- ✅ Aceite: menus/loading/idle detectados com alta precisão no gabarito **sem nenhum perfil de jogo**; perfil plugável
  sem tocar no núcleo.

### Fase 4 — Motor de relevância
- Fusão de sinais (áudio + vídeo + marcadores + eventos de mod) → segmentação → classificação → nota explicável.
- Lookback dos marcadores e refino dos limites dos segmentos.
- Métricas contra o gabarito (precisão/revocação de "farm" e de "momento legal") e medição da taxa de compressão real.
- Painel da série (seção 4.1) no relatório: minutos estimados de produto final por sessão e acumulados.
- ✅ Aceite: ≥ 85% dos momentos do gabarito aparecem no top de candidatos; farm identificado como farm.

### Fase 5 — Narrativa e roteiro
- Estrutura por dia/capítulo, arco (setup → sofrimento → virada → conquista), alocação de tempo por capítulo.
- `story-pack.json` compacto (eventos, resumos, citações suas, frames-chave) dentro do limite do plano Pro.
- Skills Claude Code: `/roteirizar`, `/humanizar`, perfil de voz. Fallback com LLM local.
- ✅ Aceite: roteiro de uma sessão real lido por você sem soar artificial; cada fala ligada a um segmento.

### Fase 6 — Montagem e exportação
- Montagem automática: cortes, timelapse/aceleração do farm, transições de dia, ritmo de referência.
- Exportação OTIO → FCPXML (+ EDL), marcadores coloridos por tipo (EDL de marcadores ou Rota B, conforme o spike),
  SRT do roteiro, relink para os masters do HD, faixas de áudio mapeadas em A1/A2 (ou WAVs extraídos).
- Candidatos a Shorts (seção 6.6: até 13 s, gancho nos 3 primeiros segundos).
- Mixagem automática básica: ducking + normalização de loudness + cadeia de voz (ganho alto com baixo risco).
- ✅ Aceite: importar no DaVinci Resolve gratuito sem erro, com mídia linkada e marcadores visíveis.

### Fase 7 — Studio de revisão e aprendizado
- App Next.js: lista de segmentos com player, waveform e sinais; aceitar/rejeitar/ajustar limites; editar roteiro; re-exportar.
- Progresso dos jobs em tempo real e painel da série (seção 4.1).
- Aprendizado: suas decisões recalibram os pesos do perfil genérico e geram/ajustam perfis de jogo declarativos (modelo simples e explicável primeiro).
- ✅ Aceite: um vídeo completo produzido de ponta a ponta pelo fluxo Studio → Resolve.

### Fase 8 — Acabamento automático e identidade do canal
- Brand kit (identidade visual e sonora, seção 6.4).
- Zooms/punch-ins, LUT de série, música da biblioteca com corte no beat.
- Pacote de templates Remotion (contador de mortes, cartelas, freeze-frame + texto, barra de progresso) + SFX.
- Modos sugerir / editável / renderizado por efeito, controlados no Studio; orçamento de efeitos por minuto.
- ✅ Aceite: vídeo exportado precisando só de narração gravada e ajustes finos; efeitos reversíveis no Resolve.

### Fase 9 — Embalagem e distribuição
- Shorts finalizados: reenquadramento 9:16, legenda gravada, margens seguras, gancho em 3 s, máximo 13 s (seção 6.6).
- Thumbnails a partir do modelo do canal, com 2–3 variações (seção 6.7).
- Sugestões de título humanizadas.
- ✅ Aceite: o vídeo da série publicado com thumbnail, título e pelo menos 3 shorts gerados pelo app e aprovados pelo criador.

> O relatório HTML da Fase 2 garante visibilidade desde cedo. O Studio completo vem na Fase 7, quando já há dados reais para revisar.

---

## 8. Riscos

| Risco | Mitigação |
|---|---|
| Limites de uso do Claude Pro | Story-pack compacto; trabalho pesado no LLM local; Claude só no roteiro final |
| Processamento lento em 25+ h | Proxies, análise de frames em baixa taxa, VLM só em candidatos, cache por etapa |
| Jogos muito diferentes entre si | Núcleo universal só com sinais agnósticos (fala, novidade, ritmo, cena, marcadores); perfis declarativos como refinamento opcional |
| "Legal" é subjetivo | Marcadores + gabarito + aprendizado com o feedback |
| SSD cheio | Masters no HD; política de limpeza de cache por projeto |
| HD único com as gravações brutas | Backup imediato do que é pequeno (banco, marcadores, roteiros); NAS/nuvem depois; política de retenção |
| PC de desenvolvimento sem GPU | Fallback CPU, mocks e fixtures sintéticas; testes de GPU só no PC de casa |
| Gabarito atrasado | Fase 1 não depende dele; a partir da Fase 2 ele é obrigatório para medir qualidade |
| Render lento no Resolve gratuito (sem encoding por GPU) | Medir no spike; rota intermediário + NVENC pelo app (seção 6.5) |
| Efeito exclusivo do Studio deixar marca d'água | App e templates nunca usam recursos do Studio; timelapse e limpeza de voz feitos fora do Resolve |
| Licença de música gerada por IA | Verificar uso comercial antes de monetizar; Biblioteca de Áudio do YouTube como padrão seguro |
| Sistema universal acerta menos que um ajustado por jogo | Perfis declarativos aprendidos com o feedback da revisão |
| Processamento disputando a GPU com o jogo | Pausa automática com o OBS gravando ou jogo em tela cheia; pipeline retomável (seção 4.1) |
| Hotkeys bloqueadas por jogo como administrador ou anti-cheat | OBS/gravador de marcadores também como administrador ou dispositivo físico (MIDI/HID) (seção 4) |
| Gravação interrompida deixa o Hybrid MP4 sem finalizar | Remux sem recodificar na ingestão; testado no spike (seções 2 e 6.5) |
| Dependências de ML quebrando no Windows/Python 3.12 | PyTorch + ONNX Runtime só; RapidOCR; DeepFilterNet opcional; CI também em Windows (seção 5.2) |

## 9. Decisões

**Já decididas:**
- Sistema universal, sem jogo de calibração específico.
- Só a voz do criador nas gravações.
- Nome "Cronista" mantido (o nome não é prioridade).
- Processamento a cada sessão de gravação, com painel da série.
- Código no PC do trabalho; produção no PC de casa.
- Fluxo git: branch por fase, commits no nome do criador, revisão com Opus, CI no GitHub Actions.
- O "dia" é fictício (unidade de progresso); hotkey `Início Dia N` obrigatória (seção 4).
- Fala ao vivo tem prioridade; o roteiro é complemento explicativo (seção 6).
- Contêiner Hybrid MP4; marcadores do OBS dentro do arquivo + diário de eventos, com reconciliação (seções 2 e 4).
- Sem facecam (seções 6.6 e 6.7).
- Produto: **um único vídeo de 30–50 min** por série, montado a partir de sessões de duração variável (3 h, 6 h, 10 h…) (seções 0.1, 1 e 2).
- O app não substitui o Resolve como editor, mas pode codificar vídeo quando é só execução (seção 1).
- Marcador = "aconteceu algo aqui" (ponto no tempo dentro do arquivo); os capítulos do vídeo vêm só de `Início Dia N`,
  com contador de dias persistido por projeto (seção 4).
- A contagem de dias aparece na tela, mas o número final e a divisão são decididos na edição; `Início Dia N` é proposta,
  e cartelas/contador saem editáveis (seções 4 e 6.3).
- Gravação e timeline em 60 fps exatos; microfone em duas fontes no OBS (RNNoise só na do mix) (seção 2).
- Processamento automático ao fim da gravação, com pausa enquanto o OBS grava ou um jogo em tela cheia está aberto (seção 4.1).
- ML em PyTorch + ONNX Runtime; OCR com RapidOCR em frames do master; DeepFilterNet só se melhorar o WER (seção 5.2).
- CI em Ubuntu e Windows; configuração versionada sem caminhos pessoais + `*.local.yaml` fora do git (seção 5.6).

**Em aberto:**
1. Verificar na prática os itens ☑️/⚠️ da seção 6.5 (FCPXML, scripts, decodificação por GPU, HEVC e tempo de render),
   com o Resolve instalado no PC de casa. Os limites gerais do gratuito já foram confirmados pela pesquisa do criador.
2. Testar se a FIFINE SC3 serve como dispositivo de marcação (seção 4).
3. Gravar a gameplay de teste (~30 min, com faixas separadas e marcadores) e anotar o gabarito.
4. Modelo de thumbnail do canal (seção 6.7): definir juntos.
5. Identidade visual e sonora do canal: definir juntos (paleta, fontes, vinheta, sons recorrentes).
6. Quem cria o marcador com tipo e dia no OBS (seção 4): A, programa ao lado do OBS via obs-websocket (recomendada);
   B, script Lua; C, só a hotkey nativa.
