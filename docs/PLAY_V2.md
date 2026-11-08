# StackChan Champion Play V2 — experimental

Status: development / not hardware-validated. Do NOT flash until the latest CoreS3 CI run succeeds and hardware caveats have been reviewed.

## English UI localization

All on-device English label translations are managed in:
`components/config_service/include/config_service/ui_english.hpp`.

The header is a key/value dictionary. Edit the **English value** of an entry without changing the key, then rebuild the firmware. Device screens (device_ui, AP QR screen, status badge), operation-mode labels, and common balloons now refer to this dictionary. This covers the K151 on-device UI; the separate Wi-Fi web settings page needs its own localization audit.

## Persian game speech

`tools/generate_play_audio.py` supports:

- `--engine piper --model <path/to/fa_IR-mana-medium.onnx>` — synthesize with the open-source Mana Persian neural voice;
- `--recording-dir assets/play_audio_fa` — optional replacement WAV files, named `dali.wav`, `red.wav`, `blue.wav`, `yellow.wav`, `bravo.wav`, `try.wav`, `find_red.wav`, `find_blue.wav`, `find_yellow.wav`;
- `--engine espeak` — legacy robotic fallback when requested explicitly.

Generated speech assets are stored in the build output header and played as local 16 kHz PCM. A human-recorded voice is still preferred for a toddler. GitHub CI uses Python venv, Piper 1.8.0 and the pinned, SHA-256 verified Mana model. No cloud calls or external network are made at runtime by games.

## Color learning

- TEACH: large color areas say the Persian color name when tapped.
- FIND GAME: the robot speaks the target color in Persian and the LCD reads LISTEN & TAP; the answer is deliberately **not** displayed.
- Correct answer says `آفرین!` and queues the next spoken target; wrong answer says `دوباره امتحان کن`.

## Peekaboo: motion-triggered experiment

The K151/CoreS3 has an onboard GC0308 camera, **not** physical hands or eyelids.
- Camera is enabled in the V2 experimental CoreS3 config; resident camera init can fail if the sensor or internal memory is unavailable.
- The game draws visual hands and uses a gentle servo pitch, waiting for a camera-motion event or optional screen touch.
- No repeated timed "Dali!" sequence. One motion/tap hides the eyes; a later one reveals the eyes and says `دالی!` locally.
- Camera detection is a coarse ~320 pixel grayscale-image difference, **not** face recognition. It cannot tell whether a child's hands cover their eyes and may trigger on lighting or background motion. It uses global brightness compensation plus a threshold and a ~1.6 s debounce.
- When camera unavailable, UI shows TAP TO PLAY and taps remain usable. No frames are retained or uploaded, and no recorded images leave the robot.
- Capture temporarily pauses display rendering and I2C pollers to prevent bus/PSRAM contention; this must be tested on real hardware. Do not assume smooth animation until tested.
- Follow-up project: if motion detection is stable, evaluate Espressif ESP-WHO face/person detection for actual visual awareness. That is **not** part of this build.

## Remaining validation

1. Latest GitHub Actions run passes both host tests and full CoreS3+recovery firmware packaging.
2. Confirm camera initialization and RAM headroom on the physical K151.
3. Confirm no I2S mic/speaker race, Persian pronunciation, UI navigation, and servo motion.
4. Check end-to-end color quiz timing, response interruption, microphone unavailable, camera unavailable.
5. Revisit the web-based settings interface for Japanese text (on-device interface is translated).
