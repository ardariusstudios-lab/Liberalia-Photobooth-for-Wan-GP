# Liberalia-Photobooth-for-Wan-GP
Your one stop shop for capturing frames and using them for new Generations (this project is made by a non coding autistic but good planner and prompter using Anti Grav)
If you get stuck watch this video https://youtu.be/LjYMxzsapvg?si=w4BNVi4cAe2V4fe1 always remember to snap a picture first so it appears bellow before sending it to a VACE modal. this is untested with Image to Video modals as of now

# Simaler but diffrent
the Liberalia photo booth is diffrent to the Wan GP Gallery plugin for the fact you can load any video in and snap ANY frame.

# Known Bug
You have a button that says open in Photobooth sadly in the first version this is not working.
once Wantastic is off to a good start I will Revisit this issue it's a known bug and should not affect usage.

# 📸 Liberalia Photobooth — WanGP Plugin

A plugin for [WanGP](https://github.com/deepbeepmeep/Wan2GP) that adds a dedicated **Photobooth** tab, letting you load generated videos, snap high-quality frames, and send them directly to the Generator as reference images.

---

## Features

- 🎬 **Video Frame Browser** — Load any `.mp4` and scrub through frames with a slider (may upgrade to support more formats later on)
- 📸 **Frame Snapping** — Capture the current frame as a full-resolution PNG you must do this first.
- 🖼️ **Snapshot Gallery** — Browse all snapped frames in a session gallery
- 📤 **Send to Generator** — Push one or all snapshots to the Generator's Reference Images input (perfect for VACE / Phantom workflows) untested with Image to video but should work with single images.
- 💾 **Persistent Storage** — Snapshots are saved to `outputs/liberalia_photobooth/` with timestamps
- Refare to my demo video to see how to use it correctly https://youtu.be/LjYMxzsapvg?si=7ZzVHC6GLIWWeSXV

# Disclamer/Contact Info
this project is developed by an individual dignosed with savere autisim and leaning difficaltys it would not be here at all if Anti Grav did not exsist. please remember this when filing issues I also do not always have the internet and work on lots of projects at once. so sorry for any wait for fixes. if you urgently want to talk to me your best option is Discord. on the Wan GP server or My Private Server https://discord.gg/XUtF2mmU3Q I check Discord most days.

---

## Installation

### Option A — Manual
1. Copy the `liberalia-photobooth/` folder into your WanGP `plugins/` directory.
2. Open `wgp_config.json` and add `"liberalia-photobooth"` to the `enabled_plugins` list:
   ```json
   "enabled_plugins": ["liberalia-photobooth"]
   ```
3. Restart WanGP.

### Option B — Zip
1. Download `liberalia-photobooth.zip`.
2. Extract it so that `liberalia-photobooth/` ends up inside your WanGP `plugins/` folder.
3. Enable it in `wgp_config.json` as above and restart.

---

## Usage

1. **Liberalia Photobooth Tab** — Click the tab in the main WanGP interface.
2. **Load Video** — Drag and drop or select any generated video.
3. **Browse Frames** — Use the **Frame Number** slider to seek.
4. **Snap** — Click 📸 **Snap Frame** to save the current frame to the gallery.
5. **Send** — Click 📤 **Send to Generator** to push all snapped frames to Reference Images.
6. **Clear** — Click 🗑️ **Clear Snapshots** to reset the session gallery (saved files are kept on disk).

A shortcut **✨ Open Liberalia Photobooth** button is also injected next to the **Generate** button for quick access.

---

## File Structure

```
plugins/
└── liberalia-photobooth/
    ├── plugin.py           # Main plugin logic & UI
    ├── plugin_info.json    # Plugin metadata
    ├── __init__.py
    └── README.md
```

Snapshots are saved to:
```
outputs/
└── liberalia_photobooth/
    ├── snap_20260223_090000_123456.png
    └── ...
```

---

## Requirements

All dependencies are bundled with WanGP:
- `gradio`
- `Pillow`
- `opencv-python` (via `shared.utils.utils`)

---

## Compatibility

Tested with WanGP. Does not modify any core WanGP files.

---

## License

MIT — feel free to use, fork, and improve! Please Credit Liberalia when sharing.
