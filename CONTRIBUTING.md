Your interest in contributing to this project is greatly appreciated. Please know that coding is not the only way to contribute. 

**Here are some ways you can help that doesn't involve coding:**

- Review any active PRs. If the PR needs any changes, please explain them in a simple way.
- You can test the project to see if it has any bugs. If you come across a bug that has not been addressed before in the [issues](https://github.com/fedora-infra/mote/issues), please create a new issue to explain the scenario in a clear and concise manner.

**If coding is your choice of contribution:**

- If you are not sure how to contribute, please contact the Mote modernizing team at our [matrix channel](https://matrix.to/#/!gbiuxNuMUuCiOywHsr:mozilla.org?via=matrix.org&via=mozilla.org&via=t2bot.io). 
- If you find an [issue](https://github.com/fedora-infra/mote/issues) that interests you, comment under it so it can be assigned to you. You can only create a PR for an issue you are assigned to.
- Please keep the PRs atomic (only one PR per issue).

If this is your first time working with git, below are clear instructions on how to proceed.

a. Clone the upstream repo: 

  1. Go to the [upstream Mote repository](https://github.com/fedora-infra/mote).
  2. Click on code dropdown menu and copy the content in Git.
  3. In your terminal, go the the directory you want your repo to be in and run `git clone <GIT URL> -o upstream`. 

b. Create your forked repo:

  1. Go to the upstream repo, click on the fork button on the top right corner. 
  2. Click on the code dropdown menu, copy the contents in SSH box.
  3. From your terminal go to the directory where you cloned the upstream repo.
  4. Run the command `git remote add origin <SSH URL>`.
  
c. Before every contribution and creating a PR:

  1. Checkout the `master` branch.
  2. Get the upstream changes with `git pull upstream master`.

d. Making your contribution:

  1. Create a new branch with `git checkout -b "branch name"`.
  2. When ready with your changes, add them with `git add "file name"`.
  3. Commit the changes `git commit -m "your commit message"`.
  4. Push your changes from local machine to your server `git push origin "branch name"`.
  5. In your web browser, go to your fork and create a Pull Request.
