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
    <div className={classes.root}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={3}>
          <CityCard cityId="chicago" name="Chicago" active={city}/>
          <CityCard cityId="dublin" name="Dublin" active={city}/>
          <CityCard cityId="london" name="London" active={city}/>
          <CityCard cityId="newjersey" name="New Jersey" active={city}/>
          <CityCard cityId="neworleans" name="New Orleans" active={city}/>
          <CityCard cityId="newyork" name="New York" active={city}/>
          <CityCard cityId="prague" name="Prague" active={city}/>
        </Grid>
        <Grid item xs={12} md={9}>
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Card square>
                        <CardContent>
                          <Typography variant="h5" component="h3">
                            Header
                          </Typography>
                          <Typography className={classes.pos} color="textSecondary">
                            Subheader
          </Typography>
          <Typography variant="body2" component="p">
            Content
          </Typography>
        </CardContent>

              </Card>
            </Grid>
            <Grid item md={6}>
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
