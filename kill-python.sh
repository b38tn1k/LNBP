#!/bin/bash

# Find Flask processes
flask_processes=$(ps aux | grep 'python' | awk '{print $2}')

# Check if any Flask processes are running
if [ -z "$flask_processes" ]; then
    echo "No Flask processes found."
else
    echo "Found Flask processes: $flask_processes"

    # Kill each Flask process
    for pid in $flask_processes; do
        echo "Killing Flask process with PID: $pid"
        kill -9 $pid
    done

    echo "All Flask processes have been terminated."
fi
