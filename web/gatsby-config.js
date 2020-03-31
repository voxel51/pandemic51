/**
 * Implement Gatsby's Node APIs in this file.
 *
 * See: https://www.gatsbyjs.org/docs/node-apis.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */

module.exports = {
  siteMetadata: {
    title: `Voxel51 // PDI: Measuring the Social Impact of the Coronavirus Pandemic`,
    description: `Live site monitoring the effect of physical distancing measures during the Coronavirus pandemic`,
    author: `Voxel51 Inc.`,
  },
  plugins: [
    `gatsby-plugin-offline`,
    `gatsby-plugin-react-helmet`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
    },
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `Voxel51 // PDI: Measuring the Social Impact of the Coronavirus Pandemic`,
        short_name: `Voxel51 // PDI`,
        start_url: `/`,
        background_color: `#ffffff`,
        theme_color: `#ff6d04`,
        display: `minimal-ui`,
        icon: `src/images/logo.png`, // This path is relative to the root of the site.
      },
    },
    {
      resolve: `gatsby-plugin-material-ui`,
      options: {
        stylesProvider: {
          injectFirst: true,
        },
      },
    },
    {
      resolve: `gatsby-plugin-typography`,
      options: {
        pathToConfigModule: "src/utils/typography.js",
      },
    },
    {
      resolve: `gatsby-plugin-prefetch-google-fonts`,
      options: {
        fonts: [
          {
            family: `Palanquin`,
            variants: [`400`, `600`, `700`, `800`],
          },
        ],
      },
    },
  ],
}
