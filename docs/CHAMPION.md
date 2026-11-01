# StackChan Champion (K151 / CoreS3)

Experimental public fork of ciniml/stackchan-idf. This branch changes Gemini Live to the stable `gemini-3.8-live` model and enables server-managed `googleSearch` while preserving existing robot function tools.

## Build
Actions > Champion CoreS3 (Gemini Live + Google Search) > run the workflow from the feature branch. After a successful build download and extract `champion-cores3-firmware`. The workflow builds BOTH main and recovery, and packages the upstream ADR-001 boot layout using `script/pack_release.py`.

## Flash (only after successful build)
The artifact's `flash_args` describes the required offsets. Do NOT flash the application binary at a guessed address. On macOS, with a connected CoreS3, Python 3.12 and esptool 4.10 installed in a virtual environment, run from the extracted artifact directory:

```bash
python -m esptool --chip esp32s3 --port /dev/cu.usbmodemXXXX --baud 460800 write_flash @flash_args
```

Change the port to the real USB serial device. This replaces the factory firmware and may erase settings. Restore official firmware using M5Burner if needed. USB flashing has NOT been tested by this project on real hardware.

## Configure
Use https://ciniml.github.io/stackchan-idf/settings.html in desktop Chrome/Edge to configure Wi-Fi (2.4 GHz), Gemini provider, API key, and conversation enabled. Never commit credentials to this repo. Search grounding and realtime audio can incur Google API charges.

## Next
Offline Peekaboo (touch head, gentle animation, prerecorded Persian voice) and interactive Red/Blue/Yellow color games are scoped for later work. Neither is implemented yet.
