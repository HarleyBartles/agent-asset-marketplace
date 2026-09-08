pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript skill-called superpowers-plus:finishing-a-development-branch
    check-transcript tool-not-called git-push
}
