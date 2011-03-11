#!/bin/sh

# This script is just a wrapper around follow.js that lets us change uzbl's mode
# after a link is selected.

keys="$1"
shift

# if socat is installed then we can change Uzbl's input mode once a link is
# selected; otherwise we just select a link.
if ! which socat >/dev/null 2>&1; then
  printf "script @scripts_dir/follow.js \"@{follow_hint_keys} $keys\"\n" > "$UZBL_FIFO"
  exit
fi

result="$( printf "script @scripts_dir/follow.js \"@{follow_hint_keys} $keys\"\n" | socat - "unix-connect:$UZBL_SOCKET" )"
case $result in
    *XXXEMIT_FORM_ACTIVEXXX*)
        # a form element was selected
        printf "event FORM_ACTIVE\n" > "$UZBL_FIFO"
        ;;
    *XXXRESET_MODEXXX*)
        # a link was selected, reset uzbl's input mode
        printf "set mode=\n" > "$UZBL_FIFO"
        ;;
esac
