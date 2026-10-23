---
title: A nicer PowerShell prompt with Starship
date: 2026-10-10
tags: [powershell, terminal, tooling]
excerpt: Install Starship, load it from your PowerShell profile and keep the config in git.
---

[Starship](https://starship.rs) is a fast, cross-shell prompt. On PowerShell it takes two steps.

## Install

```powershell
winget install --id Starship.Starship
```

## Load it from your profile

Add this line to your PowerShell profile (`$PROFILE`):

```powershell
Invoke-Expression (&starship init powershell)
```

## Keep the config in git

Starship reads `~/.config/starship.toml`. Store the file in a repository and point `STARSHIP_CONFIG` at it, so every machine shares one prompt.

```powershell
$env:STARSHIP_CONFIG = "$HOME\repos\config-files\starship\starship.toml"
```

| Setting | Where it lives |
| --- | --- |
| Prompt layout | `starship.toml` |
| Shell hook | `$PROFILE` |
