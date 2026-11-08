# Experimental local face-based Peekaboo (NOT production firmware)

The user asked for the robot to *find a face*, turn towards it, and start
Peekaboo when the child's eyes are covered/uncovered. Arbitrary object
motion triggering the game is not acceptable.

## What this spike changes

- Adds Espressif ESP-DL's `espressif/human_face_detect` component,
  two-stage MSR/MNP model, local on the ESP32-S3. No cloud or API calls.
- Uses GC0308 RGB565BE frames inside camera_service, returned directly by the
  resident camera. Gets the largest detected face's confidence and bounding
  box. Does not store or send image frames or enroll identities.
- Before a face is found, the head makes a small, slow scan within -8..+8°
  yaw and -3..+7° pitch. This is **not guaranteed to lift the head** on the
  actual K151 without first calibrating servo zero and pitch direction.
- Acquires only after two consecutive face detections. Tracks the face with
  very small steps (2° per frame sample) clamped to ±14° yaw and -6..12°
  pitch. Actual servo orientation must be checked on hardware.
- After face acquisition, two consecutive detector misses hide the on-screen
  eyes. Two detected frames on reappearance within 12 s reveal the eyes and
  play a local Persian "دالی!" once.
- *No general motion trigger is used.* When model/camera is unavailable,
  manual tap fallback is still possible.

## Known limitations (essential)

1. **This cannot truly detect "hands covering the eyes".** Loss of a
   face bounding box is a proxy. A child leaving the frame, turning sideways
   or poor lighting can also cause a loss. Conversely, the face detector may
   continue to detect a partly covered face.
2. The K151 camera is not the same as Espressif's reference ESP32-S3-EYE
   module; the capture driver, RGB565 byte order, and CoreS3 RAM/PSRAM bus
   must all be tested.
3. Main app OTA partition is 5 MiB; previous V3 bin was 4,037,776 bytes.
   The ESP-DL code and model may exceed this partition even if the component
   compiles. CI must verify the actual binary size.
4. Camera and inference compete for PSRAM, I2C and render-time budget.
   The first model allocation has a conservative RAM headroom guard, but
   this does not guarantee successful allocation or thread-safe runtime.
5. If the head tracks in the wrong direction, turn off servo torque and do
   NOT repeatedly run the game. Servo sign and "looking upward" must be
   physically calibrated in the existing Range/Controls UI first.
6. Children's video is processed locally in RAM; face IDs/biometrics are
   not recorded. Do not upload the camera stream to public repositories.
7. This experiment must NEVER be presented as ready for children without a
   successful build and attended physical K151 tests.

## Next validation gates

- GitHub Actions: host tests + complete CoreS3 and Recovery build.
- Package check: new main image fits 5 MiB app slot.
- Boot: stable Wi-Fi, microphone, speaker and camera init; no I2C panics.
- Face search/track: find face at typical tabletop position, confirm pitch
  direction and power draw. Limit speed/force appropriately.
- Game: hands-over-eyes, ordinary toy motion, lighting, and face leaving
  frame must be distinguished enough for an acceptable preschool experience.
  Consider a dedicated eye/hand occlusion detector later if needed.

Ref:
https://developer.espressif.com/workshops/edge-ai-with-esp32-s3/assignment-2/
