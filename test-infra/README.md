# Integration test infrastructure

This project defines long-lived, shared infrastructure for integration testing.
It uses a local OpenTofu backend, with the state committed to Git.


## Purpose

- Common infrastructure (e.g., S3 buckets, IAM role) for cloud-based test automation
- Simple, low-collaboration setup (mostly a single maintainer)
- Reproducibility and version tracking


## Why check in state?

This is a rare exception to normal best practices:

- No secrets or sensitive data are stored in state
- The infrastructure is stable and rarely changed
- The setup is primarily maintained by a single person
- Having state in Git helps track and reproduce test environment changes

**Do not use this pattern for production infrastructure.**


## Requirements

- [OpenTofu](https://opentofu.org/) installed
- [Terragrunt](https://terragrunt.gruntwork.io/) installed
- AWS credentials configured (e.g., via environment variables or `~/.aws/credentials`)


## Usage

```sh
cd test-infra
terragrunt init
terragrunt apply
```


## Infrastructure versioning

We use Git tags to mark changes to the infrastructure. Use the following
pattern:

```sh
git tag -a test-infra-v1.2 -m "Describe what changed"
git push origin infra-v1.2
```

This helps track which version of infrastructure was active for integration
testing or rollbacks.
