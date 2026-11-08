# Play V4 — automatic Persian colors dialogue (experimental, offline)

## What changes

- Colors starts automatically in FIND mode. No need to press FIND GAME.
- The spoken first question is a complete greeting + target-color prompt.
- For a correct tap, the response names the color, congratulates the child
  and asks for the NEXT color in a **single expressive clip**.
- For an incorrect tap, the response names the color actually touched, gently
  corrects the child and repeats the requested target in a complete sentence.
- No cloud dialogue or live TTS is used in games. The embedded phrases are
  generated during CI using Piper Mana Persian, or can be replaced by
  user-supplied adult WAV recordings (see assets/play_audio_fa/README.md).
- Audio completion gates touchscreen answers. The first speech event is no
  longer dropped by the PLAY-entry race.
- The EXPLORE button switches to the legacy "touch a color to hear its name"
  mode; PLAY GAME switches back to the full spoken challenge.

## Files

- tools/generate_play_audio.py — ordered dialogue line bank and generator
- main/play_dialogue.hpp — enum/lookup table tying selected and target colors
  to complete voice clips; clip indexes must agree with generator order
- main/device_ui.cpp — the auto-start UI and correctness logic
- main/demo_loop.cpp — speaker audio and completion handshake
- main/shared_state.hpp — audio_busy and touch gating
- assets/play_audio_fa/README.md — human-recorded voice replacement path

## Important limits

- Piper Mana is offline and low cost, **but not emotionally expressive by
  itself**. Punctuation helps segmentation; it does not turn it into a
  human narrator. To get warm preschool intonation, use recorded adult speech
  or a licensed one-time high-quality TTS conversion of the exact lines,
  then embed the WAV output. Never clone a person's voice without permission.
- The separate face detector spike is NOT included in this color-only build.
- Not validated on physical K151 yet: check listening/answer timing and
  speaker volume before merging to a generally installed firmware.
