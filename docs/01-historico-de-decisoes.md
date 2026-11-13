# Histórico de decisões

Registro, em ordem, de cada pergunta feita durante o planejamento (2026-11-12) e da resposta ou decisão tomada.
O detalhe técnico de cada item está no [plano mestre](00-plano-mestre.md), na seção indicada.

---

## 1. Ideia inicial

**Pedido:** criar uma aplicação que entenda do início ao fim as horas de gameplay gravadas, identifique o que é
interessante para o público e faça cortes automáticos, separando o que é legal de assistir do que é farm.
Precisa ser profissional, com arquitetura e organização, e a melhor forma de construir deve ser sugerida.

**Resposta:** o sistema combina vários sinais (voz, áudio do jogo, vídeo, contexto via LLM, marcadores manuais),
dá uma nota a cada trecho e monta a narrativa. Python no núcleo, FFmpeg, pipeline em etapas com cache, banco
SQLite/Postgres, interface de revisão e exportação para o editor. → Plano mestre, seções 1 e 5.

## 2. Respostas do criador ao questionário

| Pergunta | Resposta |
|---|---|
| Jogos | Jogos em geral: Minecraft, Valheim, Terraria, EA FC modo carreira, GTA V com mod, entre outros |
| Gravação | OBS, 1920×1080 a 60 fps; narra ao vivo algumas coisas; consegue gravar faixas separadas |
| Narração | Quer que o projeto também sugira narrações para ilustrar melhor cada momento |
| Duração do produto | Vídeo de 100 dias com 30 a 50 minutos |
| Hardware | RTX 3060 12 GB VRAM, 32 GB RAM, HD 2,5 TB, SSD 450 GB |
| Custo | Local e grátis se possível; usar o plano Claude Pro ou outra ferramenta integrada para melhor resultado; custo zero |
| Saída | Timeline pré-montada no DaVinci Resolve; Shorts para divulgar em outras plataformas |
| Roteiro | Somente o roteiro, nada de cara de IA; implementar uma skill no estilo do Humanizer do GitHub |
| O que é "legal" | Percepção pessoal: muitas mortes e falhas em desafios difíceis (mostrar o sofrimento), falhas como humor, mas o foco é o storytelling: piadas, conquistas, falhas, chefes derrotados, construções concluídas |
| Marcadores | Aceita apertar uma tecla para marcar |
| Criadores de referência | Baronismo, Xedou, Trousy, Promptz |
| Público do app | Só para o criador, mas estruturado para escalar no futuro |
| Linguagens conhecidas | C#, Python, Next.js, React, NestJS, JavaScript, TypeScript |
| Formato do plano | Versão completa, em grandes fases (ex.: 7); cada fase vira um plano de execução próprio, implementado de forma segura e calculada |

## 3. Ruído: teclas, respiração e pisadas

**Pergunta:** identificar teclas do teclado, respiração e a própria pisada do personagem (na grama é mais suave,
na pedra mais alta) seria um problema. Isso precisa ser pensado.

**Decisão:** volume absoluto não é usado como sinal. Quatro camadas: separação por faixa; no microfone, só a fala
conta (VAD + supressão de ruído); no jogo, classificar o tipo de som e medir a novidade em relação ao padrão da
sessão (sons rítmicos = farm); calibração por jogo com o feedback da revisão. → Seção 3.

> **Parcialmente substituído pelos §15 e §18.** A supressão de ruído (DeepFilterNet) só entra se melhorar o WER no
> benchmark (§18, risco 10), e a calibração por jogo virou perfil declarativo aprendido com o feedback, sobre um
> perfil genérico universal (§15).

## 4. Marcadores: início e fim, ou um toque só?

**Pergunta:** é preciso marcar o início e o final do acontecimento, ou só marcar para deixar claro que há algo ali?

**Decisão:** um toque basta. O sistema olha 60–90 s para trás e encontra os limites reais. Início e fim só para
construções (viram timelapse). Hotkeys opcionais por tipo e uma de "Início Dia N". → Seção 4.

> **Substituído pelos §14 e §20.** A hotkey de dia passou a ser obrigatória (§14) e hoje se chama `Novo dia`, sem
> número: grava só onde o dia começa, e o número é definido na edição (§20).

## 5. Quantas horas gravar

**Pergunta:** quantas horas de gravação são necessárias para ter com certeza 30–50 min de produto final?

**Decisão:** mirar 25 h (faixa de 20–35 h), pela compressão típica de 30:1 a 50:1. No Minecraft, 100 dias ≈ 33 h
reais (17–25 h pulando noites). A Fase 4 mede a taxa real. → Seção 2.

> **Atualizado pelos §15 e §19.** A conta passou a partir da duração do vídeo final, sem depender do relógio do
> Minecraft (§15), e a faixa de 20–35 h foi explicada como a faixa central de 15–42 h (§19, item 5).

## 6. Primeira versão do plano

**Decisão:** 7 fases (fundação, áudio, vídeo, relevância, narrativa, montagem, Studio). Usar o plano Pro via
Claude Code, porque o Pro não inclui API. Skill de humanização em português, calibrada pelas narrações
transcritas do criador. NestJS e C# ficaram de fora por enquanto, para evitar ponte entre linguagens. → Seção 7.

> **Atualizado pelos §10 e §13.** O plano tem hoje 9 fases: a Fase 8 (acabamento automático) entrou no §10 e a
> Fase 9 (embalagem e distribuição) no §13.

## 7. Como usar um modelo local do Ollama

**Pergunta:** como implementar um modelo local do Ollama? Na última vez que foi usado para code assist, não funcionou bem.

**Decisão:** o LLM local fica só com tarefas curtas e fechadas (rotular trecho, descrever frame), com saída em
JSON Schema, validação e nova tentativa. Interface `LLMProvider` trocável (Ollama, Claude Code, só heurística).
Um modelo por vez na GPU. A tarefa só fica no local se passar no benchmark contra o gabarito. → Seção 6.1.

## 8. Cenas cinematográficas e timelapse de construção

**Pergunta:** a IA consegue entender tomadas de câmera cinematográficas e registrar isso, por exemplo, numa timelapse de construção?

**Decisão:** a IA reconhece tomadas cinematográficas (movimento de câmera, HUD oculto, beleza visual, busca por texto)
e monta uma biblioteca de B-roll, mas não cria ângulos que não foram gravados. Timelapse de construção em três níveis:
automático, ponto de câmera fixo com a hotkey `Foto de progresso` (recomendado) e ferramenta do jogo (Replay Mod,
câmera livre, Rockstar Editor, replays). Nova hotkey `Cinemática`. → Seção 6.2.

## 9. Como a edição será feita

**Pergunta:** como a edição será feita?

**Decisão:** o app monta o primeiro corte (rough cut) e o acabamento fica no Resolve. Regras de montagem (corte na
ação, nunca no meio de uma palavra, remoção de silêncio, cortes J/L, farm em timelapse pré-renderizado), layout de
trilhas V1–V3 / A1–A4 + legendas, marcadores coloridos com sugestões de edição. Caminho de mão única. → Seção 6.3.

> **Layout de trilhas substituído pelo §21.** Hoje são V1–V5 / A1–A7: efeitos renderizados, overlays, SFX e stems
> crus ganharam trilha própria; B-roll passou para V3 e cartelas para V5.

## 10. VFX, zoom, cor e mixagem automáticos

**Pergunta:** não teria como adicionar VFX, zooms, ajuste de cores e mixagem automáticos?

**Decisão:** sim, com três modos por efeito (sugerir, aplicar editável, aplicar renderizado) e sempre reversível
(efeito renderizado numa trilha acima do original). Mixagem antecipada para a Fase 6; zoom, cor, música e VFX
(Remotion) na nova **Fase 8**. Regras contra "cara de template". → Seções 6.4 e 7.

## 11. O que o DaVinci Resolve gratuito aceita

**Pergunta:** verificar quanto o Resolve gratuito aceita / o que podemos fazer com ele.

**Situação:** a busca na web foi interrompida e o Resolve não estava instalado no PC do trabalho, então o levantamento
foi feito de memória, com nível de confiança. Pontos principais: importa timeline de arquivo; scripts rodam de dentro
do Resolve (externos provavelmente só no Studio); sem decodificação/codificação por GPU de H.264/HEVC no Windows.
Estratégia com Rota A (importar arquivo) e Rota B (script interno), efeitos animados renderizados pelo app e mídia
intermediária só dos trechos usados. **Pendente:** verificação prática no PC de casa. → Seção 6.5.

> **Parcialmente substituído pelos §16 e §17.** A pesquisa do criador confirmou que o gratuito não tem *encoding* por
> GPU. A *decodificação* por GPU não foi confirmada nem descartada: passou a ser item de teste no spike. O scripting
> externo também segue como teste, com o `README.txt` instalado com o Resolve como fonte oficial.

## 12. Documentação e repositório

**Pedido:** estruturar tudo em documento para retomar no PC de casa; depois, colocar no repositório e subir no GitHub;
por fim, atualizar os documentos sem retirar nenhuma informação conversada.

**Decisão:** o repositório git é a fonte de verdade (`docs/00-plano-mestre.md` + este histórico). O GitHub CLI não
estava instalado no PC do trabalho, então o repositório remoto precisa ser criado manualmente (ver README).
Um documento no claude.ai chegou a ser iniciado e ficou incompleto (4 de 8 seções); o repositório o substitui.

> **Resolvido.** O repositório remoto foi criado (https://github.com/gustavobarcelos18/Editor_De_Video) e integrado
> (commits `bf41e4f` e `32c1483`); o README traz o comando de clone.

## 13. Pendências antes da Fase 1

**Pergunta:** o que mais precisamos conversar? Foram levantados 12 pontos; respostas do criador e decisões:

| # | Tema | Resposta do criador | Decisão / impacto no plano |
|---|---|---|---|
| 1 | Jogo inicial, vozes, nome | Não será Minecraft: precisa ser universal. Só a própria voz. O nome não importa tanto | Perfil genérico universal como padrão; perfis por jogo opcionais e declarativos. Sem faixa de Discord. Nome "Cronista" mantido (seções 1, 5.3, Fase 3) |
| 2 | Gravações de teste | Não tem ainda; vai gravar ~30 min assim que possível | Fixtures sintéticas com FFmpeg até lá. Observação: a gameplay serve para **calibrar e testar**, não para treinar um modelo (seção 5.6) |
| 3 | Gabarito | Topa anotar, mas não agora | Fase 1 não depende do gabarito; ele é obrigatório a partir da Fase 2 |
| 4 | Onde programar | Código neste PC (trabalho); produção no PC de casa | Ambientes `dev` (sem GPU) e `prod` (RTX 3060) (seção 5.6) |
| 5 | Quando processar | A cada sessão de gravação; ajuda a saber quanto produto final já existe | Projeto incremental + painel da série (seção 4.1) |
| 6 | Ver o resultado no Resolve cedo | Não consegue configurar ou testar o Resolve agora | Esqueleto de ponta a ponta na Fase 1 com **prévia MP4 via FFmpeg** (não depende do Resolve) + FCPXML mínimo validado depois |
| 7 | Teclas dos marcadores | Tem uma mesa de som FIFINE SC3; dá para usar um botão dela? | Spike na Fase 1: evento HID/MIDI → marcador por áudio → alternativas (F13–F24, mouse, macropad) (seção 4) |
| 8 | Música e efeitos | Biblioteca de Áudio do YouTube ou gerada por IA; identidade visual e sonora é importante | Brand kit visual e sonoro; alerta de licença comercial para música de IA (seção 6.4) |
| 9 | Thumbnail e títulos | Quer sugestão de thumbnail; criar um modelo do canal para gerar identidade; decidir junto | Seção 6.7 + nova Fase 9; formato do modelo em aberto |
| 10 | Shorts | Todas as plataformas, edição genérica, prender em 3 s, **máximo 13 s** com começo, gancho e fim | Especificação na seção 6.6; candidatos na Fase 6, finalização na Fase 9 |
| 11 | Backup | Se funcionar, assinar nuvem ou montar NAS | `StorageBackend` trocável; backup imediato do que é pequeno; política de retenção (seção 5.6) |
| 12 | Fluxo git | Branch por fase, commits no nome dele, revisão com Opus, CI no GitHub Actions se necessário | Seção 5.6 |

## 14. Revisão do plano: dúvidas levantadas pelo Claude

| # | Dúvida | Resposta do criador | Decisão / impacto no plano |
|---|---|---|---|
| 1 | O que é "dia" em jogos sem dia (EA FC, GTA V)? | O dia é fictício, só define progresso e passagem de tempo | Hotkey `Início Dia N` passa a ser obrigatória e é a fonte universal de capítulos (seção 4) |
| 2 | Fala ao vivo × roteiro | A fala ao vivo é preferida (reação espontânea); o roteiro complementa explicando o que foi feito, as decisões, o porquê, o que vem a seguir e o que ele pensava | Roteiro só nos espaços sem fala ao vivo; story-pack inclui a fala ao vivo transcrita (seções 6 e 6.3) |
| 3 | MKV ou Hybrid MP4? | Hybrid MP4 | Seção 2 |
| 4 | Pausa/divisão de arquivo no OBS quebram o tempo dos marcadores | Perguntou como resolver | Capítulo no arquivo (tempo de mídia) como fonte primária + diário de eventos com pausas e trocas de arquivo, reconciliados na ingestão; testes com fixtures (seção 4) |
| 5 | Usa facecam? | Não | Shorts e thumbnails só com gameplay (seções 6.6 e 6.7) |

> **Item 1 atualizado pelo §20:** a hotkey obrigatória hoje se chama `Novo dia` e não carrega número.
>
> **Item 4 atualizado pelo §18 (risco 4):** "capítulo no arquivo" passou a se chamar "marcador do OBS".

## 15. Ajustes de consistência

**Pedido:** reforçar que o sistema precisa ser universal, corrigir a ordem das seções e criar o `CLAUDE.md`.
A verificação do Resolve gratuito fica com o criador, que vai pesquisar e trazer o resultado.

**Decisão:** removidas as menções a calibração/adaptadores por jogo no núcleo (seções 2, 3, 4, 5.5, Fase 7 e riscos):
o perfil genérico é o padrão, perfis de jogo são YAML aprendidos com o feedback, e `adapters/` fica só para leitores
de mods opcionais. A conta de horas da seção 2 passou a partir do vídeo final (~15 min de gravação por "dia"), sem
depender do relógio do Minecraft. Seção 6.5 movida para antes da 6.6. Criado o `CLAUDE.md` com as regras que não se negociam.

## 16. Pesquisa do Resolve gratuito e referência do humanizador

**Entrada do criador:** pesquisa "Limitações do DaVinci Resolve gratuito (v19/20)" e o link do Humanizer
(https://github.com/blader/humanizer) como base da skill de humanização.

**Decisões:**
- Resolve: confirmados saída até UHD 60 fps sem marca d'água, Fairlight e Fusion completos, sem encoding por GPU,
  formatos 10-bit/HDR mal suportados, recursos de IA e vários FX só no Studio (e com marca d'água se usados no gratuito).
  → OBS grava H.264 8-bit SDR (seção 2); app nunca usa recurso do Studio; render final com duas rotas a medir
  (CPU no Resolve ou intermediário + NVENC pelo app). FCPXML, API de scripts, decodificação por GPU e HEVC continuam
  para o spike (seção 6.5).
- Humanizador: a skill `/humanizar` adapta o Humanizer (MIT, baseado no guia da Wikipédia sobre sinais de texto de IA):
  mantém o fluxo auditar → rascunhar → conferir → finalizar, seleciona os padrões que valem para fala, descarta os de
  formatação e acrescenta padrões de pt-BR falado; a amostra de voz são as narrações ao vivo do criador (seção 6).

## 17. Como verificar o que falta no Resolve gratuito

**Entrada do criador:** documento "DaVinci Resolve gratuito: pendente de teste", com quatro pontos que a pesquisa não
cobriu (importação de FCPXML, scripting externo no gratuito, decodificação por GPU, HEVC no Windows) e o aviso de
que FCPXML e scripting quase não aparecem nos comparativos free × Studio.

**Decisão:** teste prático, com a documentação oficial como preparação. Fonte da API de scripts = `README.txt`
instalado com o Resolve (versão exata). O kit de teste (FCPXML, script interno, clipes H.264/HEVC 8-bit, roteiro de
checagem) entra como tarefa da Fase 1 e roda no PC de casa. → Seções 6.5 e 7 (Fase 1).

## 18. Revisão do plano: inconsistências e riscos técnicos

**Pedido:** analisar o projeto e os documentos em busca de falhas, dúvidas, pontos em aberto e melhorias.

**Inconsistências corrigidas:**

| # | Ponto levantado | Resposta do criador | Decisão / impacto no plano |
|---|---|---|---|
| 1 | Diagrama da seção 5.1 mostrava gravação em `.mkv` | Alterar para Hybrid MP4 | Diagrama corrigido |
| 2 | "Render final fora de escopo" contradizia `cronista render`, efeitos renderizados e Shorts finalizados | Reescrever | Fora de escopo passa a ser "substituir o Resolve como editor"; o app pode codificar quando é só execução (seção 1) |
| 3 | Ambiguidade: um vídeo de 30–50 min ou episódios semanais? | Um vídeo só de 30–50 min, feito a partir de várias horas de gameplay em sessões de 3 h, 6 h, 10 h etc. | Produto = um vídeo por série; sessões de duração variável; um dia pode atravessar sessões; "episódio" trocado por "vídeo" (seções 0.1, 1, 2, 4.1, 5.4, 5.6, 6.5, Fases 7–9) |
| 4 | Nomes das skills diferentes na seção 5.5 | Corrigir | `/roteirizar` e `/humanizar`; perfil de voz é guia de estilo usado por elas |
| 5 | §11 deste histórico não marcado como substituído | Conferir | Nota de substituição parcial adicionada ao §11 |
| 6 | `.gitignore` ignoraria assets do brand kit, o `.env.example` e não separava config local | Corrigir | Exceção para `packages/brand-kit/`, `!.env.example`, `config/*.local.yaml` e `.claude/settings.local.json` ignorados; `dev.yaml`/`prod.yaml` versionados sem caminhos pessoais (seção 5.6) |

**Riscos técnicos corrigidos** (pedido: "corrija os riscos técnicos; se houver dúvida, me faça pergunta"):

| # | Risco | Resposta do criador | Decisão / impacto no plano |
|---|---|---|---|
| 1 | No OBS o filtro vale para a fonte, não para a faixa: RNNoise "só no mix" não funciona com uma fonte só | — | Microfone em duas fontes: com RNNoise → faixa 1; sem filtro → faixa 3 (seção 2) |
| 2 | FCPXML não carrega cor de marcador | — | Cor via EDL de marcadores do Resolve ou script interno; item do spike (seções 6.3, 6.5, Fase 6) |
| 3 | Não se sabe se o FCPXML mapeia faixa 2 → A1 e faixa 3 → A2 | — | Item do spike; alternativa com WAVs extraídos (seções 6.3, 6.5) |
| 4 | Script Python no OBS exige Python específico e talvez não exponha a função de marcador | Perguntou se não pode usar os marcadores do OBS; esclareceu que o marcador serve para indicar que algo aconteceu, não para definir capítulo | Os marcadores **são** os do OBS (o Hybrid MP4 os chama tecnicamente de "capítulo", mas não cria capítulo no vídeo). Termo trocado para "marcador do OBS". Quem cria o marcador com tipo e dia fica em aberto: A (obs-websocket, recomendada), B (Lua), C (hotkey nativa) (seção 4 e seção 9) |
| 5 | Hotkeys não chegam a jogos rodando como administrador ou com anti-cheat | — | Rodar como administrador ou usar dispositivo físico; verificar no PC de casa (seção 4) |
| 6 | Hybrid MP4 interrompido fica fragmentado | — | Remux sem recodificar na ingestão; item do spike (seções 2, 6.5, Fase 1) |
| 7 | 60 × 59,94 fps causa deriva nos cortes | 60 fps exatos | Gravação, timeline, timelapses e cartelas em 60 fps (seções 2, 6.3) |
| 8 | Navegador toca só a primeira faixa de áudio | — | Proxy H.264 + AAC com uma faixa e `faststart`; waveform a partir dos WAVs (Fase 1) |
| 9 | OCR ilegível no proxy 360p | — | OCR em frames do master (seção 5.2, Fase 3) |
| 10 | PaddleOCR e DeepFilterNet arriscados no Windows/Python 3.12 | RapidOCR + teste | ML em PyTorch + ONNX Runtime; OCR com RapidOCR; DeepFilterNet só se melhorar o WER no benchmark (seções 3, 5.2, Fases 1–3) |
| 11 | Processamento disputa a GPU com o jogo | Automático, com pausa | Começa ao fim da gravação e pausa com o OBS gravando ou jogo em tela cheia (seção 4.1) |
| 12 | CI só em Linux, produção em Windows | — | CI em Ubuntu e Windows (seção 5.6) |

> **Risco 4 resolvido pelo §20:** quem cria o marcador = opção A (obs-websocket), e o marcador não leva mais o dia.
>
> **Risco 10 complementado pelo §21:** o CTranslate2 do faster-whisper é exceção aceita à regra PyTorch + ONNX Runtime.

**Dias na tela:** o criador informou que a contagem de dias aparece na tela, mas que isso é decidido na hora da
edição. → `Início Dia N` passa a ser uma proposta de divisão; o número final é ajustado no Studio ou no Resolve;
cartelas e contador de dias saem editáveis (título Text+/Fusion ou regenerados pelo app), com item no spike
(seções 4, 6.3, 6.5). Contador de dias por projeto, persistido entre sessões; sem tecla de correção.

> **Parcialmente substituído pelo §20:** não há contador de dias na gravação; `Início Dia N` virou `Novo dia`, sem
> número. Continua valendo: a divisão é proposta, o número é da edição e as cartelas saem editáveis.

As demais perguntas e sugestões da revisão (Fase 1.5 com rough cut só de marcadores, divisão da Fase 1, contratos via OpenAPI,
gabarito com dois gêneros, critérios de aceite numéricos, backup na Fase 1, retenção × relink, política do PC do
trabalho, termos do `claude -p`, licenças do Remotion/modelos, macros do Fusion) foram apresentados como sugestões e
**ainda não foram decididos**. Desde o §21, estão listadas no item 7 das decisões em aberto do plano mestre (seção 9).

## 19. Segunda revisão: inconsistências restantes

**Pedido:** analisar o projeto e os documentos em busca de erros, dúvidas e melhorias pontuais (melhoria não é
obrigatória e não pode mudar o projeto todo). O criador aprovou a correção das inconsistências.

| # | Inconsistência | Decisão / impacto no plano |
|---|---|---|
| 1 | Mixagem citava "EBU R128 (−14 LUFS)", mas o alvo da EBU R128 é −23 LUFS; −14 LUFS é o alvo do YouTube | Texto corrigido: −14 LUFS integrado (alvo do YouTube), medido pelo método ITU-R BS.1770/EBU R128 (seção 6.4) |
| 2 | Benchmark "contra o gabarito" e WER na Fase 1 contradiziam "a Fase 1 não depende do gabarito" (WER exige transcrição de referência) | Fase 1 mede só desempenho (velocidade, VRAM); WER com/sem DeepFilterNet vira a primeira tarefa da Fase 2; precisão das tarefas do LLM local medida contra o gabarito (seções 3, 6.1, Fases 1 e 2, seção 9) |
| 3 | "Fallback com LLM local" para o roteiro contradizia a regra de LLM local só em tarefas curtas e fechadas | Fallback = `NullProvider`: sem roteiro escrito, só marcadores com contexto (Fase 5, seção 9) |
| 4 | Diagrama da seção 5.1 mostrava "Adaptador do Jogo" como etapa fixa, contra a decisão do §15 | Etapa renomeada para "Perfil Jogo (opc.)" |
| 5 | Faixa "20–35 h" não saía da conta 30:1–50:1 (que dá 15–42 h) | Tabela da seção 2 explica: 20–35 h na faixa central (~40:1), 15–42 h nos extremos. Meta de 25 h mantida |
| 6 | §12 deste histórico ainda dizia que o repositório remoto precisava ser criado | Nota de "resolvido" adicionada ao §12 |

**Dúvidas levantadas** (respondidas logo abaixo): onde ficam as skills `criar-plano`/`implementar-plano` (não estão no
repositório); como cumprir o aceite "ingerir 10 h" na Fase 1 sem gravação longa (fixture sintética?); se os marcadores
do OBS sobrevivem a uma gravação interrompida (item para o spike); onde ficam os WAVs extraídos (~0,7 GB/h por faixa)
e qual faixa vai no proxy.

**Respostas do criador às dúvidas:**

| # | Dúvida | Resposta do criador | Decisão / impacto no plano |
|---|---|---|---|
| 1 | Onde ficam as skills `criar-plano`/`implementar-plano`? | Não sabe responder | Não existem no PC do trabalho nem no repositório (provavelmente vieram de outra máquina). As referências foram retiradas: os planos de fase são escritos direto em `docs/fase-N-*.md`, sem depender de skill externa (`CLAUDE.md`, seção 0). Se aparecerem, podem ser versionadas em `.claude/skills/` |
| 2 | Como cumprir o aceite "ingerir 10 h" na Fase 1? | O critério está errado: qualquer hora de gameplay é válida | Aceite da Fase 1 sem mínimo de horas: ingerir sem intervenção uma gravação de qualquer duração (Fase 1, seção 9) |
| 3 | Os marcadores do OBS sobrevivem a uma gravação interrompida? | Não faz ideia | Item novo no checklist do spike: `ffprobe -show_chapters` antes e depois do remux; se não sobreviverem, o diário é a única fonte nesse caso (seção 6.5) |
| 4 | Onde ficam os WAVs extraídos e qual faixa vai no proxy? | Provavelmente ficam no vídeo | O áudio original fica sempre dentro do vídeo (master com as três faixas). Os WAVs são cópias de trabalho da análise: cache no SSD, regeneráveis do master; vão para o HD só se o spike exigir WAVs na timeline. O proxy toca o mix (faixa 1), só para ouvir (seção 2, Fase 1, seção 9) |

**Sugestões apresentadas, não decididas:** faixa 2 com "Captura de áudio de aplicativo" no OBS; importar o teste
também como `.otio` no spike; pausar o processamento pelo uso da GPU em vez de detectar tela cheia. Desde o §21,
estão no item 7 das decisões em aberto (seção 9 do plano mestre).

## 20. Quem cria o marcador e o número do dia

**Pergunta:** qual opção cria o marcador com tipo no OBS (A, programa ao lado do OBS via obs-websocket; B, script Lua;
C, só a hotkey nativa)? E a tecla de construção é uma só ou são duas?

**Resposta do criador:** opção A. Mas o programa não tem como saber o número do dia, porque esse número é o da
edição, e não o de quanto ele jogou. Sobre a construção: `▶/■` é só uma forma de escrever.

**Decisão:**
- Gravador de marcadores = **opção A** (seção 4, Fase 1, seção 9).
- **Sem contador de dias na gravação.** Substitui o "contador de dias por projeto, persistido entre sessões" do §18.
  A hotkey `Início Dia N` passa a se chamar `Novo dia` e grava só onde o dia começa, sem número. O nome do marcador
  passa de `tipo|dia|id` para `tipo|id`. O número de cada dia é definido na edição (Studio ou Resolve). Uma sessão que
  começa sem `Novo dia` continua o dia anterior (seções 2, 4, 5.4, Fase 1, seção 9 e `CLAUDE.md`).
- `Construção ▶/■` é uma tecla só, que alterna; o programa da opção A sabe se há uma construção aberta (seção 4).

## 21. Terceira revisão: inconsistências e dúvidas

**Pedido:** analisar o projeto e os documentos em busca de dúvidas ou erros aparentes. O criador aprovou a correção
das inconsistências.

| # | Inconsistência | Decisão / impacto no plano |
|---|---|---|
| 1 | O modelo de domínio (seção 5.4) ainda mostrava `Marcador (tipo, t, dia)`, contra o §20 | Marcador = `tipo, t, id`; o dia de cada trecho sai da posição dos `Novo dia` |
| 2 | A estrutura do repositório (seção 5.5) dizia "mecanismo em aberto" para o gravador de marcadores | Texto trocado para opção A via obs-websocket |
| 3 | O faster-whisper roda sobre o CTranslate2, que traz CUDA próprio, contra a regra "só PyTorch + ONNX Runtime" (§18, risco 10) | Exceção aceita e documentada; ⚠️ conferir na Fase 1 se as versões de cuBLAS/cuDNN convivem com as do PyTorch; se não, transcrição em processo separado (seções 5.2, 8 e 9) |
| 4 | A seção 6.4 põe efeitos renderizados "numa trilha acima do original", stems crus "abaixo" e overlays do Remotion, mas o layout da seção 6.3 só tinha V1–V3 / A1–A4 | Layout novo: V1 gameplay, V2 efeitos renderizados, V3 B-roll, V4 overlays, V5 cartelas (sempre por cima); A1 jogo, A2 voz ao vivo, A3 narração complementar, A4 música, A5 SFX, A6/A7 stems crus desativados (seções 6.3 e 9) |
| 5 | Itens do histórico substituídos por decisões posteriores sem nota (§3, §4, §6, §9, §14, §18) | Notas de substituição/atualização adicionadas |
| 6 | Sugestões não decididas dos §18 e §19 não apareciam na seção 9, que é onde a retomada procura o que está em aberto | Listadas no item 7 das decisões em aberto |

**Dúvidas levantadas, ainda sem resposta** (registradas no item 8 das decisões em aberto, seção 9):
- Primeira sessão do projeto sem `Novo dia`: abre o primeiro dia implicitamente?
- `Construção ▶` sem `■` é fechada no fim da sessão, mas um dia pode atravessar sessões: a construção também deveria?
- Fala ao vivo durante um farm que vira timelapse: descartar, cortar normal ou manter por cima?
- Critérios de aceite sem número nas Fases 2, 3 e 4.
- Fases 7 e 9 dependem de uma série inteira gravada e de um vídeo publicado.
- ⚠️ De memória: Voice Isolation (e talvez Dialogue Leveler) do Fairlight seriam exclusivos do Studio.
- Cópia do `README.txt` do Resolve em `docs/referencias/` num repositório público.

## 22. Quarta revisão: inconsistências e dúvidas

**Pedido:** analisar o projeto e os documentos em busca de dúvidas ou erros aparentes. O criador aprovou a correção
das inconsistências e o registro das dúvidas.

| # | Inconsistência | Decisão / impacto no plano |
|---|---|---|
| 1 | O remux da gravação interrompida usava `ffmpeg -c copy`; sem `-map 0` o FFmpeg copia só uma faixa de áudio e perde as faixas 2 e 3 | Comando passa a ser `ffmpeg -map 0 -c copy`; o spike confere as três faixas depois do remux (seções 2, 6.5, Fase 1) |
| 2 | A linha de base do áudio do jogo era "por contexto visual", mas o contexto só existe depois dos embeddings da Fase 3, e o áudio é a Fase 2 | Fase 2 calcula a linha de base por sessão; a Fase 3 acrescenta o recorte por contexto visual e recalcula só a novidade (seção 3, Fases 2 e 3) |
| 3 | No microfone, "só a fala conta" (o VAD descarta o resto), mas risada e grito eram sinais, e o VAD costuma tratá-los como não-fala | O classificador de eventos sonoros roda também no microfone, só para risada e grito; o VAD decide o que vai para a transcrição (seção 3, Fase 2) |
| 4 | "A falta do DeepFilterNet não bloqueia nada" só valia para a transcrição: a faixa 3 crua vira a trilha A2, e a cadeia de voz precisa de redução de ruído | A redução de ruído da mixagem não depende do benchmark de WER: DeepFilterNet, se instalar, ou filtros do FFmpeg (⚠️ de memória: `arnndn`, `afftdn`), escolhidos na Fase 6 (seções 5.2, 6.4, Fase 6) |
| 5 | O ducking pronto no stem de A1 só considerava a fala ao vivo; a narração complementar (A3) é gravada depois, e ali o jogo ficaria em volume cheio | O stem de A1 também é abaixado nos trechos em que o roteiro prevê narração; desfaz-se com o stem cru (A6). ⚠️ A confirmar com o criador (seção 6.4, Fase 6, seção 9 item 9) |
| 6 | −14 LUFS era aplicado aos stems, mas é alvo da mixagem final (com narração, música e SFX somados) | Stems nivelados entre si; o loudness integrado é medido e ajustado no render final, no Resolve ou no `cronista render` (seção 6.4, Fase 6) |
| 7 | O `.gitignore` ignora `*.mp4`/`*.mov`/`*.wav` em todo o repositório, o que pega os clipes do kit de teste do Resolve e as fixtures de vídeo de `tests/` | Clipes do kit e fixtures sintéticas são gerados por script em cada máquina; exceção no `.gitignore` para amostras reais pequenas em `services/engine/tests/fixtures/` (seção 9) |

**Lacunas menores corrigidas:**
- Checklist do PC de casa (seção 0): OBS 30.2+ (⚠️ de memória) e servidor obs-websocket ativado.
- Checklist do spike (seção 6.5): marcadores do OBS lidos pelo `ffprobe` numa gravação normal, overlay com canal alfa,
  clipes/trilhas desativados via FCPXML, importação do SRT e exportação em ProRes no Windows.
- Rota do intermediário (seção 6.5): ⚠️ de memória, o Resolve no Windows não exporta ProRes; padrão DNxHR até o spike.

**Dúvidas levantadas, ainda sem resposta** (registradas no item 9 das decisões em aberto, seção 9):
- Para que serve o mix com RNNoise, se a análise e a timeline não usam a faixa 1? Uma fonte única de microfone bastaria?
- Como o criador sabe que o toque foi registrado com o jogo em tela cheia (principalmente a tecla de construção, que
  alterna)? E se o programa de marcadores não estiver aberto?
- Marcador que existe só no arquivo e não no diário: qual é a regra da reconciliação?
- `Cinemática` e `Foto de progresso`: a tomada é antes ou depois do toque?
- Ducking sob a narração complementar: pré-aplicado pelo app (padrão atual) ou deixado para o Fairlight?
- Métricas de ritmo dos criadores de referência: origem dos arquivos de vídeo e fase em que entram.
- Itens sem fase definida: `cronista render`, mídia intermediária DNxHR, métricas de ritmo, `StorageBackend` e
  política de retenção.

## 23. Quarta revisão: pontos menores

**Pedido:** "algo mais para ser corrigido?". Foram apresentados seis pontos menores; o criador aprovou a correção.

| # | Inconsistência | Decisão / impacto no plano |
|---|---|---|
| 1 | A opção 2 das cartelas (PNG/MOV regenerado "depois do ajuste dos dias no Studio") não funciona na Fase 6, porque o Studio só chega na Fase 7 | Na Fase 6 vale o título editável (opção 1); se o spike reprovar, os números vêm de um arquivo de dias do projeto, editado à mão (seções 6.3 e 9) |
| 2 | A seção 5.5 listava "ADRs" em `docs/`, mas as decisões vão para este histórico e ADR não aparece em mais nenhum lugar | Texto trocado para "este plano + histórico de decisões + planos por fase" |
| 3 | A árvore da seção 5.5 começava em `cronista/`, e o repositório se chama `Editor_De_Video` | Raiz corrigida; `cronista` é o nome do pacote Python |

**Dúvidas levantadas, ainda sem resposta** (acrescentadas ao item 9 das decisões em aberto, seção 9):
- Direção dos contratos: JSON Schema → Pydantic (seção 5.2) ou Pydantic → JSON Schema (exemplo da 6.1)? Decidir junto
  com a sugestão de OpenAPI.
- Marcador por áudio da FIFINE: o som do pad na faixa do microfone iria para a trilha A2 do vídeo final.
- Ferramenta de anotação do gabarito na Fase 1: o que é, se o Studio só chega na Fase 7?

## 24. Quinta revisão: inconsistências e dúvidas

**Pedido:** analisar o projeto e os documentos em busca de dúvidas ou erros aparentes. O criador aprovou a correção
das inconsistências e o registro das dúvidas.

| # | Inconsistência | Decisão / impacto no plano |
|---|---|---|
| 1 | Os WAVs iriam para o HD "só se o spike exigir", mas os stems processados de A1/A2 (Fase 6) não cabem no MP4 e são sempre WAVs | Stems processados sempre em WAV, no HD (`exports`); o teste de faixas embutidas do spike vale só para as faixas cruas (seções 2, 6.3 e 9) |
| 2 | "Trilhas sem conteúdo numa fase não são criadas" contradizia A3 e A4 "vazias" e deslocaria a numeração | Numeração fixa: trilhas sem conteúdo são criadas vazias; só A6/A7 são condicionais. ⚠️ FCPXML usa "lanes": item novo no spike (seções 6.3 e 6.5) |
| 3 | "O perfil é aprendido, não escrito à mão" contradizia o lookback "ajustável no perfil" e as regiões de HUD "definidas no perfil" | Pesos aprendidos + campos manuais opcionais (HUD, lookback, rótulos ignorados) (seção 3) |
| 4 | Cartelas: título editável na Fase 6 (seção 6.3) × "cartelas de dia" como template Remotion (seção 6.4, Fase 8); a lista da Fase 6 não citava cartelas nem B-roll | Cartelas Remotion = opção 2 (regeneradas pelo app, sem número fixo); título editável continua; Fase 6 passa a citar cartelas e B-roll (seções 6.3, Fases 6 e 8) |
| 5 | "Dois caminhos independentes" para o marcador, mas na opção A o mesmo programa faz os dois | Texto trocado para "dois registros separados"; a redundância não cobre a falha do programa (seção 4) |
| 6 | A exceção `!services/engine/tests/fixtures/**` do `.gitignore` versionaria fixtures sintéticas geradas ali, contra o §22 | Fixtures geradas vão para `data/fixtures/`; a pasta de `tests/` guarda só amostras reais pequenas (seções 5.6 e 9, `.gitignore`) |
| 7 | Pontos de texto: "nessa mesma gravação interrompida" depois do item da gravação normal; "avisa (ou converte)" × "converte" para 10-bit; "o app não chama o Claude" × `ClaudeCodeProvider`; §5 sem nota de atualização; beats da seção 5.4 × arco da Fase 5; intermediário DNxHR SQ "dezenas de GB" | Checklist reescrito; 10-bit = avisa e converte; "nunca chama a API do Claude"; nota no §5; Fase 5 usa os beats da 5.4; intermediário ~65–110 GB (⚠️ de memória) (seções 1, 2, 6.5, Fase 5) |

**Conferido:** o Humanizer lista mesmo 26 padrões (README do repositório, 2026-11-12).

**Itens novos no checklist do spike (seção 6.5):** trilhas em que o Resolve põe os clipes do FCPXML e criação de
trilhas vazias; FCPXML de teste gerado pelo caminho OTIO → FCPXML; script interno sem janela própria.

**Dúvidas levantadas, ainda sem resposta** (registradas no item 10 das decisões em aberto, seção 9):
- O adaptador FCPXML do OTIO dá conta, ou o app escreve o FCPXML direto?
- O FCPXML garante o layout de trilhas e cria trilhas vazias?
- O script interno funciona no gratuito recente sem interface gráfica?
- Timelapse de farm fica mudo na Fase 6, até a música chegar na Fase 8?
- Shorts 9:16 a partir de 1080p: recorte de 608 px ampliado ~1,8×.
- Quem dispara o processamento automático, e em que linguagem é o gravador de marcadores?
- Stems processados: sessão inteira ou só os trechos usados?

## 25. Como começar: divisão da Fase 1

**Pergunta do criador:** o que podemos fazer para começar a desenvolver o projeto?

**Resposta do Claude:** o projeto só tem planejamento; o próximo passo é detalhar a Fase 1. Como ela está grande
demais (sugestão do §18, item 7), propôs dividi-la em 1A (esqueleto e ingestão, roda no PC do trabalho), 1B (marcadores
e prévia) e 1C (itens do PC de casa: kit do Resolve, FIFINE, guia do OBS, benchmark).

**Decisão:** o criador aprovou a divisão ("Sim, dividir"). Criado [fase-1-fundacao.md](fase-1-fundacao.md) com tarefas,
critérios de aceite e testes por sub-etapa. O aceite da Fase 1 equivale a 1A + 1B; a 1C bloqueia a Fase 2 e o spike do
Resolve antes da Fase 6. Plano mestre atualizado (Fase 1 e seção 9).

**Propostas ainda não confirmadas** (D1–D4 no plano da fase, listadas no item 7 da seção 9): gravador de marcadores em
Python e disparo do processamento pelo engine; contratos Pydantic → JSON Schema/OpenAPI → TypeScript (inverte o texto
da seção 5.2); gabarito em CSV; sem Fase 1.5. Também propostos, a confirmar: marcador que só existe no arquivo vira
`Momento` com aviso; primeira sessão sem `Novo dia` abre um dia implícito.

## 26. Confirmação das propostas D1–D4

**Resposta do criador:** "Confirmo todas" (as propostas D1–D4 do §25, mais os dois pontos de reconciliação).

**Decisão:**
- **D1:** gravador de marcadores em Python; o engine dispara o processamento ao observar `recording_stopped`.
- **D2:** contratos Pydantic → JSON Schema/OpenAPI → TypeScript. **Substitui** "JSON Schema → Pydantic" da seção 5.2.
- **D3:** gabarito em CSV com script de validação.
- **D4:** sem Fase 1.5; a prévia MP4 da 1B cumpre o papel.
- Marcador só no arquivo = `Momento` com aviso; primeira sessão sem `Novo dia` abre um dia implícito.
- Itens dos §21–§24 respondidos por isso: dia implícito, marcador só no arquivo, direção dos contratos, ferramenta do
  gabarito, disparo do processamento e linguagem do gravador.

---

## Decisões em aberto

A lista atual fica na seção 9 do [plano mestre](00-plano-mestre.md).
