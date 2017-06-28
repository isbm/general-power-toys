_osb()
{
  _script_commands=$(osc build x 2>&1 | sed -e 's/.*://g' | sed -e 's/ //g' | sed -e 's/,/ /g')

  local cur prev
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  COMPREPLY=( $(compgen -W "${_script_commands}" -- ${cur}) )

  return 0
}
complete -o nospace -F _osb osb
