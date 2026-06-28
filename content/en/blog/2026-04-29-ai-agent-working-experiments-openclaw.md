---
title: AI News Daily 04-29
slug: ai-agent-working-experiments-openclaw
description: ''
date: 2026-04-29 22:39:01 +0800
draft: false
comments: true
tags:
- AI Agent
- OpenClaw
- GitHub
- 开源维护
- 自动化
- 效率工具
- 独立开发
linkTitle: 04-29 AI News
---
# OpenClaw's fizzled out, so here are two cool AI experiments I ran where AI actually did the heavy lifting for me 🤖

The AI scene is just moving at warp speed lately, and sometimes I wonder if I've already fallen a cycle behind. But then **OpenClaw** dropped a couple of months ago, and my curiosity just totally piqued.

After messing around at home for about a week, I cooked up two pretty cool little experiments. Both revolved around the same age-old question: **Can AI genuinely do the work for me?**

I'm not talking about those "emotional support AIs" that just chat with you or whip up a few pretty sentences. I'm talking about **digital temp workers** that can deploy on schedule, follow processes, and even give reliable feedback when things go sideways.

So, here are the experiments that have been running stably for two months. Today, I'm gonna spill the beans with you all.

## First up, the experiment subject: A project with a silly name but serious chops

Before we dive into OpenClaw, let's get the "experiment subject" out of the way first:

**[justlovemaki/git-commit-sao-hua](https://github.com/justlovemaki/git-commit-sao-hua)**

Its name, as you can see, is the **Git Commit Sass Generator**. This idea was something my AI and I brainstormed together. I figured it would just be a small program for developers to have a bit of fun, generating sweet talk, sassy remarks, or even chuunibyou lines to make their commits a bit less dry.

Initially, the project was super lightweight, just a static HTML page. But as I kept working on it, things started to get weird; it gradually sprinted towards becoming a full-blown engineering project. Later, it even got **AST (Abstract Syntax Tree) analysis** to determine commit types based on code changes. After that, it even connected to an **MCP Server**.

Clearly, this wasn't just "a playful gimmick tool" anymore.

What I mean is, AI Agents like Claude and Cursor can directly call its API to generate commit messages. Even though it's called the "Sass Generator," at its core, it has evolved into a full-featured multi-platform program, an AI-native CLI.

So, while its name is definitely irreverent, and you might think it's just a casual project, it's actually ridiculously feature-rich.

## Experiment One: Getting AI to maintain the project twice a day, all by itself

Since AI is already so powerful, could I use **OpenClaw** to set up a scheduled task and have AI maintain the project itself every single day?

The answer, of course, is a resounding yes!

I had OpenClaw write a Skill and set it to run twice a day. The core logic isn't too complicated; it essentially does this:

1.  **When it's time, read issues** to gather human bug reports and update instructions.
2.  **Check for recent dependency updates** or any areas that could be conveniently optimized.
3.  **Automatically modify and test**.
4.  **Finally, push the changes**.

The first time I saw OpenClaw actually push code, only one thought popped into my head: **"My mischievous kid, who usually just causes trouble, suddenly learned to wash his own socks!"** 😂

To be honest, in that moment, I felt pretty darn good. You could clearly feel that AI wasn't just a "writing assistant" anymore; it was starting to resemble a genuine collaborator capable of taking over repetitive tasks. Even if it's not tackling super advanced stuff right now, it's already gobbling up the most fragmented and annoying maintenance work.

## Experiment Two: Issue Support that's even more polite than me 🤯

The second experiment was even more practical and closer to my usual work scenarios.

What do independent developers fear most? It's not writing code; often, it's **issue explosions**!

When you're swamped, you can't always check them, but not replying feels rude. Especially when someone seriously asks a question, you know you *should* reply, but with a pile of other things to do, it's easy to keep procrastinating. And then there are those really contentious questions that just get on your nerves, making you want to retort.

So, I had OpenClaw write a second Skill: **Read the repo's issues every hour and help me reply and process them.**

This Skill was a bit more complex because it wasn't just "glance and send a templated reply"; it had to first determine the issue type:

-   If it's a **query-based question**, it would combine the README and codebase content to provide a reply.
-   If it's a **bug**, it would try to understand the problem, and if necessary, offer reproduction steps and modification suggestions.

The actual effect was much better than I expected. Just a couple of weeks ago, some dude raised a pretty obscure question. I hadn't even had time to open it yet when OpenClaw had already organized the steps and replied. In the end, the person actually replied with:

> “Thanks, this solved my problem!”

I stared at that reply for a long time, and only one thought ran through my head: **This AI is way more courteous than I am!**

If it had been me, it probably would've been a simple `fixed` or `check README` — as concise as possible, just aiming for "read and replied." But this digital colleague not only replied but did it quite properly: politely, thoroughly, with a stable tone, looking like someone genuinely invested in customer service.

The most meaningful part of this is: **It didn't replace the creative work I truly wanted to do. It simply took away the necessary but very mechanical tasks.** I no longer have to waste energy on things like "Did I check the issue?", "Did I reply?", or "Is this sentence polite enough?". It handles that layer for me, freeing up my time for other things.

## My two cents after all that tinkering 🤔

After these two Skills got up and running, I was sitting on my balcony one night, staring into space, and one question kept swirling in my head: **What's really left of the barrier to independent development these days?**

It used to be about who could write code faster, who had a more stable approach, or who could build complex processes piece by piece themselves. Now, with tools like OpenClaw emerging, the gap between "I have an idea" and "this idea can actually run" has significantly narrowed.

I don't need to write a bunch of GitHub Actions, stitch together Cron jobs myself, or scour the internet for scripts to piece together processes. A lot of the time, I just need to articulate the requirements clearly:

-   *Hey, go check for issues for me every hour.*
-   *If there's an issue, reply to it, and be a bit polite.*

The rest? It just takes over.

Of course, AI is still a long way from "fully autonomous development." It occasionally still comes up with some bizarre sass or gives you that "it seems to understand, but only half" kind of vibe. But even just in an auxiliary role, it's already good enough to be incredibly useful.

For me, at least, this feeling is pretty novel: **I'm not just "using a tool"; I'm slowly training a digital buddy who can actually take on tasks.**

And this whole process, in itself, is pretty damn interesting. At the end of the day, isn't that why us tinkerers love doing what we do?

---

**Final thoughts:**

If you're also interested in this project—which seems outwardly playful but is actually a hardcore engineering boilerplate—you can go check it out:
**Project Link**：[justlovemaki/git-commit-sao-hua](https://github.com/justlovemaki/git-commit-sao-hua)
While you're at it, maybe hit that Star button for the author? I don't think that's asking too much. 😉

As for OpenClaw, I've actually given up tinkering with it and have switched to **Hermes** to continue helping me with tasks.

A lot of people say OpenClaw isn't useful, but that's really just because they haven't found the right application scenarios for it. For simple, repetitive tasks like these, handing them over to AI can totally free up our hands.

As for other things, if you want AI to help you make money, you first need to know *how* to make money yourself, instead of expecting AI to figure it out for you. **AI is just your employee; *you* are the boss.**

That's all for now! If I stumble upon any more outrageous but genuinely useful Agent plays later on, I'll be sure to come back and share them with you all.