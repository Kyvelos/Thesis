
import nrrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load the NRRD file
file_path = "C:/02_Thesis/Resources/Patient_9/Segmentation.seg.nrrd"
data, header = nrrd.read(file_path)

# Initialize figure
fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(bottom=0.2)

# Initial slice
slice_index = data.shape[2] // 2
img = ax.imshow(data[:, :, slice_index], cmap="gray")
ax.set_title(f"Slice {slice_index}/{data.shape[2] - 1}")
ax.axis("off")

# Slider setup
ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03])
slice_slider = Slider(ax_slider, "Slice", 0, data.shape[2] - 1, valinit=slice_index, valstep=1)

# Update function
def update(val):
    slice_idx = int(slice_slider.val)
    img.set_data(data[:, :, slice_idx])
    ax.set_title(f"Slice {slice_idx}/{data.shape[2] - 1}")
    fig.canvas.draw_idle()

slice_slider.on_changed(update)

# Keyboard interaction
def on_key(event):
    global slice_index
    if event.key == "right":
        slice_index = min(slice_index + 1, data.shape[2] - 1)
    elif event.key == "left":
        slice_index = max(slice_index - 1, 0)
    slice_slider.set_val(slice_index)

fig.canvas.mpl_connect("key_press_event", on_key)

plt.show()

