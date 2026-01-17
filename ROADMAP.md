# arcade-coach Roadmap

## Phase 1: Foundation

- [ ] Project structure and configuration
- [ ] Twitch IRC connection (shared pattern with heartbeat)
- [ ] Basic timer system (break, hydration, posture)
- [ ] Windows toast notifications
- [ ] Manual snooze command

**Deliverable:** Timers fire, but without context awareness.

---

## Phase 2: Context Engine

- [ ] Chat velocity tracking (messages per minute)
- [ ] Keyword detection (boss, fight, clutch, etc.)
- [ ] `is_good_time_for()` algorithm
- [ ] Snooze queue (deferred reminders wait for window)

**Deliverable:** Reminders wait for quiet moments.

---

## Phase 3: Speaker.bot Integration

- [ ] WebSocket connection to Speaker.bot
- [ ] Voice activity detection
- [ ] "Streamer talking" signal
- [ ] Silence window detection

**Deliverable:** Reminders wait until you stop talking.

---

## Phase 4: Streamer.bot Integration

- [ ] WebSocket connection to Streamer.bot
- [ ] Ad timer awareness
- [ ] Ad snooze triggering
- [ ] Custom action triggers

**Deliverable:** Smart ad management.

---

## Phase 5: Advanced Context

- [ ] Sentiment integration (from heartbeat or built-in)
- [ ] Emotional moment detection (don't interrupt)
- [ ] Hype detection (sustained high velocity)
- [ ] Cooldown after hype (wait for settle)

**Deliverable:** Never interrupts important moments.

---

## Phase 6: Health Dashboard

- [ ] Session statistics (breaks taken, stream duration)
- [ ] End-of-stream summary
- [ ] Weekly health report
- [ ] Streamer wellness trends

**Deliverable:** Long-term health tracking.

---

## Future Ideas

- **Voice reminders** — TTS speaks the reminder (via arcade-tts)
- **OBS integration** — Pause/dim game capture during breaks
- **Break activities** — Suggest stretches, eye exercises
- **Community breaks** — "Chat, I'm taking a 5 min break"
- **Multi-stream awareness** — Knows if you streamed yesterday
- **Caffeine tracking** — "You've had 3 coffees, maybe water?"
