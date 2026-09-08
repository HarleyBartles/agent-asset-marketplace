pre() {
    git-repo
    git-branch main
}

post() {
    file-exists notes.md
}
