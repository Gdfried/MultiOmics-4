# Set base directory
base_dir="/home/ilants/Documents/data_from_gdc"
data_dir="$base_dir/data"

# Create download log directory if it doesn't exist
mkdir -p "$base_dir/download_log"

# Start total download timer
total_download_start_time=$(date +%s)

# Set gdc script and manifest paths
gdc_script="/home/ilants/Documents/gdc-client_v1.6.1_Ubuntu_x64/gdc-client"
manifest_dir="$base_dir/manifests"
manifest="$manifest_dir/deluted_no10_gdc_manifest.2024-07-24_open.txt"
downloaded_from_manifest="$data_dir/$(basename $manifest)"

mkdir -p "$downloaded_from_manifest"

# Log the initialization of the download
echo "Initialising download of images from: $manifest_dir/$manifest" > "$base_dir/download_log/$(basename $manifest)"
echo "Initialising download of images from: $manifest_dir/$manifest"

# Start manifest download timer
mani_download_start_time=$(date +%s)

# Check disk space usage of the data directory before download
disk_space_before=$(du -s "$data_dir" | awk '{print $1}')

# Execute the download command
$gdc_script download -d "$downloaded_from_manifest" -m "$manifest" | grep -v -E "^[[:space:]]*$|[1-9][0-9]?% \[|N/A% \[" >> "$base_dir/download_log/$(basename $manifest)"
# $gdc_script download -d "$data_dir" -m "$manifest"

# End manifest download timer
mani_download_end_time=$(date +%s)

# Check disk space usage of the data directory after download
disk_space_after=$(du -s "$data_dir" | awk '{print $1}')

# Calculate runtime and disk space used
runtime=$((mani_download_end_time - mani_download_start_time))
disk_space_used=$((disk_space_after - disk_space_before))

# Log the runtime and disk space used
echo "Runtime of images from $manifest_dir/$manifest was: $runtime seconds" >> "$base_dir/download_log/$(basename $manifest)"
echo "Disk space used for download: $disk_space_used KB" >> "$base_dir/download_log/$(basename $manifest)"
echo "Runtime of images from $manifest_dir/$manifest was: $runtime seconds"
echo "Disk space used for download: $disk_space_used KB"
echo "Log was written to: $base_dir/download_log/$(basename $manifest)"
