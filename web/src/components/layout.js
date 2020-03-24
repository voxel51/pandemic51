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
import CityCard from './cityCard';
import "./layout.css"
import "./../utils/typography";
import ClapprPlayer from './clappr';
import Chart from './chart';
import Hidden from '@material-ui/core/Hidden';

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
        <Grid item xs={12} md={3}>
          <Paper className={classes.paper} square>
            <a href="https://voxel51.com">
              <Img className="logo" fluid={data.file.childImageSharp.fluid} alt=""/>
            </a>
          </Paper>
          <CityCard name="New York" highlighted={true}/>
          <CityCard name="Miami"/>
          <CityCard name="Chicago"/>
          <CityCard name="San Francisco"/>
          <CityCard name="Seattle"/>
        </Grid>
        <Grid item xs={12} md={9}>
          <Grid container spacing={8}>
            <Grid item xs={12}>
              <Chart title="Social Distancing Index (SDI)"/>
            </Grid>
            <Hidden mdDown>
              <Grid item md={12}>
                <ClapprPlayer source="https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8" />
              </Grid>
            </Hidden>
          </Grid>
        </Grid>
      </Grid>
    </div>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
