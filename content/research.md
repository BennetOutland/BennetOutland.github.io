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
        My research is in nonlinear dynamical systems and the control of agents within such systems.
        The problems I find most compelling sit at the boundary of what is mathematically tractable
        and what is physically meaningful — trajectory optimization under chaotic dynamics, autonomous
        proximity operations where interacting boundary layers or gravitational flows make classical
        methods fragile, and multi-agent systems that must act safely under uncertainty.

        Concretely, this means work in stochastic trajectory optimization, differential game theory
        for spacecraft pursuit-evasion and cooperative maneuvering, nonlinear system identification,
        and computational astrodynamics. Application domains include cislunar space operations,
        very low Earth orbit (VLEO) satellite maintenance, and — from earlier work — the long-term
        stability of compact planetary systems.
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
        Differential games formalize multi-agent problems where each agent optimizes a
        continuous-time objective subject to shared dynamics and the decisions of others.
        In the spacecraft context this captures pursuit-evasion scenarios, contested
        proximity operations, and cooperative rendezvous where the objectives of different
        agents are in tension.

        My PhD work develops theory and algorithms for these settings — focusing on
        tractable solution methods that scale to the dynamics and constraints encountered
        in cislunar and low-Earth-orbit environments.
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
        My astrodynamics work spans two threads. During my time at AFRL, I focused on
        cislunar rendezvous — developing efficient trajectory generation methods for
        autonomous deputy-chief spacecraft operations, and building spacecraft modeling
        and control libraries in Julia. Earlier, at NASA Ames, I investigated the
        long-term stability of compact planetary systems using high-throughput N-body
        simulations, which led to three forthcoming journal publications.
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
