<a href="https://www.0xnavarro.com/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img alt="Carlos Navarro. Founder, builder, CEO. Building technology companies in complex markets. I build the companies and write the software behind them. CEO and co-founder of Vitalink; CEO and founder of Brida." src="assets/hero-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://www.0xnavarro.com/"><b>0xnavarro.com</b></a> &nbsp;·&nbsp;
  <a href="https://www.0xnavarro.com/en/writing/">Writing</a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/0xnavarro/">LinkedIn</a> &nbsp;·&nbsp;
  <a href="mailto:info@0xnavarro.com">info@0xnavarro.com</a>
</p>

<br>

I founded my first company at 21, ran hospital IT in Mexico, and now lead two technology companies in markets where complexity is the barrier: healthcare, and the way companies run. I design the systems and write the code. This page is the technical side of that work; the rest is on [0xnavarro.com](https://www.0xnavarro.com/).

## Building now

### <img src="assets/logos/vitalink-icon.svg" width="24" height="24" alt=""> Vitalink · the action layer for healthcare

**Co-founder & CEO, since 2025.** Vitalink gives every person an agent that works for their health, and gives doctors the tools that agent works with. We start in Mexico.

| Product | What it does |
|:--|:--|
| [**Health agent**](https://www.vitalink.chat/) | Finds surgeons, requests and compares quotes at the full price, and books the assessment, over WhatsApp or the web. Free for patients. |
| [**Expediente Vitalink**](https://expediente.vitalink.lat/) | Electronic health record for doctors and clinics: patients, visits, prescriptions, schedule and follow-up. Free to start. |
| [**Vitalink Pay**](https://pay.vitalink.chat/) | A payment link for credentialed doctors. The patient pays in cash or in 3 to 24 monthly instalments; the doctor is paid the same either way. |

### <img src="assets/logos/brida-tile.svg" width="24" height="24" alt=""> Brida · build your company by talking

**Founder & CEO, since 2026.** Brida is the all-in-one infrastructure for a company that runs itself. You ask for what the company needs, whether portals, agents, processes, dashboards or websites, and Brida builds it on the company's own data and puts it to work. It runs from Brida or from Claude, ChatGPT, Cursor and any MCP client. Its first job is sales.

[**brida.ai →**](https://www.brida.ai/) &nbsp;·&nbsp; #12 of the top 100 AI startups in Estonia ([F6S](https://www.f6s.com/companies/artificial-intelligence/estonia/co), Nov 2026)

## How I build

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/method-dark.svg">
  <img alt="How I build: Spec (written requirement), Plan (reviewed before code), Build (agents in worktrees), Gate (tests, CI, review), Ship (deploy and observe)." src="assets/method-light.svg" width="100%">
</picture>

- **Specs before code.** Every change starts as an issue and a written requirement. Agents implement it in isolated worktrees, one reviewable pull request at a time.
- **Gates decide what ships.** Tests, CI and review, automated and human, decide what merges.
- **Publish the receipts.** Benchmarks ship their corpora, failures and limits, not just a headline number.
- **People own the decisions.** Agents do the work. Anything that spends money, reaches a customer or changes scope comes back to a person.

The method is public: the essay [Founder-Led Engineering Ops](https://www.0xnavarro.com/en/writing/founder-led-engineering-ops/), the template [AI Software Bootstrap](https://github.com/0xnavarro/ai-software-bootstrap) and the scaffolder [create-qa-ops](https://github.com/0xnavarro/qa-ops).

## Open work

Most of what I build lives in private company repositories. This is the public part.

**Evaluation research, at Brida**

- [**ReflexBench**](https://github.com/brida-ai/reflexbench) · `v1.0.0 stable`. An open benchmark and harness for typed decision models, with frozen corpora, calibration metrics, paired bootstrap intervals and a public failure ledger.
- [**AlignmentBench**](https://github.com/brida-ai/alignmentbench) · `v0.1 preview`. Tests whether an AI system stays inside explicit authority, scope and oversight rules at the moment it chooses an action.

**Engineering method**

- [**AI Software Bootstrap**](https://github.com/0xnavarro/ai-software-bootstrap). How I run agent-assisted engineering, as a template: issues, specs, plans, worktrees, CI gates and review.
- [**create-qa-ops**](https://github.com/0xnavarro/qa-ops) · `npm`. `npx create-qa-ops` scaffolds findings, audits, QA sessions and merge gates that agents can read and run.

**Earlier applied AI**

- [**ADSA**](https://github.com/AteneaLabs/adsa) · `2024`. Autonomous data-science agents: o1 writes the ML code, Claude 3.5 Sonnet debugs it, a coordinator runs the loop. Placed 71st of 2,461 active participants on Kaggle's Spaceship Titanic.
- [**Speech to Text**](https://github.com/0xnavarro/speech-to-text). Real-time, multilingual speech-to-text in the browser.
- [**IA-PARA-TODOS**](https://github.com/0xnavarro/IA-PARA-TODOS). An open collection of AI apps and tutorials in Spanish (archived).

## Path

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/path-dark.svg">
  <img alt="My path, newest first. 2026 to now: Brida, founder and CEO, build your company by talking. 2025 to now: Vitalink, co-founder and CEO, the action layer for healthcare: health agent, Expediente EHR, Vitalink Pay. 2024: ADSA, autonomous data-science agents on o1 and Claude 3.5 Sonnet, 71st of 2,461 on Kaggle. 2023: founded Atenea Labs, my applied-AI lab. 2022: Head of IT Systems at a hospital in Mexico, the start of four years in healthcare; before that, moved to Switzerland and started working in tech. 2021: founded Rigfarm, my first company, at 21 in Madrid. 2018: regional under-18 chess champion, Castilla-La Mancha." src="assets/path-light.svg" width="100%">
</picture>

## Writing

- [What a Startup CEO Does](https://www.0xnavarro.com/en/writing/what-a-startup-ceo-does/): making the company worth more, and why Vitalink starts small to go global.
- [Founder-Led Engineering Ops](https://www.0xnavarro.com/en/writing/founder-led-engineering-ops/): a spec-driven, agent-orchestrated way to build software with human governance.
- [You Cannot Just Say an AI Is Aligned. You Have to Measure It.](https://www.0xnavarro.com/en/writing/you-cannot-just-say-an-ai-is-aligned-you-have-to-measure-it/): the thinking behind AlignmentBench.
- [The Miniaturization of the Firm](https://www.0xnavarro.com/en/writing/the-miniaturization-of-the-firm/): AI doesn't eliminate the company. It compresses it.

## Build log

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/build-log-dark.svg">
  <img alt="My GitHub contributions over the last year, most of them in private company repositories. Updated daily." src="assets/build-log-light.svg" width="100%">
</picture>

<br>
<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/signoff-dark.svg">
    <img alt="Agents do the work. People own the decisions." src="assets/signoff-light.svg" width="70%">
  </picture>
</p>
