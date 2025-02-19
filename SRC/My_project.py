
import nrrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons

# Define patient numbers
patients = range(1, 21)

# Directory path format for NRRD files
base_path = "C:/02_Thesis/Resources/Patient_{}/Segmentation.seg.nrrd"

# Store data for the table
table_data = [["Patient", "Total Slices", "Non-Black Slices"]]

# Compute slices for all patients
patient_slices = {}

for patient in patients:
    file_path = base_path.format(patient)
    try:
        data, header = nrrd.read(file_path)
        total_slices = data.shape[2]
        non_black_slices = sum(np.any(data[:, :, i] > 0) for i in range(total_slices))
        table_data.append([f"Patient {patient}", total_slices, non_black_slices])
        patient_slices[patient] = data  # Store patient data
    except Exception as e:
        table_data.append([f"Patient {patient}", "Error", "Error"])
        print(f"Error loading Patient {patient}: {e}")

# Create the figure for table
fig, ax_table = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.2)

# Display the table
table = ax_table.table(cellText=table_data, cellLoc='center', loc='center', colWidths=[0.4, 0.3, 0.3])
ax_table.axis("off")

# Button for selecting a patient
ax_button = plt.axes([0.4, 0.05, 0.2, 0.07])  # Position
button = Button(ax_button, "Select Patient")

# New figure for radio buttons (patient selection)
fig_select, ax_select = plt.subplots(figsize=(4, 8))
plt.subplots_adjust(left=0.3)

# Create radio buttons for patient selection
ax_radio = plt.axes([0.05, 0.2, 0.4, 0.7])  # Position for radio buttons
radio = RadioButtons(ax_radio, [str(p) for p in patients])

selected_patient = None


def on_button_clicked(event):
    """Handles patient selection when the button is clicked."""
    global selected_patient

    # Get the selected patient
    selected_patient = int(radio.value_selected)

    # Close selection window
    plt.close(fig_select)
    plt.close(fig)

    # Load and display the selected patient
    display_patient(selected_patient)


button.on_clicked(on_button_clicked)


def display_patient(patient_num):
    """Displays the heart slices for the selected patient with a slider."""
    global fig_img

    # Load patient data
    data = patient_slices.get(patient_num, None)
    if data is None:
        print(f"Error: No data for Patient {patient_num}")
        return

    total_slices = data.shape[2]

    # Create a new figure for image display
    fig_img, ax_img = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.2)

    # Show initial slice
    slice_index = total_slices // 2
    img = ax_img.imshow(data[:, :, slice_index], cmap="gray")
    ax_img.set_title(f"Patient {patient_num} - Slice {slice_index}/{total_slices - 1}")
    ax_img.axis("off")

    # Slider setup
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03])
    slice_slider = Slider(ax_slider, "Slice", 0, total_slices - 1, valinit=slice_index, valstep=1)

    # Update function
    def update(val):
        slice_idx = int(slice_slider.val)
        img.set_data(data[:, :, slice_idx])
        ax_img.set_title(f"Patient {patient_num} - Slice {slice_idx}/{total_slices - 1}")
        fig_img.canvas.draw_idle()

    slice_slider.on_changed(update)

    # Show new figure
    plt.show()


# Show patient selection window and table
plt.show()
