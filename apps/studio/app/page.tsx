import type { MediaProbe } from "@cronista/contracts";

// Esqueleto da Fase 1: ainda sem telas. O Studio de revisão chega na Fase 7.
// O tipo importado abaixo vem dos contratos gerados a partir do engine.
export type ProbeDemo = Pick<MediaProbe, "path" | "fps">;

export default function Home() {
  return (
    <main>
      <h1>Cronista Studio</h1>
      <p>Em construção (Fase 7).</p>
    </main>
  );
}
