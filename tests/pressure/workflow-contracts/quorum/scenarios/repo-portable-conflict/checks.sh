pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript skill-called superpowers-plus:repo-worker-base
}
