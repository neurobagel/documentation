# Contributing Guidelines

*We're so excited that you're interested in contributing to Neurobagel!* :partying_face:

We appreciate all contributions, and hope that the below guidelines will make it as easy as possible for you to contribute to the [Neurobagel codebase](https://github.com/neurobagel) and to ensure your contribution can be easily integrated.

## Contributing through GitHub

In order to contribute to Neurobagel, you'll need to set up a [GitHub](https://github.com/) account and sign in.
Here are some [instructions](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) to help you get started.

## Identifying an issue to contribute to

The best way to get started contributing is to explore the list of open issues in one of our [GitHub repositories](https://github.com/orgs/neurobagel/repositories).
(For example, see the [open issues for the Neurobagel API](https://github.com/neurobagel/api/issues).)

When you are ready to contribute, we welcome you to join the conversation through one of these issues,
or open a new issue referencing a change you would like to see or contribute.
Ensuring that a relevant issue is open before you start contributing code is important because it allows others in the project to discuss your idea and tell you where your contribution would be the most helpful.

- **If the issue you want to work on already exists**:
Comment on the open issue to indicate you would like to work on it, along with any clarification/implementation questions you have
    - If someone is already [assigned to the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/assigning-issues-and-pull-requests-to-other-github-users), the task is actively being worked on and a solution will soon be proposed. Feel free to share some helpful resources or pointers that may be interesting to the person who is working the issue, and/or check back in a couple of days.

- **If the issue you want to work on does not exist**:
Open a new issue describing your proposed change and why it is necessary/beneficial.
The more detail here, the better!

This allows members of the Neurobagel developer team to confirm that you will not be overlapping with currently active work and that everyone is on the same page about the task to be accomplished.

If you would like to contribute but are not sure where to start, we recommend looking for open issues with the following labels:

![good first issue](https://img.shields.io/github/labels/neurobagel/planning/good%20first%20issue)
*Issue that is good for a new or beginner contributor, as it does not involve a steep learning curve or advanced understanding of the codebase.
(Please note: if you're a seasoned contributor, we would appreciate if you could select a different issue to work on to keep these available for less experienced folks!)*

![PR welcome](https://img.shields.io/github/labels/neurobagel/planning/PR%20welcome)
*Issue that is not an internal priority, but external pull requests to address it are welcome.*

![quick fix](https://img.shields.io/github/labels/neurobagel/planning/quick%20fix):
*Issue that should involve minimal planning or implementation work, given an understanding of the relevant code.*

## Making a change

All Neurobagel issues are expected to be addressed through [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

As an external contributor, the process you would follow to make your [proposed changes](#identifying-an-issue-to-contribute-to) should look something like this:

### 1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the relevant Neurobagel repository to your profile

### 2. [Clone](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#cloning-your-forked-repository) your fork of the Neurobagel repository to your local machine

To keep up with changes in the Neurobagel repository while you work and avoid merge conflicts later on, make sure to:

- [Add the "upstream" Neurobagel repository as a remote](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#configuring-git-to-sync-your-fork-with-the-upstream-repository) to your locally cloned repository
- [Keep your fork up to date](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-branch-from-the-command-line) with the upstream repository

### 3. Set up a development environment

Refer to the README of the Neurobagel repository you are contributing to for instructions on setting up a development environment so you can test any local code changes you make.
Note that the steps to set up a development environment (usually under a "Local installation", "Manual installation", or "Development environment" section) are generally different than those used to install the tool purely as a user, which usually appears at the top of the README.

For example, for the [Neurobagel CLI](https://github.com/neurobagel/bagel-cli):

- ["Development" mode installation steps](https://github.com/neurobagel/bagel-cli?tab=readme-ov-file#installation)
- [Normal (non-development mode) installation steps](https://github.com/neurobagel/bagel-cli?tab=readme-ov-file#development-environment)

#### Follow repository code style

Most Neurobagel repositories use tools to apply automatic code formatting and linting according to the project's code style,
which are typically configured (but not automatically enabled) in the development environment for these repositories.
At this point, please follow the repository instructions to set up these tools before you begin your work to ensure your contribution matches the existing code.

For example, our repositories written in Python have [pre-commit](https://pre-commit.com/) configured for this purpose.

To tell pre-commit to run on any local changes you make, run the following from the repository root of your local clone:

```bash
pre-commit install
```

Now, a number of code linters and formatters will run automatically when you attempt to make a commit, which will keep your changes consistent with the rest of the codebase.

### 4. [Create a new branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) to make the proposed changes

Please consider using descriptive branch names. Some examples:

- `<username>/<issue-identifier>` (`jsmith/fix-1234`)
- `<username>/<brief-change-title>` (`jsmith/add-logging`, `jsmith/enh/add-logging`)

Once you are satisfied with your local changes, [add, commit, and push](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository#adding-a-file-to-a-repository-using-the-command-line) them to your branch on your forked repository on GitHub.

### 5. [Open a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)

See the below sections for information on [how to submit your pull request](#pull-request-guidelines) and [what to expect in a pull request review](#pull-request-reviews).

## Pull request guidelines

When you first open a pull request, you should automatically see a template in the pull request body that looks something like [this](https://github.com/neurobagel/.github/blob/main/.github/pull_request_template.md?plain=1) that you can fill out.
The template is designed to make it easier for maintainers to review your pull request, but feel free to add any additional information that you feel is useful or necessary.

Pull request titles should begin with a descriptive prefix (e.g., "[ENH] Implement check for presence of a session ID column"):

- `[ENH]:` Feature improvements or additions
- `[REF]:` Refactoring existing code
- `[TST]`: Updating or adding a test
- `[CI]`: Automation-related changes
- `[MNT]`: General maintenance not covered by `[REF]`, `[TST]`, or `[CI]`
- `[INF]`: Software or graph infrastructure-related changes
- `[FIX]`: Bug fixes
- `[MODEL]`: Updates or changes related to the Neurobagel data model
- `[DOC]`: Documentation-only changes to a code repo (READMEs, within-code documentation, etc.)
    - Exception: changes to the [`documentation`](https://github.com/neurobagel/documentation) repo should use one of the below PR prefixes instead of `[DOC]`

### Pull requests to the [`documentation`](https://github.com/neurobagel/documentation) repo

In PRs to the [Neurobagel documentation](https://github.com/neurobagel/documentation), using the `[DOC]` title prefix is discouraged as it is too broad.
Instead, for documentation content changes, the following prefixes can be used to specify the nature of the change:

- `[ENH]`: Updating or adding new documentation
- `[REF]`: Simplifying or restructuring documentation (i.e., pages, sections, paragraphs)
- `[FIX]`: Fixing errors in the documentation

## Pull request reviews

A maintainer will review each PR and may provide comments or suggestions for you to address.

Neurobagel PR reviews may use the following emoji signifiers:

:cook:: Ready to merge or approved without suggestions

:cherries:: Some optional/suggested changes that could be nice to have but are not required to merge

If (required) changes are requested, please re-request a review from the reviewer once the comments have been addressed.

### When your pull request is approved

If you **do not have write access to the repository**: the reviewing Neurobagel maintainer is responsible for merging the PR.

If you **have write access to the repository**: the PR author is responsible for merging the PR.

## Have a question about contributing?

At any point during a contribution,
please do not hesitate to [mention](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#mentioning-people-and-teams) one of the [core maintainers](./team.md#developers) if you have a question or need further guidance,
in either the issue or pull request.

If you have ideas for improving this page, please help us improve it by [opening an issue](https://github.com/neurobagel/documentation/issues) :tada:.
