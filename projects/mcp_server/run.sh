#!/bin/bash

# Name of the virtual environment directory
env_dir=".venv"

# List of scripts to run (python modules/files)
SCRIPTS=("client.py" "app.py" "main.py")
STREAMLIT_APP="todo_ui.py"

# Function to activate venv
activate_venv() {
    if [ ! -d "$env_dir" ]; then
        echo "Virtual environment not found. Creating one in $env_dir..."
        python3 -m venv "$env_dir"
    fi
    source "$env_dir/bin/activate"
}

# Function to start all scripts with nohup
start_all() {
    activate_venv
    for script in "${SCRIPTS[@]}"; do
        # Don't start if already running
        if pgrep -f "$script" > /dev/null; then
            echo "$script is already running."
        else
            echo "Starting $script ..."
            nohup python "$script" > "${script}.log" 2>&1 &
            echo $! > "${script}.pid"
        fi
    done

    # Start Streamlit app
    if pgrep -f "streamlit run $STREAMLIT_APP" > /dev/null; then
        echo "$STREAMLIT_APP is already running."
    else
        echo "Starting Streamlit app $STREAMLIT_APP ..."
        nohup streamlit run "$STREAMLIT_APP" > "${STREAMLIT_APP}.log" 2>&1 &
        echo $! > "${STREAMLIT_APP}.pid"
    fi
}

# Function to kill all running scripts
kill_all() {
    for script in "${SCRIPTS[@]}"; do
        if [ -f "${script}.pid" ]; then
            pid=$(cat "${script}.pid")
            if kill -0 "$pid" 2>/dev/null; then
                echo "Killing $script (PID $pid)..."
                kill "$pid"
            fi
            rm -f "${script}.pid"
        else
            pkill -f "$script"
        fi
    done

    # Kill Streamlit app
    if [ -f "${STREAMLIT_APP}.pid" ]; then
        pid=$(cat "${STREAMLIT_APP}.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo "Killing $STREAMLIT_APP (PID $pid)..."
            kill "$pid"
        fi
        rm -f "${STREAMLIT_APP}.pid"
    else
        pkill -f "streamlit run $STREAMLIT_APP"
    fi
}

# Usage info
usage() {
    echo "Usage: $0 {start|kill|restart}"
    exit 1
}

# Main logic
case "$1" in
    start)
        start_all
        ;;
    kill)
        kill_all
        ;;
    restart)
        kill_all
        sleep 2
        start_all
        ;;
    *)
        usage
        ;;
esac