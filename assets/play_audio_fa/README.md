# Record a cheerful Persian voice for StackChan (optional)

The robot does **not** need Gemini, an API key, or internet to play these clips.
All Persian lines are generated or recorded **before firmware is built** and are stored in the firmware.

## Why recordings can sound better

The free Piper/Mana Persian voice is understandable but its intonation may sound flat.
A parent, friend, or voice actor can speak the lines warmly, with pauses and excitement.
A short *whole sentence* is one recording. Avoid joining robotic words at runtime.

## Quick recording workflow

1. Read the complete, current list of audio phrases from
   `tools/generate_play_audio.py` (the `CLIPS` array). Names matter.
2. Record the lines in a quiet room using Voice Memos on macOS or iPhone.
   Use a playful voice, not an exaggerated shouted tone; leave 0.15 seconds
   of silence before and after each utterance.
3. Place mono, signed 16-bit PCM WAV files in `assets/play_audio_fa/`,
   named after the **lowercase clip IDs**: `start_red.wav`,
   `correct_yellow_then_red.wav`, `wrong_blue_for_yellow.wav`, etc.
   You only need to provide the lines you want to override; remaining lines
   still use Piper.
4. If your recording app exports M4A, on macOS run:
   `afconvert -f WAVE -d LEI16@16000 -c 1 input.m4a output.wav`
   (if that command fails, use ffmpeg:
   `ffmpeg -i input.m4a -ar 16000 -ac 1 -c:a pcm_s16le output.wav`).
5. Build the firmware. The generator checks each WAV override first, then
   falls back to the local Piper synthesis. `audio_preview/` in the
   artifact contains the actual waveform for each line.

**Full-sentence scripts:** the built-in `CLIPS` array includes 3 welcoming
first questions, 6 unique correct-answer-plus-next-question responses, and
6 wrong-answer corrective responses naming the touched color and restating
the goal. You can edit their Persian text in `tools/generate_play_audio.py`
before generating new speech; recordings override text generation.

## Important constraints

- Do not upload a child's private recordings or images. These lines can be
  recorded by an adult. Keep recordings local until you deliberately decide
  to add them to the repository; public repositories expose committed assets.
- Do not use commercial voice-cloning without consent and checking licenses.
- Do not commit unlicensed commercial/third-party voice files.
- The CoreS3 output expects signed 16-bit mono WAV input. The generator
  resamples all clips to 16 kHz and encodes them to compact mu-law in firmware.
- Prefer finished voice clips below ~6 seconds each, so playback feels quick.
