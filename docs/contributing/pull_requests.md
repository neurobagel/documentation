# Pull requests

When submitting a pull request, titles should begin with a descriptive prefix (e.g., "[ENH] Implement check for presence of a session ID column").

- `[ENH]:` Feature improvements or additions
- `[REF]:` Refactoring existing code
- `[TST]`: Updating or adding a test
- `[CI]`: Automation-related changes
- `[MNT]`: General maintenance not covered by `[REF]`, `[TST]`, or `[CI]`
- `[INF]`: Software or graph infrastructure-related changes
- `[FIX]`: Bug fixes
- `[MODEL]`: Updates or changes related to the Neurobagel data model
- `[DOC]`: Documentation-only changes to a code repo (READMEs, within-code documentation, etc.) 
_Note: do not use for changes to the [`neurobagel/documentation`](https://github.com/neurobagel/documentation) repo_. See below for PR prefixes for the documentation repo.

## Changes to documentation pages
In PRs for the [Neurobagel documentation](https://github.com/neurobagel/documentation), using the `[DOC]` title prefix is discouraged as it is too broad. 
Instead, for documentation content changes, the following prefixes can be used to specify the nature of the change:

- `[ENH]`: Updating or adding new documentation
- `[REF]`: Simplifying or restructuring documentation (i.e., pages, sections, paragraphs)
- `[FIX]`: Fixing errors in the documentation

## Pull request reviews
A developer will review each PR and may provide comments or suggestions for the PR author to address.

Neurobagel PR reviews may use the following emoji signifiers:

:cook:: Ready to merge or approved without suggestions

:cherries:: Some optional/suggested changes that could be nice to have but are not required to merge

If (required) changes are requested, the PR author should re-request a review from the reviewer once the comments have been addressed.
