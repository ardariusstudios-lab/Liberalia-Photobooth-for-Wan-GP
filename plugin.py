import gradio as gr
import os
from shared.utils.plugins import WAN2GPPlugin
from shared.utils.utils import get_video_frame, get_video_info

# Dedicated output folder for photobooth snapshots
PHOTOBOOTH_OUTPUT_DIR = os.path.join("outputs", "liberalia_photobooth")


class LiberaliaPhotoboothPlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()

    def setup_ui(self) -> None:
        """Register the tab and request components from the main app."""
        self.add_tab("liberalia_photobooth", "Liberalia Photobooth", self.build_tab_ui)

        # Components we need from the main app
        self.image_refs = self.request_component("image_refs")
        self.state = self.request_component("state")

        # Integration: Wait, the user wants this removed as it never worked.
        # self.insert_after("generate_btn", self.create_launch_button)

    def build_tab_ui(self):
        """Build the UI components inside the tab."""
        gr.Markdown("### 📸 Liberalia Photobooth")
        gr.Markdown("Load a video, find your favorite frame, and snap it as a reference image for the generator!")

        with gr.Row():
            with gr.Column(scale=2):
                self.video_input = gr.Video(label="Input Video", interactive=True, height=300)
                self.frame_slider = gr.Slider(minimum=0, maximum=100, step=1, label="Frame Number", value=0, interactive=True)
                self.snap_btn = gr.Button("📸 Snap Frame", variant="primary")

            with gr.Column(scale=1):
                self.preview_image = gr.Image(label="Preview", interactive=False, height=300)
                self.send_to_gen_btn = gr.Button("📤 Send to Generator", variant="secondary")

        self.snaps_gallery = gr.Gallery(label="Captured Snapshots", columns=4, height=300, preview=True)
        self.clear_snaps_btn = gr.Button("🗑️ Clear Snapshots", size="sm")

        # Wire events
        self.video_input.change(
            fn=self.on_video_change,
            inputs=[self.video_input],
            outputs=[self.frame_slider, self.preview_image]
        )

        self.frame_slider.change(
            fn=self.update_preview,
            inputs=[self.video_input, self.frame_slider],
            outputs=[self.preview_image],
            show_progress="hidden"
        )

        self.snap_btn.click(
            fn=self.snap_frame,
            inputs=[self.video_input, self.frame_slider, self.snaps_gallery],
            outputs=[self.snaps_gallery]
        )

        self.send_to_gen_btn.click(
            fn=self.send_to_generator,
            inputs=[self.state, self.snaps_gallery],
            outputs=[self.image_refs]
        )

        self.clear_snaps_btn.click(
            fn=lambda: [],
            outputs=[self.snaps_gallery]
        )


    def on_video_change(self, video_path):
        if video_path is None:
            return gr.update(maximum=0, value=0), None

        try:
            _, _, _, frames_count = get_video_info(video_path)
            first_frame = get_video_frame(video_path, 0)
            return gr.update(maximum=max(0, frames_count - 1), value=0), first_frame
        except Exception as e:
            print(f"[LiberaliaPhotobooth] Error loading video: {e}")
            return gr.update(maximum=0, value=0), None

    def update_preview(self, video_path, frame_no):
        if video_path is None:
            return None
        try:
            return get_video_frame(video_path, int(frame_no))
        except Exception:
            return None

    def snap_frame(self, video_path, frame_no, current_gallery):
        """Captures a frame and saves it to the dedicated photobooth output folder."""
        if video_path is None:
            return current_gallery

        try:
            from PIL import Image
            frame = get_video_frame(video_path, int(frame_no), return_PIL=True)
            if frame is None:
                return current_gallery

            os.makedirs(PHOTOBOOTH_OUTPUT_DIR, exist_ok=True)

            # Build a unique filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            save_path = os.path.join(PHOTOBOOTH_OUTPUT_DIR, f"snap_{timestamp}.png")

            if isinstance(frame, Image.Image):
                frame.save(save_path)
            else:
                # frame may be a numpy array
                Image.fromarray(frame).save(save_path)

            if current_gallery is None:
                current_gallery = []
            current_gallery.append(save_path)
            return current_gallery

        except Exception as e:
            print(f"[LiberaliaPhotobooth] Error snapping frame: {e}")
            return current_gallery

    def send_to_generator(self, state, gallery):
        """Sends all snapped images to the Generator's Reference Images input."""
        if not gallery or len(gallery) == 0:
            gr.Warning("No snapshots to send!")
            return gr.update()

        new_refs = []
        for item in gallery:
            if isinstance(item, tuple):
                item = item[0]
            if isinstance(item, str) and os.path.isfile(item):
                new_refs.append(item)

        if not new_refs:
            gr.Warning("No valid snapshot files found.")
            return gr.update()

        gr.Info(f"Sent {len(new_refs)} snapshot(s) to Generator Reference Images!")
        return new_refs
