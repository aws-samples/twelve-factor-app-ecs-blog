## Developing Applications on ECS with Fargate using the Twelve-Factor App Methodology

This GitHub repository hosts the artifacts for the AWS Containers blog on developing Twelve Factor Apps on ECS using Fargate. The Twelve-Factor-App-Stack.yml AWS Cloudformation template launches the reference solution in your AWS account. The other sources are used by the Twelve-Factor-App-Stack.yml AWS Cloudformation template to setup an AWS CodeCommit repository in the AWS account that launches the stack. The CodeCommit repository serves as the starting point in the AWS CodePipeline deployment pipeline. Any updates to the application code are best done in the AWS CodeCommit repository within the AWS account that launches this solution. Code should only be modified in this GitHub repository if the bootstrap application code for the reference solution must change. See [CONTRIBUTING](CONTRIBUTING.md) for instructions on how to submit a pull request for this repository

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
