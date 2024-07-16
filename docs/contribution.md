# Contribution

[Source on Github](https://github.com/daveisagit/blocksets)

- At the moment it is early days so whilst the foundations are forming I am only
  inviting comments which can be given via [github issues](https://github.com/daveisagit/blocksets/issues)

## Deployment Notes

If using VS Code make sure you have _Follow Tags When Sync_ in settings set to true.

`"git.followTagsWhenSync": true`

If you don't then github actions will simply just get `refs/heads/main` in
`github.ref` and not the expected `refs/tags/`.

Meaning the condition `if: startsWith(github.ref, 'refs/tags/')` fails and there
is no deployment

Install `bump-my-version` and run `bump-my-version bump <version_part>` to

- update the version in `pyproject.toml`
- add a tag commit

Once pushed/sync'd, github actions will

- run test coverage and upload results to codecov
- deploy to pypi

Use the following either of (which have been setup as VS Code tasks too)

- `bump-my-version bump patch`
- `bump-my-version bump minor`
- `bump-my-version bump major`
