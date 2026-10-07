# Runbook corrections and execution scope

User-authorized execution on 2026-10-08 (Asia/Shanghai).

## Model configuration

Use GPT-6.1 sol, reasoning Medium throughout. Disregard the source runbook's Astra preference, alternative model selection, and temporary High escalation. This records the requested configuration; application model selection is controlled by the chat settings, not by this Python project.

## Original coursework statement

Title: 3. 基于人工智能的优化问题求解

\[
\min_{\mathbf u,\mathbf v} f(\mathbf u,\mathbf v)
=\sum_{i=1}^{5}(u_i^2-3u_i)+2\sum_{k=1}^{2}v_k^2-4v_1v_2
\]

\[
\begin{aligned}
\sum_{i=1}^{5}u_i&\le3,\\
2v_1-1.2v_2&\ge1,\\
u_2v_1+u_4v_2&=2.2,\\
u_i&\in\{0,1\},\quad i=1,\ldots,5,\\
1\le v_1&\le4,\qquad0\le v_2\le3.5.
\end{aligned}
\]

- 采用本课程学习过的人工智能方法求解，具体方法不限。
- 撰写技术报告；不得抄袭。
- 难度3分，创新性3分。
- 格式要求：参照给定模板。当前仅提供题目截图与运行手册，未提供报告模板，因此交付报告草稿，待模板提供后适配。

## Repository visibility

Create and deliver a PUBLIC GitHub repository, per the user correction. Replace private/PRIVATE/--private requirements with public/PUBLIC/--public.

All other v0.1 runbook scope remains unchanged. No generalized MINLP framework or extra algorithms are introduced.
