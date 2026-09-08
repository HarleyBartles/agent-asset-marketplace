pre() {
    git-repo
    git-branch fixture-finish
}

post() {
    check-transcript skill-called superpowers-plus:finishing-a-development-branch
    check-transcript tool-not-called git-push
}
