# Socket Video Streaming Project

This repository contains a Computer Networking course project built with Python sockets. The project demonstrates a simple video streaming system where a client controls playback through RTSP-like commands over TCP, while the server streams MJPEG video frames to the client through RTP packets over UDP.

## Project Information

- **Project name:** Socket Video Streaming Project
- **Course:** Computer Networking
- **Institution:** University of Science, VNU-HCM (HCMUS)
- **Purpose:** This project was developed for learning and practicing core networking concepts, including TCP control channels, UDP media transport, packetization, client-server communication, and basic real-time video playback.

## Team Members

| Full name | Student ID |
| --- | --- |
| Nguyen Duc Dat | 24120037 |
| Do Quoc Dai | 24120030 |
| Nguyen Trong An | 24120017 |

## Main Features

- RTSP-like control flow using TCP:
  - `SETUP`
  - `PLAY`
  - `PAUSE`
  - `TEARDOWN`
- RTP-like packet structure for media transport over UDP.
- MJPEG frame extraction and streaming.
- Client GUI built with Tkinter.
- Video frame rendering with Pillow.
- Frame chunking based on Ethernet MTU limits to avoid oversized UDP packets.
- RTP marker bit support to identify the final packet of each frame.
- Client-side frame buffering for smoother playback.
- Basic playback statistics, including bitrate, lost frames, and loss rate.

## System Architecture

The application is divided into two main parts:

1. **Server**
   - Listens for RTSP-like control requests over TCP.
   - Opens the requested MJPEG video file.
   - Splits each JPEG frame into RTP payload chunks.
   - Sends RTP packets to the client over UDP.

2. **Client**
   - Connects to the server through a TCP control connection.
   - Sends playback commands from the GUI.
   - Opens a UDP port to receive RTP packets.
   - Reassembles RTP payload chunks into JPEG frames.
   - Buffers and displays frames in the Tkinter window.

## Repository Structure

| File | Description |
| --- | --- |
| `Server.py` | Starts the server and accepts client RTSP/TCP connections. |
| `ServerWorker.py` | Handles client requests and sends RTP packets. |
| `ClientLauncher.py` | Entry point for launching the GUI client. |
| `Client.py` | Implements client state, GUI controls, RTP receiving, buffering, and playback. |
| `RtpPacket.py` | Encodes and decodes RTP packet headers and payloads. |
| `VideoStream.py` | Reads MJPEG data and extracts JPEG frames. |
| `movie.Mjpeg` | Sample MJPEG video file. |
| `TestSocketok.mjpeg` | Additional MJPEG test video file. |
| `ReportSocket.pdf` | Project report documenting the design, implementation, and results. |

## Project Report

A detailed report of the project is available in [`ReportSocket.pdf`](ReportSocket.pdf). It documents the system design, implementation details, networking decisions, and results.

## Requirements

- Python 3.x
- Pillow
- Tkinter

Tkinter is included with most standard Python installations on Windows. Pillow is required for decoding and rendering JPEG frames.

Install Pillow:

```bash
python -m pip install pillow
```

## How to Run

Open two terminals in the project directory.

### 1. Start the server

```bash
python Server.py 1025
```

The server listens for RTSP/TCP connections on port `1025`.

### 2. Start the client

```bash
python ClientLauncher.py localhost 1025 5008 movie.Mjpeg
```

Command format:

```bash
python ClientLauncher.py <server_address> <server_port> <client_rtp_port> <video_file>
```

Example using another local video file:

```bash
python ClientLauncher.py localhost 1025 5008 TestSocketok.mjpeg
```

## Client Controls

The client GUI provides four controls:

| Button | Function |
| --- | --- |
| Setup | Creates the RTSP session and prepares the RTP receiving port. |
| Play | Starts video streaming from the server. |
| Pause | Pauses streaming while keeping the session active. |
| Teardown | Ends the session and closes the client. |

## Networking Design

### RTSP-like Control Channel

The control channel uses TCP because playback commands must arrive reliably and in order. The client sends text-based requests to the server, and the server replies with a status code, sequence number, and session ID.

Example request:

```text
SETUP movie.Mjpeg RTSP/1.0
CSeq: 1
Transport: RTP/UDP; client_port= 5008
```

Example response:

```text
RTSP/1.0 200 OK
CSeq: 1
Session: 123456
```

### RTP-like Media Channel

The media channel uses UDP because video streaming benefits from low latency. Each video frame is encoded as JPEG data, split into chunks, wrapped with a 12-byte RTP-like header, and sent to the client.

The RTP packet includes:

- Version
- Marker bit
- Payload type
- Sequence number
- Timestamp
- SSRC
- Payload

The marker bit is used to indicate the final packet of a JPEG frame, allowing the client to reassemble complete frames before displaying them.

## Notes

- The project is intended for learning and demonstration purposes.
- The server and client can be run on the same machine using `localhost`.
- If running across two machines, make sure the server IP address is reachable and the client RTP port is not blocked by the firewall.
- Large MJPEG files may require more memory because frames are loaded and extracted by `VideoStream.py`.
- `__pycache__` and `.pyc` files are generated by Python at runtime and are not part of the source code.

## Educational Value

This project helps demonstrate how application-layer protocols can coordinate with transport-layer protocols. It shows why reliable TCP is useful for session control, why UDP is commonly used for media streaming, and how packet headers, sequence numbers, marker bits, and buffering support real-time video transmission.
