import pandas as pd
import numpy as np
import nibabel as nb
import sys

# User settings: update these paths before running the script.
# SUBJECTS_CSV_PATH should point to a CSV with one subject ID per row.
# Example rows: 001, 002, sub-003
SUBJECTS_CSV_PATH = "path/to/subject_ids.csv"

# FREESURFER_DIR should point to the folder that contains sub-*/mri folders.
# Example structure:
# path/to/freesurfer/sub-001/mri/lh.hippoAmygLabels-T1-T2.v21.FS60.nativeSpace.nii.gz
FREESURFER_DIR = "path/to/freesurfer"

# OUTPUT_CSV_PATH is where the voxel counts will be saved.
OUTPUT_CSV_PATH = "path/to/volume_of_lh_hippocampus.csv"

LABEL_FILE_NAME = "lh.hippoAmygLabels-T1-T2.v21.FS60.nativeSpace.nii.gz" # you can change this to the left or right hippocampus label file

# Place participant's mask into Nibabel.
def sum_of_voxels(s, ROI):
	img_path = f"{FREESURFER_DIR}/sub-{s}/mri/{LABEL_FILE_NAME}"
	img = nb.load(img_path)
	data = np.asanyarray(img.dataobj, dtype='int32')
	
	
	if ROI == "Subiculum":
		total = np.sum(data == 203) + np.sum(data == 204) + np.sum(data == 205)
	elif ROI == "GC_ML_DG":
		total = np.sum(data == 210) + np.sum(data == 214) 
	else:
		total = np.sum(data == dictionary[ROI])

	return total

def save_csv():
	global df
	df.to_csv(OUTPUT_CSV_PATH, header = True, sep = ',', index = False)
	return None

def read_subjects_from_csv(csv_file_path):
	"""Read subject IDs from a CSV file (one subject per line)"""
	try:
		# Read the CSV file - assuming one column with subject IDs
		subjects_df = pd.read_csv(csv_file_path, header=None)
		# Extract subject IDs and remove 'sub-' prefix if present
		subjects = []
		for subject in subjects_df.iloc[:, 0]:
			subject_str = str(subject).strip()
			# Remove 'sub-' prefix if present
			if subject_str.startswith('sub-'):
				subject_str = subject_str[4:]
			subjects.append(subject_str)
		return subjects
	except Exception as e:
		print(f"Error reading subjects from {csv_file_path}: {e}")
		return []

# Read subjects from the CSV file specified above.
subjects = read_subjects_from_csv(SUBJECTS_CSV_PATH)

if not subjects:
	print("No subjects found in CSV file. Exiting.")
	sys.exit(1)

print(f"Found {len(subjects)} subjects in CSV file")

df = pd.DataFrame(columns = ["Subnum", "Total", "Subiculum", "CA1", "CA3", "CA4", "GC_ML_DG", "Fimbria"])
dictionary = {"Subiculum": 0, "CA1": 206, "CA3": 208, "CA4": 209, "GC_ML_DG": 0, "Fimbria": 212}

# Initialize dataframe with subjects from CSV
for s in subjects:
	df.loc[len(df.index)] = [s,0,0,0,0,0,0,0]

print(f"Processing {len(subjects)} subjects...")

# Process each ROI for all subjects
for roi in dictionary.keys():
	print(f"Processing {roi}...")
	df[roi] = df["Subnum"].apply(lambda s: sum_of_voxels(s, ROI = roi))

# Calculate total
df["Total"] = df[["Subiculum", "CA1", "CA3",  "CA4", "GC_ML_DG", "Fimbria"]].sum(axis = 1)

print("Saving results to CSV...")
save_csv()
print("Processing complete!") 