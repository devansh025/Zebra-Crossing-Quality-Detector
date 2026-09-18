import os
import tkinter as tk
from tkinter import filedialog, messagebox

from core import pipeline
from utils import visualization
from utils import history


class ZebraCrossingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zebra Crossing Quality Detector")
        self.root.geometry("950x650")

        self.selected_file = None
        self.last_result = None

        self.build_widgets()

    def build_widgets(self):
        title_label = tk.Label(
            self.root, text="Zebra Crossing Quality Detector", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.original_label = tk.Label(self.root, text="Original Image", bg="#eeeeee")
        self.original_label.grid(row=1, column=0, padx=10, pady=5)

        self.edge_label = tk.Label(self.root, text="Processed/Edge Image", bg="#eeeeee")
        self.edge_label.grid(row=1, column=1, padx=10, pady=5)

        self.overlay_label = tk.Label(self.root, text="Detected Crossing", bg="#eeeeee")
        self.overlay_label.grid(row=1, column=2, padx=10, pady=5)

        self.original_canvas = tk.Label(self.root, width=350, height=280, bg="#dddddd")
        self.original_canvas.grid(row=2, column=0, padx=10, pady=5)

        self.edge_canvas = tk.Label(self.root, width=350, height=280, bg="#dddddd")
        self.edge_canvas.grid(row=2, column=1, padx=10, pady=5)

        self.overlay_canvas = tk.Label(self.root, width=350, height=280, bg="#dddddd")
        self.overlay_canvas.grid(row=2, column=2, padx=10, pady=5)

        results_frame = tk.Frame(self.root)
        results_frame.grid(row=3, column=0, columnspan=3, pady=15)

        self.stripe_var = tk.StringVar(value="Stripe Count: -")
        self.visibility_var = tk.StringVar(value="Visibility: -")
        self.score_var = tk.StringVar(value="Quality Score: -")
        self.condition_var = tk.StringVar(value="Condition: -")

        tk.Label(results_frame, textvariable=self.stripe_var, font=("Arial", 12)).grid(
            row=0, column=0, padx=20
        )
        tk.Label(results_frame, textvariable=self.visibility_var, font=("Arial", 12)).grid(
            row=0, column=1, padx=20
        )
        tk.Label(results_frame, textvariable=self.score_var, font=("Arial", 12)).grid(
            row=0, column=2, padx=20
        )
        tk.Label(results_frame, textvariable=self.condition_var, font=("Arial", 12, "bold")).grid(
            row=0, column=3, padx=20
        )

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=3, pady=15)

        tk.Button(button_frame, text="Select Image", width=15, command=self.select_image).grid(
            row=0, column=0, padx=10
        )
        tk.Button(button_frame, text="Process Image", width=15, command=self.process_image).grid(
            row=0, column=1, padx=10
        )
        tk.Button(button_frame, text="Reset", width=15, command=self.reset).grid(
            row=0, column=2, padx=10
        )
        tk.Button(button_frame, text="Save Result", width=15, command=self.save_result).grid(
            row=0, column=3, padx=10
        )

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Road Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")],
        )
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("Image Selected", os.path.basename(file_path))

    def process_image(self):
        if not self.selected_file:
            messagebox.showwarning("No Image", "Please select an image first")
            return

        result = pipeline.process_image(self.selected_file)

        if not result.success:
            messagebox.showerror("Error", result.message)
            return

        self.last_result = result

        original_tk = visualization.cv2_to_tk(result.original_image)
        edge_tk = visualization.cv2_to_tk(result.edge_image)
        overlay_tk = visualization.cv2_to_tk(result.overlay_image)

        self.original_canvas.configure(image=original_tk)
        self.original_canvas.image = original_tk

        self.edge_canvas.configure(image=edge_tk)
        self.edge_canvas.image = edge_tk

        self.overlay_canvas.configure(image=overlay_tk)
        self.overlay_canvas.image = overlay_tk

        self.stripe_var.set(f"Stripe Count: {result.stripe_count}")
        self.visibility_var.set(f"Visibility: {result.visibility_percent}%")
        self.score_var.set(f"Quality Score: {result.quality_score}/100")
        self.condition_var.set(f"Condition: {result.condition}")

        history.log_result(
            os.path.basename(self.selected_file),
            result.stripe_count,
            result.visibility_percent,
            result.quality_score,
            result.condition,
        )

    def reset(self):
        self.selected_file = None
        self.last_result = None

        self.original_canvas.configure(image="")
        self.edge_canvas.configure(image="")
        self.overlay_canvas.configure(image="")

        self.stripe_var.set("Stripe Count: -")
        self.visibility_var.set("Visibility: -")
        self.score_var.set("Quality Score: -")
        self.condition_var.set("Condition: -")

    def save_result(self):
        if not self.last_result:
            messagebox.showwarning("No Result", "Process an image before saving")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG file", "*.jpg"), ("PNG file", "*.png")],
        )

        if save_path:
            visualization.save_result_image(self.last_result.overlay_image, save_path)
            messagebox.showinfo("Saved", f"Result saved to {save_path}")


def run_app():
    root = tk.Tk()
    app = ZebraCrossingApp(root)
    root.mainloop()
