# Cronista

App pessoal que transforma horas de gameplay gravada no OBS em uma timeline pré-montada no DaVinci Resolve
gratuito + roteiro de narração, para vídeos de "100 dias". Usuário único (o criador), mas estruturado para escalar.

## Fonte de verdade

- `docs/00-plano-mestre.md`: requisitos, arquitetura, stack, fases, riscos e decisões. Leia antes de propor ou
  implementar qualquer coisa. Se uma ideia contradiz o plano, aponte a contradição em vez de seguir em silêncio.
- `docs/01-historico-de-decisoes.md`: cada pergunta do planejamento e a decisão tomada.
- `docs/fase-N-*.md`: plano de execução de cada fase (criado com a skill `criar-plano`, executado com `implementar-plano`).
- Toda decisão nova vai para o plano mestre (seção relevante + seção 9) **e** para o histórico. Nunca apague
  informação já conversada; atualize ou marque como substituída.

## Regras de produto que não se negociam

- **Universal:** o núcleo é agnóstico de jogo e funciona sem nenhuma configuração por jogo. Nada de `if jogo == ...`
  no núcleo. Refinamentos por jogo só em perfis declarativos (YAML) aprendidos com o feedback; leitores de mods são opcionais.
- **"Dia" é fictício:** unidade de progresso da série, definida pela hotkey `Início Dia N`, não pelo relógio do jogo.
- **Fala ao vivo tem prioridade:** o roteiro só complementa (explica decisões, o porquê, o que vem a seguir) nos
  espaços sem fala ao vivo. Sem voz sintética. Texto sem "cara de IA" (skill `/humanizar`, adaptada do Humanizer, MIT; ver seção 6 do plano).
- **Custo zero:** tudo local (RTX 3060 12 GB). Claude só via Claude Code no plano Pro (sem API); entradas compactas.
- **LLM local só para tarefas curtas e fechadas**, com saída em JSON Schema validada por Pydantic.
- **Caminho de mão única** app → Resolve; efeitos sempre reversíveis (trilha acima do original).
- Gravação: OBS em Hybrid MP4, H.264 8-bit SDR (NV12, Rec. 709), faixa 1 = mix, 2 = jogo, 3 = microfone.
  Nunca analisar o mix. Sem facecam.
- **Resolve gratuito:** nunca gerar nada que dependa de recurso do Studio (Speed Warp, Magic Mask, Super Scale,
  redução de ruído de vídeo etc.), porque deixa marca d'água. Limites e estratégia de render na seção 6.5 do plano.

## Ambientes

- `dev` = PC do trabalho, **sem GPU**: tudo precisa rodar em CPU, com mocks e fixtures sintéticas geradas por FFmpeg.
- `prod` = PC de casa (RTX 3060, OBS, Resolve, mídia real).
- Testes que exigem GPU ou mídia real: `@pytest.mark.gpu` / `@pytest.mark.media` (rodam só em `prod`).
- Caminhos de mídia nunca fixos no código; configuração em `config/dev.yaml` / `config/prod.yaml`.
- Mídia, cache e banco ficam em `data/` (fora do git).

## Stack

Engine em Python 3.12 + uv (FastAPI, SQLite com SQLAlchemy + Alembic, FFmpeg, OTIO). Studio em Next.js + TypeScript
com pnpm. Contratos em JSON Schema → Pydantic e TypeScript gerados. Estrutura do monorepo na seção 5.5 do plano.

## Fluxo git

- Branch por fase (`fase/N-nome`), PR para a `main` ao fim da fase, revisão com `/code-review` antes do merge.
- Commits no nome do criador (identidade git já configurada), padrão Conventional Commits, mensagens em pt-BR.
- CI no GitHub Actions: ruff, mypy, pytest (CPU), eslint, tsc.

## Comunicação

- Responda e escreva documentação em português do Brasil.
- Quando algo for de memória e não verificado (versões, APIs do OBS/Resolve), diga isso e marque para verificação.
