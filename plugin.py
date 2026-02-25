import gradio as gr
import os
import PIL.Image
from shared.utils.plugins import WAN2GPPlugin
from shared.utils.utils import get_video_frame, get_video_info

class LiberaliaPhotoboothPlugin(WAN2GPPlugin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Components we need from the main app
        self.image_refs = self.request_component("image_refs")
        self.state = self.request_component("state")
        self.output_gallery = self.request_component("output")

    def setup_ui(self) -> None:
        """Register the tab and request components."""
        self.add_tab("liberalia_photobooth", "Liberalia Photobooth", self.build_tab_ui)
        
        # Components we need from the main app
        self.image_refs = self.request_component("image_refs")
        self.state = self.request_component("state")
        self.output_gallery = self.request_component("output")
        
        # Integration: Add a button below Generate
        self.insert_after("generate_btn", self.create_launch_button)

    def build_tab_ui(self):
        """Build the UI components inside the tab."""
        gr.Markdown("### 📸 Liberalia Photobooth")
        gr.Markdown("Load a video, find your favorite frame, and snap it as a reference image!")
        
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

    def create_launch_button(self):
        """Creates the button that will be inserted near Generate button."""
        # This button doesn't do much in Gradio since we are already in another tab,
        # but it serves as a shortcut/indicator. 
        # Actually, in Gradio, it might be better to have it switch tabs if possible.
        # But for now, just informative button.
        return gr.Button("✨ Open Liberalia Photobooth", variant="secondary")

    def on_video_change(self, video_path):
        if video_path is None:
            return gr.update(maximum=0, value=0), None
        
        try:
            _, _, _, frames_count = get_video_info(video_path)
            # Preview the first frame
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
        if video_path is None:
            return current_gallery
        
        try:
            frame = get_video_frame(video_path, int(frame_no))
            if current_gallery is None:
                current_gallery = []
            
            # Add to gallery
            current_gallery.append(frame)
            return current_gallery
        except Exception as e:
            print(f"[LiberaliaPhotobooth] Error snapping frame: {e}")
            return current_gallery

    def send_to_generator(self, state, gallery):
        if not gallery or len(gallery) == 0:
            gr.Warning("No snapshots to send!")
            return gr.update()
        
        # Get selected image if any, otherwise the last snapped
        # Gradio gallery select data is not easily accessible here without a separate state,
        # so for now we'll send all or the last one.
        # Let's say we send all snaps to the reference gallery.
        
        # In wanGP, image_refs is an AdvancedMediaGallery.
        # its value is a list of image paths.
        # We need to save the PIL images to temp files first.
        
        import tempfile
        from PIL import Image
        
        new_refs = []
        for item in gallery:
            # item can be a path (str) or a PIL Image
            if isinstance(item, tuple): item = item[0]
            
            if isinstance(item, str):
                new_refs.append(item)
            elif isinstance(item, PIL.Image.Image):
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                item.save(tmp.name)
                new_refs.append(tmp.name)
        
        # We need to append to existing refs if any
        # Since we don't have the current value of image_refs here (it's a component),
        # we return the list. Gradio will handle the update.
        
        gr.Info(f"Sent {len(new_refs)} snapshots to Generator Reference Images!")
        return new_refs

plugin = LiberaliaPhotoboothPlugin()
