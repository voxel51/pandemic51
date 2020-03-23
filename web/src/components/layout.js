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
import Container from '@material-ui/core/Container';
import MediaCard from "./videoCard";
import Header from "./header"
import YouTube from 'react-youtube';
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
    }
  `);

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
          <Paper className={classes.paper} square>Times Square</Paper>
          <Paper className={classes.paper} square>Jackson Hole</Paper>
          <Paper className={classes.paper} square>Hollywood</Paper>
          <Paper className={classes.paper} square>Sears Tower</Paper>
          <Paper className={classes.paper} square>Miami Beach</Paper>
        </Grid>
        <Grid item xs={12} sm={9}>
          <video
              data-html5-video
              poster="https://static.skylinewebcams.com/_3155001280.jpg"
              preload="metadata"
              playsInline
              src="blob:https://www.skylinewebcams.com/d409fd8b-b574-4d2a-8514-2e4a7d6eac38">
            </video>
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
