---
title: Managing a homelab with Ansible
date: 2026-10-20
tags: [ansible, homelab, automation]
excerpt: Why I describe my servers in an inventory and playbooks instead of SSHing in by hand.
---

When a homelab grows past one machine, repeating the same SSH commands gets old. Ansible lets you describe the end state instead.

## Inventory

```ini
[ai_lab]
minirack ansible_host=192.168.1.50 ansible_user=admin
```

## A small playbook

```yaml
- hosts: ai_lab
  become: true
  tasks:
    - name: Apply system updates
      ansible.builtin.apt:
        update_cache: true
        upgrade: dist
```

Run it with:

```bash
ansible-playbook -i inventory/servers.ini main.yml
```

## Takeaways

1. Playbooks are idempotent, so re-running them is safe.
2. The inventory and playbooks double as documentation.
3. Split tasks into files early, such as `system-updates.yaml` and `app-docker.yaml`.
