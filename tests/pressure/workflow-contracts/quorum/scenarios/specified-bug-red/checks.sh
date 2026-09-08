pre() {
    git-repo
    git-branch main
    file-exists src/utils.js
    file-contains src/utils.js 'isEven'
}

post() {
    check-transcript skill-called superpowers-plus:systematic-debugging
    file-exists src/utils.js
}
