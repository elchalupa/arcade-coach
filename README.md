# arcade-coach

Context-aware stream management — intelligent timing for breaks, ads, and self-care reminders.

## Philosophy

**Never interrupt a moment. Wait for the right window.**

Dumb timers fire regardless of context. arcade-coach understands what's happening in your stream and waits for the right moment to nudge you.

| Dumb Timer | Smart Coach |
|------------|-------------|
| "Break every 30 min" | "2 hours without a break, chat just went quiet — good time" |
| "Run ads now" | "Ad timer up, but chat is hyped — snoozing 10 min" |
| "Drink water" | "You've been talking nonstop — take a sip" |

## Features (Planned)

### Health Reminders
- **Break reminder** — 2+ hours since last break (configurable)
- **Hydration nudge** — 45 min intervals
- **Posture check** — 90 min intervals
- **"You've been live X hours"** — Long stream awareness

### Context-Aware Timing
All reminders wait for a "good window":
- Chat velocity low (quiet moment)
- No emotional moments in progress
- No intense gameplay keywords detected
- Streamer not mid-sentence (Speaker.bot integration)

### Ad Management
- Detect when ad timer fires
- Auto-snooze if chat is hype
- Notify when a good ad window opens

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ARCADE-COACH                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Signal Collectors                    │   │
│  │                                                     │   │
│  │  • Chat velocity (Twitch IRC)                       │   │
│  │  • Keywords detection                               │   │
│  │  • Streamer voice activity (Speaker.bot)            │   │
│  │  • Manual snooze commands                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Context Engine                      │   │
│  │                                                     │   │
│  │  is_good_time_for("break") → (bool, reason)         │   │
│  │  is_good_time_for("ad") → (bool, reason)            │   │
│  │  is_good_time_for("hydration") → (bool, reason)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Action Manager                      │   │
│  │                                                     │   │
│  │  • Health timers (break, water, posture)            │   │
│  │  • Ad timer integration                             │   │
│  │  • Snooze queue                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│              ┌────────────┼────────────┐                   │
│              ▼            ▼            ▼                   │
│       ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│       │  Toast   │ │Streamer  │ │ Speaker  │              │
│       │ Notifs   │ │  .bot    │ │  .bot    │              │
│       └──────────┘ └──────────┘ └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## The "Good Time" Algorithm

```python
def is_good_time_for(action: str) -> tuple[bool, str]:
    # Blockers - never interrupt these
    if chat_velocity > HIGH_THRESHOLD:
        return (False, "Chat is popping off")
    
    if detected_keywords(["boss", "fight", "clutch", "run", "close"]):
        return (False, "Intense gameplay detected")
    
    if streamer_actively_talking:  # Speaker.bot
        return (False, "You're mid-sentence")
    
    # Enablers - good windows
    if chat_velocity < LOW_THRESHOLD:
        return (True, "Chat is quiet")
    
    if streamer_silent_for(minutes=2):
        return (True, "Natural pause")
    
    return (False, "No clear window yet")
```

## Integration Points

| System | Purpose | Required |
|--------|---------|----------|
| Twitch IRC | Chat monitoring | Yes |
| Windows Toasts | Notifications | Yes |
| Speaker.bot | Voice activity detection | Optional |
| Streamer.bot | Action triggers, ad control | Optional |

## Configuration

```yaml
# Reminder intervals
health:
  break_reminder_hours: 2
  hydration_minutes: 45
  posture_minutes: 90
  stream_duration_alert_hours: 4

# Context thresholds
context:
  chat_velocity_high: 10    # msgs/min = hype
  chat_velocity_low: 2      # msgs/min = quiet
  silence_window_seconds: 30

# Keywords that block reminders
blockers:
  keywords:
    - "boss"
    - "fight"
    - "clutch"
    - "run"
    - "close"
    - "dont"
    - "wait"

# Integrations
integrations:
  speakerbot:
    enabled: false
    websocket_url: "ws://localhost:7474"
  streamerbot:
    enabled: false
    websocket_url: "ws://localhost:8080"
```

## Relationship to arcade-heartbeat

| arcade-heartbeat | arcade-coach |
|------------------|--------------|
| Community health monitor | Streamer health manager |
| "Is my chat engaged?" | "Is now a good time?" |
| Viewer-focused | Streamer-focused |
| Engagement prompts | Self-care prompts |

Both tools share:
- Twitch IRC monitoring
- Windows toast notifications
- YAML configuration
- Prompt customization

They can run independently or together as part of the arcade suite.

## Related Projects

- [arcade-heartbeat](https://github.com/elchalupa/arcade-heartbeat) — Community engagement monitor
- [arcade-tts](https://github.com/elchalupa/arcade-tts) — Channel point TTS
- [arcade-jam](https://github.com/elchalupa/arcade-jam) — AI jam roulette

## License

MIT License — See [LICENSE](LICENSE) for details.
