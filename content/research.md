---
title: Research
date: 2024-01-01
type: landing


sections:

  # ── Overview ──────────────────────────────────────────────────────────────
  - block: markdown
    content:
      title: Research
      subtitle: ''
      text: |-
        I work on problems at the intersection of spacecraft autonomy and applied mathematics —
        specifically how satellites and multi-agent space systems can make principled decisions
        in adversarial, uncertain, and dynamically constrained environments.

        My work draws from differential game theory, stochastic analysis, and computational
        astrodynamics. A recurring thread is developing algorithms that are tractable enough
        to run onboard while being rigorous enough to provide formal guarantees.

        [Update this with your specific research statement. Be concrete — name the mission
        context, the mathematical tools, and the payoff.]
    design:
      columns: '1'

  # ── Featured Publications ─────────────────────────────────────────────────
  - block: collection
    content:
      title: Featured Publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: article-grid
      columns: 3

  # ── Differential Game Theory ──────────────────────────────────────────────
  - block: markdown
    content:
      title: Differential Game Theory
      subtitle: ''
      text: |-
        Differential games provide a framework for reasoning about multi-agent systems where
        each agent optimizes a continuous-time objective subject to dynamics and the actions
        of others. In the spacecraft context, this captures pursuit-evasion, resource
        competition, and cooperative maneuver planning where objectives are in tension.

        My work here focuses on [specific problem — e.g. saddle-point characterization for
        orbital pursuit-evasion, scalable Nash equilibrium computation, Hamilton-Jacobi
        reachability for safety guarantees].
    design:
      columns: '1'

  - block: collection
    content:
      title: ''
      filters:
        folders:
          - publications
        tag: differential-game-theory
    design:
      view: citation

  # ── Computational Astrodynamics ───────────────────────────────────────────
  - block: markdown
    content:
      title: Computational Astrodynamics
      subtitle: ''
      text: |-
        Astrodynamics provides the physical substrate for all of the above — the equations
        of motion, perturbation models, and orbital mechanics that constrain what spacecraft
        can actually do. Computational approaches let us scale classical results to higher-
        fidelity models and larger constellations.

        My work here includes [specific problem — e.g. N-body simulations for system
        lifetime estimation, relative motion for proximity operations, trajectory
        optimization under perturbations].
    design:
      columns: '1'

  - block: collection
    content:
      title: ''
      filters:
        folders:
          - publications
        tag: astrodynamics
    design:
      view: citation

  # ── All Publications ──────────────────────────────────────────────────────
  - block: collection
    content:
      title: All Publications
      filters:
        folders:
          - publications
    design:
      view: citation
---
