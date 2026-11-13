# Cronista

App pessoal que transforma dezenas de horas de gameplay gravada no OBS em uma **timeline pré-montada no
DaVinci Resolve** + **roteiro de narração**, para vídeos de "100 dias".

Status: planejamento concluído em linhas gerais. Nenhum código ainda. Fase 1 detalhada e dividida em 1A/1B/1C;
decisões D1–D4 confirmadas; próxima etapa: começar a 1A.

## Documentos

| Documento | Conteúdo |
|---|---|
| [docs/00-plano-mestre.md](docs/00-plano-mestre.md) | Fonte de verdade: requisitos, arquitetura, stack, produção, fases, riscos |
| [docs/fase-1-fundacao.md](docs/fase-1-fundacao.md) | Plano de execução da Fase 1 (1A, 1B, 1C) |
| [docs/01-historico-de-decisoes.md](docs/01-historico-de-decisoes.md) | Cada pergunta do planejamento e a decisão tomada |

## Retomar em outro PC ou numa nova sessão

Clone o repositório e abra o Claude Code na pasta: o `CLAUDE.md` carrega o contexto sozinho. Para a retomada guiada, use o prompt da seção 0 do plano mestre.

## Repositório

```
git clone https://github.com/gustavobarcelos18/Editor_De_Video.git
```

Fluxo: branch por fase (`fase/N-nome`), pull request para a `main` ao fim de cada fase, revisão com Opus e CI no
GitHub Actions (detalhes na seção 5.6 do plano mestre).
