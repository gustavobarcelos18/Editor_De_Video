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

## 4. Marcadores: início e fim, ou um toque só?

**Pergunta:** é preciso marcar o início e o final do acontecimento, ou só marcar para deixar claro que há algo ali?

**Decisão:** um toque basta. O sistema olha 60–90 s para trás e encontra os limites reais. Início e fim só para
construções (viram timelapse). Hotkeys opcionais por tipo e uma de "Início Dia N". → Seção 4.

## 5. Quantas horas gravar

**Pergunta:** quantas horas de gravação são necessárias para ter com certeza 30–50 min de produto final?

**Decisão:** mirar 25 h (faixa de 20–35 h), pela compressão típica de 30:1 a 50:1. No Minecraft, 100 dias ≈ 33 h
reais (17–25 h pulando noites). A Fase 4 mede a taxa real. → Seção 2.

## 6. Primeira versão do plano

**Decisão:** 7 fases (fundação, áudio, vídeo, relevância, narrativa, montagem, Studio). Usar o plano Pro via
Claude Code, porque o Pro não inclui API. Skill de humanização em português, calibrada pelas narrações
transcritas do criador. NestJS e C# ficaram de fora por enquanto, para evitar ponte entre linguagens. → Seção 7.

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

## 12. Documentação e repositório

**Pedido:** estruturar tudo em documento para retomar no PC de casa; depois, colocar no repositório e subir no GitHub;
por fim, atualizar os documentos sem retirar nenhuma informação conversada.

**Decisão:** o repositório git é a fonte de verdade (`docs/00-plano-mestre.md` + este histórico). O GitHub CLI não
estava instalado no PC do trabalho, então o repositório remoto precisa ser criado manualmente (ver README).
Um documento no claude.ai chegou a ser iniciado e ficou incompleto (4 de 8 seções); o repositório o substitui.

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

---

## Decisões em aberto

A lista atual fica na seção 9 do [plano mestre](00-plano-mestre.md).
