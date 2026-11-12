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

---

## Decisões em aberto

1. Jogo da calibração inicial (sugestão: Minecraft).
2. Há voz de amigos/Discord nas gravações?
3. Nome definitivo do projeto ("Cronista" é provisório).
4. Verificar na prática o que o Resolve gratuito aceita (seção 6.5 do plano).
