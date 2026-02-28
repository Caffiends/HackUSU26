precmd() {
    last_command=$(fc -ln -1)
    cmd=${last_command%% *}

    [[ -z "$cmd" ]] && return
    [[ "$cmd" == "typo-wrapper" ]] && return
    [[ "$cmd" == "typo-log-correct" ]] && return

    typo-log-correct "$cmd"
}

command_not_found_handler() {
    typo-wrapper "$@"
}
