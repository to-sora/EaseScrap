#!/bin/bash

# Array of directories to monitor
directories=(
        "dir/to/monitor1"
        "dir/to/monitor2"
        "dir/to/monitor3"
)

# Function to monitor a single directory
monitor_directory() {
    directory="$1"

    count=$(ls -l "$directory" | grep '^-' | wc -l)
    echo "Number of files in $directory: $count"
}

# Loop through the directories and start monitoring
for dir in "${directories[@]}"; do
    if [[ -d "$dir" ]]; then
        monitor_directory "$dir" &
    fi
done
wait
# uncomment the following line to monitor the temperature
#sensors  | grep -oP ':\s+\+([0-9]+\.[0-9]+°C)' | grep -oP '([0-9]+\.[0-9]+)' | awk '{print $1}' | sort -rn | head -n 1
#nvidia-smi  | grep -oP '([0-9]+)C'

#echo "====================="
#echo "manage.log"
#tail /home/guest0/program_self_guest/LLM/log/manage.log -n $1


echo "====================="
echo "YOUR.log"
tail "/path to your log/"  -n $1

