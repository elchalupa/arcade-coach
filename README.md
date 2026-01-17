# arcade-coach

A context-aware self-care assistant for streamers.

Coach monitors your stream and sends gentle reminders to take breaks, stay hydrated, and check your posture. Unlike a simple timer, Coach waits for the right moment - it never interrupts a hype moment or active conversation.

**Philosophy:** Never interrupt a moment. Wait for the right window.

## Features

**Break Reminder**
After 2 hours of streaming, Coach reminds you to stand up, stretch, and rest your eyes.

**Hydration Nudge**
Every 45 minutes, a gentle reminder to take a sip of water.

**Posture Check**
Every 90 minutes, a reminder to sit up straight and relax your shoulders.

**Stream Duration Alert**
After 4 hours, Coach suggests considering wrapping up soon.

**Context Awareness**
Coach monitors chat activity and waits for quiet moments. It detects hype keywords and won't interrupt when chat is popping off.

## Installation

### Prerequisites

- Python 3.11+
- Windows, macOS, or Linux
- Twitch account

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/elchalupa/arcade-coach.git
   cd arcade-coach
   ```

2. Create virtual environment:
   ```
   # Windows
   py -3.11 -m venv venv
   .\venv\Scripts\Activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the application:

   If this is your first time, create your config files:
   ```
   # Windows
   if not exist config.yaml copy config.example.yaml config.yaml
   if not exist .env copy .env.example .env

   # macOS/Linux
   cp -n config.example.yaml config.yaml
   cp -n .env.example .env
   ```

5. Edit `.env` with your Twitch credentials.

6. (Optional) Customize `config.yaml` with your preferred timer intervals.

## Usage

### Start the application

```
python -m coach
```

Or on Windows:

```
start.bat
```

### What you'll see

```
  ╔═╗┌─┐┌─┐┌─┐┬ ┬
  ║  │ │├─┤│  ├─┤
  ╚═╝└─┘┴ ┴└─┘┴ ┴

  Stream Self-Care v0.1.0

[Coach] Loading configuration...
[Coach] Connecting to #yourchannel...

[Coach] Connected to #yourchannel
[Coach] Monitoring context... (Ctrl+C to stop)

[Coach] Active timers:
  - Break: 120 min remaining
  - Hydration: 45 min remaining
  - Posture: 90 min remaining
  - Duration: 240 min remaining
```

When a timer is due and chat is quiet, you'll get a notification.

## Configuration

Edit `config.yaml` to customize behavior:

```yaml
timers:
  break_reminder_minutes: 120      # 0 to disable
  hydration_reminder_minutes: 45
  posture_reminder_minutes: 90
  stream_duration_alert_minutes: 240

context:
  quiet_threshold_seconds: 30      # Seconds of silence = "quiet"
  hype_cooldown_seconds: 60        # Wait after hype before reminding
  wait_for_quiet: true             # false = ignore context, remind immediately

notifications:
  sound: true
  app_name: "Coach"
```

## Relationship to arcade-heartbeat

These are companion tools with different focuses:

- **arcade-heartbeat** = Community health (monitors chat, tracks viewers, engagement prompts)
- **arcade-coach** = Streamer health (self-care reminders with context awareness)

They can run simultaneously and share the same Twitch credentials.

## Future Enhancements

- [ ] Speaker.bot integration (detect when streamer is talking)
- [ ] Streamer.bot integration (coordinate with ad breaks)
- [ ] Custom reminder messages
- [ ] Snooze functionality
- [ ] Stream schedule awareness

## License

MIT License
