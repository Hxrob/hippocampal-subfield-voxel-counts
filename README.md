<h1 align="center"> <img src="https://avatars.githubusercontent.com/u/6330653?s=280&v=4" alt="Freesurfer icon" style="height: 1em; vertical-align: middle;"> Hippocampal Subfield Voxel Count (Freesurfer) </h1>

This is a small Python script I used to pull left and right hippocampal subfield voxel counts from FreeSurfer/Nibabel label files. I originally wrote it for a research project that I presented at SOBP 2024, where I needed a straightforward way to summarize hippocampal subfield volumes across a list of study participants.

The script is not meant to be a full neuroimaging pipeline. It assumes the segmentation files have already been generated, and it just reads those label images, counts the voxels for the regions I needed, and saves the results into a CSV.

## What The Script Does

`sum_of_voxels.py` reads a CSV containing subject IDs, looks for each participant's left hippocampal/amygdala label file, and counts voxels for these regions:

- Subiculum
- CA1
- CA3
- CA4
- GC_ML_DG
- Fimbria

It also calculates a `Total` column by summing those subfield counts for each participant.

## How I Used It

For my neuroscience research study, I had a list of participants and already-processed MRI outputs. I used this script after preprocessing/segmentation to create a clean table of hippocampal subfield voxel counts that could be used in later statistical analyses.

The workflow was:

1. Create a CSV with one subject ID per row.
2. Point the script to the folder containing each participant's FreeSurfer output.
3. Run the script to count voxels for each hippocampal subfield label.
4. Use the output CSV in the next stage of analysis.

## Input Files

The subject list should be a simple CSV with one subject per line. The script accepts IDs with or without the `sub-` prefix.

Example:

```csv
001
002
003
```

The script expects each subject to have a label file with this structure:

```text
path/to/freesurfer/sub-001/mri/lh.hippoAmygLabels-T1-T2.v21.FS60.nativeSpace.nii.gz
```

If your files are named differently, update `LABEL_FILE_NAME` in the script.

## Setup

Install the Python packages used by the script:

```bash
pip install pandas numpy nibabel
```

Then update the user settings at the top of the script:

```python
SUBJECTS_CSV_PATH = "path/to/subject_ids.csv"
FREESURFER_DIR = "path/to/freesurfer"
OUTPUT_CSV_PATH = "path/to/volume_of_lh_hippocampus.csv"
```

## Running It

From the folder containing the script:

```bash
python "sum_of_voxels.py"
```

When it finishes, it writes a CSV with one row per subject and columns for each hippocampal subfield count.

## Notes

The voxel label values in the script come from the hippocampal/amygdala segmentation file I used for this project. If you use a different segmentation method, atlas, or label file, double-check that the numeric labels match your data before using the output.
