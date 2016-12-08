_git_delete_branch()
{
  # All without current
  _branch_to_delete=$(git branch | grep -v '\*')

  local cur prev
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  COMPREPLY=( $(compgen -W "${_branch_to_delete}" -- ${cur}) )

  return 0
}
complete -o nospace -F _git_delete_branch git-delete-branch

