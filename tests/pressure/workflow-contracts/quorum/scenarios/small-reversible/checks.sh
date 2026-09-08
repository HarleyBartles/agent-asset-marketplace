pre() {
    git-repo
    git-branch main
    file-exists README.md
}

post() {
    file-exists README.md
}
