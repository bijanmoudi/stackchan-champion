# Offline Play MVP (StackChan Champion)

**Status:** First implementation; CoreS3 build and hardware interaction still need validation.

## How to launch (on the robot)

1. Tap the top-right corner to open the on-device settings UI.
2. Use the right arrow or swipe horizontally to find the **PLAY** tab.
3. Choose **COLORS** or **PEEKABOO**.
4. Tap **BACK** to switch games, or close the on-device UI to return to the robot's face.

### Colors
Three oversized touchscreen choices (RED / BLUE / YELLOW). Each tap highlights the chosen color and displays its name. This is a visual MVP; spoken Persian color names and the find-a-color challenge will come next.

### Peekaboo
Tap anywhere in the play area to alternate between **WHERE AM I?** and a pair of animated-style eyes with **PEEKABOO!**. This is a visual MVP; real head-touch triggering, gentle servo movement, and a prerecorded Persian "دالی!" sound will come next.

## Offline guarantee

Entering the **PLAY** tab sets `SharedState::play_mode_active`. The conversation task sees this flag and closes its WebSocket + microphone session before the game proceeds, then reconnects once the user exits PLAY. The game itself never sends audio or text to a cloud API. There may be a startup Gemini connection **before** PLAY is opened if the saved operation mode is Conversation; switch to `MicLipSync` in the phone settings if you want zero AI requests even at boot.

## Known constraints

- No Persian audio yet (we should add a user-supplied or appropriately licensed prerecorded clip).
- No head-touch activation yet; on-screen taps only.
- Quota-rejection handling halts the conversation task until reboot. Play still works on its own.
- Build success does not prove on-device hardware behavior.
