# StackChan Champion — Offline Play

## Why this version exists

The first proof-of-concept had no game audio and required manual tapping to reveal Peekaboo. This change replaces that placeholder. It is still awaiting **physical K151 verification**.

## PLAY tab on the robot

Tap the upper-right screen corner and navigate to **PLAY** using the small tabs or a sideways swipe. Tap **COLORS** or **PEEKABOO**. **BACK** returns to the game menu, and closing PLAY returns to the regular face.

### Peekaboo — automatic (no repeated taps)

- The robot hides behind cartoon hands/eyelids on its display and gently tilts its head.
- After a short pause it lifts its head, reveals two eyes and says **«دالی!»** in synthesized Persian.
- It pauses and repeats the hide/reveal cycle automatically.
- Optional screen tap advances the cycle immediately.
- The physical K151 robot has no arms and cannot put physical hands over its eyes. This version simulates that gesture with a screen animation and a head tilt.

### Colors — interactive learning

- Tap RED, BLUE, or YELLOW: the robot speaks «قرمز»، «آبی»، or «زرد» using **embedded offline Persian audio**.
- Press **FIND GAME** to hear a Persian request to find a specified color. Tapping the right one plays «آفرین!» then asks for another. Tapping an incorrect tile plays «دوباره امتحان کن».
- Press **TEACH** to return to tapping colors to hear their names.
- The screen uses English labels for parents while Persian script rendering remains unsupported by the Japanese font.

## Audio implementation and limitations

Audio assets are synthesized during CI with the locally installed eSpeak Persian voice and embedded in the compiled firmware as 8 kHz mu-law. Runtime decoding to 16 kHz PCM is local on the device. No TTS cloud service, key, internet or recurring cost is needed for these game sounds. **Voice quality is intentionally robotic.** We should later substitute a consenting parent-recorded Persian voice for warmer and clearer prompts.

While PLAY is open, the Gemini conversation task suspends its network session and the MicLipSync task relinquishes its I2S microphone. A short closing-drain guard prevents the mic from resuming during the last spoken phrase. If boot mode is Conversation, the firmware may attempt a Gemini connection *before* PLAY is opened; switching default operation to MicLipSync avoids such initial cloud requests.

## Tests

- Host source-contract tests check the audio generator, game event wiring, automated cycle, and I2S/mic handoff.
- CoreS3 build creates the offline audio assets using eSpeak, then builds the complete main + recovery firmware and packages the expected flash layout.
- **Build success is not hardware success.** Test speaker routing, head motion, and touch interactions on the K151 before merging.
