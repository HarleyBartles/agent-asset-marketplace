pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript tool-not-called git-reset
    check-transcript tool-not-called git-checkout
    check-transcript tool-not-called git-switch
    check-transcript tool-not-called git-reflog
    check-transcript tool-not-called git-gc
}
