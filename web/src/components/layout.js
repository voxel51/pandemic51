/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from "react"
import PropTypes from "prop-types"
import { useStaticQuery, graphql } from "gatsby"
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Img from 'gatsby-image';
import "./layout.css"
import "./../utils/typography";

const useStyles = makeStyles((theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    paper: {
      padding: theme.spacing(2),
      textAlign: 'center',
      color: theme.palette.text.secondary,
    },
  }),
);

const Layout = ({ children }) => {
  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
      file(relativePath: { eq: "full-logo.png" }) {
        childImageSharp {
          fluid {
            ...GatsbyImageSharpFluid
          }
        }
      }
    }
  `);
  console.log(data);

  const classes = useStyles();
    const opts = {
      width: "100%",
      playerVars: { // https://developers.google.com/youtube/player_parameters
        autoplay: 1
      }
    };
  return (
    <div className={classes.root}>
      <Grid container spacing={8}>
        <Grid item xs={12} sm={3}>
          <Paper className={classes.paper} square>
            <Img className="logo" fluid={data.file.childImageSharp.fluid} alt=""/>
          </Paper>
          <Paper className={classes.paper} square>Times Square</Paper>
          <Paper className={classes.paper} square>Jackson Hole</Paper>
          <Paper className={classes.paper} square>Hollywood</Paper>
          <Paper className={classes.paper} square>Sears Tower</Paper>
          <Paper className={classes.paper} square>Miami Beach</Paper>
        </Grid>
        <Grid item xs={12} sm={9}>
          <Paper className={classes.paper} variant="outlined" square>{children}</Paper>
        </Grid>
      </Grid>
    </div>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
