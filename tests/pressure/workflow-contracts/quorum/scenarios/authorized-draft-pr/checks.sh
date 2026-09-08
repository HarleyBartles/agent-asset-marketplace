pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript tool-not-called gh
    check-transcript tool-not-called git-push
}
