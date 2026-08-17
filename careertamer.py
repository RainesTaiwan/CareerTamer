#!/usr/bin/env python3
"""CareerTamer CLI: a personal AI career agent backed by the Claude API.

Modules (see system_prompt.py for the full spec Claude follows):
  /path              Evolution Tree - skill roadmap
  /interview [topic] Boss Fight - one-question-at-a-time mock interview
  /log [what I did]  Quest Log - formats + saves a daily update
  /daily             Daily Sync - dashboard for today
  (paste a JD)       Job Matcher - match rate + resume tweaks
"""
import os
import sys

from anthropic import Anthropic

import storage
from system_prompt import SYSTEM_PROMPT

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
MAX_TOKENS = 1500

INIT_BANNER = (
    "**[System Online] CareerTamer Initialized.** "
    "歡迎回來。請提供你目前的『履歷摘要/技能樹』以及『短期求職目標』，"
    "我將為你建立初始 Career Profile，並準備開始我們的第一次 Daily Sync。"
)


def build_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.")
    return Anthropic(api_key=api_key)


def ask_claude(client: Anthropic, history: list[dict]) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return "".join(block.text for block in response.content if block.type == "text")


def run_initialization() -> dict:
    print(INIT_BANNER)
    resume_summary = input("\n> 履歷摘要/技能樹: ").strip()
    short_term_goal = input("> 短期求職目標: ").strip()
    profile = {
        "resume_summary": resume_summary,
        "short_term_goal": short_term_goal,
        "main_goal": short_term_goal,
    }
    storage.save_profile(profile)
    print("\nCareer Profile saved. Type /daily to start, or /help for all commands.\n")
    return profile


def context_prefix(profile: dict, command: str) -> str:
    base = f"[Career Profile on file]\n{storage.profile_as_context(profile)}"
    if command == "/daily":
        base += f"\n\n[Most recent Quest Log entry]\n{storage.last_quest_log_entry()}"
    return base


def print_help() -> None:
    print(__doc__)


def main() -> None:
    client = build_client()
    profile = storage.load_profile() if storage.profile_exists() else run_initialization()

    history: list[dict] = []
    print("CareerTamer ready. Type /help for commands, /exit to quit.\n")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input in ("/exit", "/quit"):
            break
        if user_input == "/help":
            print_help()
            continue

        command = user_input.split()[0] if user_input.startswith("/") else None
        prefixed_input = f"{context_prefix(profile, command)}\n\n[My message]\n{user_input}"
        history.append({"role": "user", "content": prefixed_input})

        reply = ask_claude(client, history)
        history.append({"role": "assistant", "content": reply})
        print(f"\ncareertamer> {reply}\n")

        if command == "/log":
            storage.append_quest_log_entry(reply)
            print("(saved to data/quest_log.md)\n")


if __name__ == "__main__":
    main()
