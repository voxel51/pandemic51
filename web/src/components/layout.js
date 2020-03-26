/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from "react"
import Helmet from "react-helmet"
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
import Footer from './footer';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) =>
  createStyles({
    wrapper: {
      display: "flex",
      minHeight: "100vh",
      flexDirection: "column"
    },
    root: {
      flexGrow: 1,
      margin: "4rem auto",
      maxWidth: "1040px",
      width: "100%"
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
    <div className={classes.wrapper}>
      <Helmet>
        <meta name="referrer" content="no-referrer"/>
      </Helmet>
      <Header/>
      <div className="cta">
        <h2 class="body_block__title">
  Social Distancing Index
  </h2>
  <div class="body_block__text">
    Using our AI-powered video understanding capabilities, Voxel51 has generated the Social Distancing Index (SDI) to track how the Coronavirus and subsequent policies and calls for social distancing are impacting social behavior.
      <h3 class="force-pad-top6 force-pad-bot1"><span class="text-tertiary-on-dark">Stop the spread. Flatten the curve.</span></h3>
  </div>
    </div>
    <div className={classes.root}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <CityCard cityId="chicago" name="Chicago" active={city}/>
          <CityCard cityId="dublin" name="Dublin" active={city}/>
          <CityCard cityId="london" name="London" active={city}/>
          <CityCard cityId="newjersey" name="New Jersey" active={city}/>
          <CityCard cityId="neworleans" name="New Orleans" active={city}/>
          <CityCard cityId="newyork" name="New York" active={city}/>
          <CityCard cityId="prague" name="Prague" active={city}/>
        </Grid>
        <Grid item xs={12} md={8}>
          <Grid container spacing={4}>
            <Grid item md={12}>
                <ClapprPlayer city={city} />
            </Grid>
          </Grid>
          <Hidden smDown>
            <Grid container spacing={4}>
              <Grid item xs={12}>
              <Chart title="Social Distancing Index (SDI)"/>
              </Grid>
            </Grid>
          </Hidden>
        </Grid>
      </Grid>
    </div>
    <Footer/>
  </div>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
