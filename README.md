# ARRF — Arduino · ROS · Raspberry · FastAPI

Control a **servo** and an **LED** on an Arduino Uno from any device, across a chain of
technologies: Arduino → Raspberry Pi (ROS 2 Lyrical) → FastAPI → UI.

## What it does

- Rotate a servo to a commanded angle (0–180°)
- Switch one LED on/off
- Report the real servo position back to the UI (potentiometer feedback)

## Architecture

```
┌──────────────┐  USB (ROSSerial)   ┌───────────────────────────────┐  HTTP/WebSocket  ┌───────────────┐
│  Arduino Uno │ ◀────────────────▶ │  Raspberry Pi 4 (headless)    │ ◀───────────────▶ │  UI (ARRF_ui) │
│  servo + LED │                    │  ROS 2 Lyrical + FastAPI      │                   │  slider+button│
└──────────────┘                    └───────────────────────────────┘                   └───────────────┘
```

## Tech stack

| Layer | Technology |
|---|---|
| Microcontroller | Arduino Uno (C++, Arduino framework, rosserial) |
| Single-board computer | Raspberry Pi 4, Ubuntu 26.04 |
| Robot middleware | ROS 2 **Lyrical Luth** (`lyrical`) |
| Backend | FastAPI + Uvicorn (Python, `rclpy`) |
| Arduino ↔ Pi | USB serial, via rosserial |
| Pi ↔ UI | HTTP + WebSocket |
| Python dependencies | managed with `uv` |

## API contract

| Method | Endpoint | Request body | Response |
|---|---|---|---|
| `POST` | `/servo` | `{"angle": 90.0}` | `{"ok": true}` |
| `GET`  | `/servo` | — | `{"angle": 88.0}` |
| `WS`   | `/ws` | `{"angle": 90.0}` | `{"angle": 88.0}` |

> TODO: add `/led` endpoints once the LED is exposed over ROS.

## Repository structure

```
ARRF_robot/
├── arduino/
│   └── servo_led/          # Arduino sketch (folder name must match .ino)
├── scripts/
│   └── flash.sh            # build + flash via arduino-cli
├── ros2_ws/
│   └── src/                # ROS 2 packages (rosserial bridge, api_server)
└── README.md
```

## Getting started

### Prerequisites

- [Arduino CLI](https://arduino.github.io/arduino-cli/latest/getting-started/)
- [ROS 2 Lyrical](https://docs.ros.org/en/ros2_documentation/lyrical/) on the Raspberry Pi
- Python + `uv`

### Build & flash the Arduino

```bash
# TODO: replace with the final command once flash.sh exists
./scripts/flash.sh <PORT>
```

### Run on the Raspberry Pi

```bash
# TODO: document launching rosserial_server + the FastAPI server
```

## Roadmap

- [ ] Phase 1 — servo + LED standalone (no ROS)
- [ ] Phase 2 — ROS 2 basics on the Pi
- [ ] Phase 3 — rosserial: Arduino becomes a ROS 2 node
- [ ] Phase 4 — servo/LED control over ROS topics
- [ ] Phase 5 — FastAPI layer (REST, then WebSocket)
- [ ] Phase 6 — polish (safety, systemd, docs)

## Related

- **ARRF_ui** — the frontend that talks to this backend's API.