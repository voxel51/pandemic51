# Instructions

The web client for this application is based on Gatsby.

## Resources

- [NodeJS](https://nodejs.org)
- [Gatsby](https://www.gatsbyjs.org/)


## Steps to Setup Environment

Install [nvm/nodejs for gatsby](https://www.gatsbyjs.org/tutorial/part-zero/) [Here is more information about nodejs](https://medium.com/stackfame/how-to-update-node-js-to-latest-version-linux-ubuntu-osx-windows-others-105749e90040)
You should refer to the links above for more detail.  Basic steps
```
sudo apt-get upgrade
sudo apt-get install curl
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash
# manipulate your bash environment per the instructions in your terminal
nvm install 12.8.0
```


Install [yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable)
Do not just execute `sudo apt install yarn` as this will install a different version of it.
```
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
```

In `./web` run `yarn install`.

Install the gatsby client: `npm install -g gatsby-cli`


## Developing and Runnign

In `./web` run `gatsby develop`.  This basically is a continuous build-process with an integrated web-server.  You can edit the files/site directly on the disk and it will detect changes and go.

