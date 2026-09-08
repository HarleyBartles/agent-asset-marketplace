pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript tool-not-called git-reset
    check-transcript tool-not-called git-checkout
}
