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
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Img from 'gatsby-image';
import CityCard from './cityCard';
import "./layout.css"
import "./../utils/typography";
import ClapprPlayer from './clappr';
import Chart from './chart';
import Hidden from '@material-ui/core/Hidden';
import SEO from './seo';
import Header from './header';

const useStyles = makeStyles((theme) =>
  createStyles({
    root: {
      flexGrow: 1,
      overflow: "hidden",
      padding: "2rem 10rem"
    },
    paper: {
      padding: theme.spacing(2),
      textAlign: 'center',
      color: theme.palette.text.secondary,
      background: "transparent",
      boxShadow: "none",
      border: "none",
      margin: 32
    },
  }),
);

const Layout = ({ children, city }) => {
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
            ...GatsbyImageSharpFluid_noBase64
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
    <>
      <Header/>
    <div className={classes.root}>
      <Grid container spacing={8}>
        <Grid item xs={12} md={3}>
          <CityCard cityId="newyork" name="New York" active={city}/>
          <CityCard cityId="miami" name="Miami" active={city}/>
          <CityCard cityId="chicago" name="Chicago" active={city}/>
          <CityCard cityId="sanfrancisco" name="San Francisco" active={city}/>
          <CityCard cityId="seattle" name="Seattle" active={city}/>
        </Grid>
        <Grid item xs={12} md={9}>
          <Grid container spacing={8}>
            <Grid item xs={12}>
              <Card square>
                Explanatory Text
              </Card>
            </Grid>
            <Hidden smDown>
              <Grid item md={12}>
                <Grid container spacing={8}>
                  <Grid item md={6}>
                    <Chart title="Social Distancing Index (SDI)"/>
                  </Grid>
                  <Grid item md={6}>
                    <ClapprPlayer source="https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8" />
                  </Grid>
                </Grid>
              </Grid>
            </Hidden>
          </Grid>
        </Grid>
      </Grid>
    </div>
  </>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
