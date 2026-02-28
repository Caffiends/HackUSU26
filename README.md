# Shame
Welcome to Shame, a gamified zsh tool designed to humble your command-line ego.

## About Shame
Ever felt like you're too good at the Linux terminal?
Wish typing commands felt exciting again?

Shame brings consequences back to the CLI.

Shame is a gamified shell extension that detects typos and command errors, then escalates punishments based on your failure rate. It is built around the Pressure Paradox.

Shame weaponizes this concept. The more you mess up, the worse it gets.
- Mistakes increase pressure.
- Pressure increases mistakes.
- You spiral.

The only way out?
- Get good. Stay good.

## How It Works
Shame wraps common shell commands and:
- Tracks incorrect command usage
- Maintains per-command competence scores
- Applies escalating punishments
- Dynamically adjusts probability of disruption
- Generates a periodic “Shame Wrapped” performance report

Punishments are contextual to the command being run and scale based on:
- Frequency of typos
- Historical performance
- CLI-wide failure rate

## Escalation Levels

| Mistake Count | Behavior |
|---------------|----------|
| 1–3           | Minor annoyance |
| 4–7           | Random disruptions |
| 8–12          | Aggressive chaos |

## Safety Notice 
**Shame is designed for containers that you do not care to lose. Install this tool at your own risk. We are not liable for any damage to you or your system, or for the permanent loss of files.**

## Getting Started
Shame can be installed with a simple curl command. All data is stored locally and *does not* leave your machine.
```bash
curl -fsSL https://raw.githubusercontent.com/Caffiends/HackUSU26/refs/heads/main/install.sh | sudo bash
```

## Getting Unstarted
If you're having a hard time coping with your mediocre skills, you can uninstall Shame with another curl command:
```bash
curl -fsSL https://raw.githubusercontent.com/Caffiends/HackUSU26/refs/heads/main/uninstall.sh | sudo bash
```

## Why We Built This
For a hackathon's gag/cursed tool category. 
