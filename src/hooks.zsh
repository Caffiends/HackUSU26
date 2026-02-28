# --- $CODENAME System-Wide Hooks ---
_PYTHON="/opt/dropship/venv/bin/python3"
_MAIN="/opt/dropship/logiccheck.py"

eval() {
    # Get the current buffer
    local user_input="$BUFFER"

    # If the buffer is empty, accept it and move on
    if [[ -z "$user_input" ]]; then
        zle accept-line
        return
    fi

    # Python returns the path to the alternate binary or "PASS"
    local action=$("$_PYTHON" "$_MAIN" "$user_input")

    if [[ "$action" == "PASS" ]]; then
        # Normal command: pass on
        zle accept-line
    else
        # Hijack: Clear the prompt line and run the alternate binary instead
        BUFFER=""
        zle accept-line
        eval "$action"
    fi
}

# Register the widget and bind it to the Enter key
zle -N eval
bindkey '^M' eval
