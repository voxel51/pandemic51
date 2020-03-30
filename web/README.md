# Pandemic51 web client

Web client for the Pandemic51 project, built using
[Node.js](https://nodejs.org) and [Gatsby](https://www.gatsbyjs.org).


## Steps to Setup Environment

Install [nvm/Node.js for Gatsby](https://www.gatsbyjs.org/tutorial/part-zero/).
[Here is more information about Node.js](https://medium.com/stackfame/how-to-update-node-js-to-latest-version-linux-ubuntu-osx-windows-others-105749e90040).
You should refer to these links for more detail.

The basis steps are:

```bash
sudo apt-get upgrade
sudo apt-get install curl
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash

# manipulate your bash environment per the instructions in your terminal

nvm install 12.8.0
```

Install [yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable).
Do not just execute `sudo apt install yarn` as this will install a different
version of it.

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
```

Alternatively, if you're using nvm, you can run `npm install -g yarn` to
install yarn in your current node environment (without root access).

In `./web` run `yarn install`. This will install dependencies, including the
Gatsby CLI, which you can run with `yarn` (below) or directly using
[`npx`](https://www.npmjs.com/package/npx).


## Developing and Running

In `./web` run `yarn run develop` (or just `yarn develop`). This runs
`gatsby develop`, which is basically is a continuous build-process with an
integrated web-server. You can edit the files/site directly on the disk and it
will detect changes and go.


## Copyright

Copyright 2020, Voxel51, Inc.<br>
voxel51.com
