/**
 * Layout component that queries for data with Gatsby's useStaticQuery
 * components.
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React from "react";
import Helmet from "react-helmet";
import PropTypes from "prop-types";
import { useStaticQuery, graphql } from "gatsby";
import { withStyles, makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Img from 'gatsby-image';
import CityCard from './cityCard';
import "./layout.css";
import "./../utils/typography";
import Player from './player';
import Chart from './chart';
import Hidden from '@material-ui/core/Hidden';
import ImageOverlay from './imageOverlay';
import Header from './header';
import Footer from './footer';
import Typography from '@material-ui/core/Typography';

const CITIES = {
  chicago: "Chicago",
  dublin: "Dublin",
  london: "London",
  newjersey: "New Jersey",
  neworleans: "New Orleans",
  newyork: "New York",
  prague: "Prague",
};

const styles = {
    wrapper: {
      display: "flex",
      minHeight: "100vh",
      flexDirection: "column",
    },
    root: {
      width: "100%",
    }
};

class Layout extends React.Component  {
  constructor(props) {
    super(props);
    this.state = {
      data: {}
    };
  }
  componentDidMount() {
    fetch("https://pdi-service.voxel51.com/api/snapshots")
      .then(response => response.json())
      .then(json => {
        this.setState({ data: json["data"] })
      });
  }

  render() {
    const { classes, children, city } = this.props;
    const { data, height } = this.state;

    const setHeight = height => this.setState({height});

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
      <div className="cta-wrapper">

      <div className="cta">
        <h2 class="body_block__title">
  Physical Distancing Index
  </h2>
  <div class="body_block__text">
    Using our AI-powered video understanding capabilities, Voxel51 has generated the Physical Distancing Index (PDI) to track how the Coronavirus and subsequent policies and calls for physical distancing are impacting social behavior.
      <h3 class="force-pad-top6 force-pad-bot1"><span class="text-tertiary-on-dark">Stop the spread. Flatten the curve.</span></h3>
  </div>
</div>
</div>
<div className={classes.root}>
  <div className="contentBody">
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          {Object.keys(CITIES).sort().map(cityId => (
            <CityCard
              cityId={cityId}
              name={CITIES[cityId]}
              active={city == cityId}
              url={data && data[cityId] ? data[cityId]["url"] : undefined}
            />
          ))}
        </Grid>
        <Grid item xs={12} md={8}>
          <Hidden smDown>
          <Grid container spacing={4}>
            <Grid item md={12}>
              <Chart title="Physical Distancing Index (PDI)" city={city}
                // todo: use correct image url
                onClick={(_) => this.setState({src: _})}/>
            </Grid>
          </Grid>
          </Hidden>
            <Grid container spacing={4}>
              <Grid item xs={12} className="media-container">
                <Player city={city} height={height} setHeight={setHeight} />
                <ImageOverlay src={this.state.src} height={height} onClose={(e) => {
                  e.stopPropagation();
                  this.setState({src: null});
                }}/>
              </Grid>
            </Grid>
        </Grid>
      </Grid>
    </div>
    </div>
    <Footer/>
  </div>
  )
  }
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
  classes: PropTypes.node.isRequired,
}

export default withStyles(styles)(Layout)
