/**
 * Layout component that queries for data with Gatsby's useStaticQuery
 * components.
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React from "react"
import Helmet from "react-helmet"
import PropTypes from "prop-types"
import { useStaticQuery, graphql } from "gatsby"
import { withStyles, makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import SB from './sb';
import PD from './pd';
import CityCard from './cityCard';
import "./layout.css"
import "./../utils/typography"
import Player from "./player"
import Chart from "./chart"
import Hidden from "@material-ui/core/Hidden"
import ImageOverlay from "./imageOverlay"
import Header from "./header"
import Footer from "./footer"
import Typography from "@material-ui/core/Typography"

const styles = {
  wrapper: {
    display: "flex",
    minHeight: "100vh",
    flexDirection: "column",
  },
  root: {
    width: "100%",
  },
}

class Layout extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      urls: {},
    }
  }
  componentDidMount() {
    fetch("https://pdi-service.voxel51.com/api/snapshots")
      .then(response => response.json())
      .then(json => {
        this.setState({ urls: json["data"] })
      })
  }

  render() {
    const { classes, children, city } = this.props;
    const { urls, height } = this.state;

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
<div class="bg-header-dark-fancy2 body_part bg-dark-primary body_block--centerfull force-pad-bottom0">
  <h2 class="body_block__title">
      Measuring the Social Impact of the <br/>Coronavirus Pandemic
  </h2>
  <div class="body_block__text" align="center">
    Voxel51 is tracking the impact of the coronavirus global pandemic on social behavior, using a metric we developed called the Voxel51 Physical Distancing Index (PDI). The PDI is computed using our cutting-edge computer vision methods from live video streams and tracks how coronavirus news impacts real-time human activity around the world.
  </div>
</div>

<div class="body_part bg-light-primary body_block--centerfull">
  <div class="body_block__text" align="center">
    Click on live video streams from some of the world’s most visited streets to see how different cities react to physical distancing. Hover over the graph to view a day-by-day timeline of the average daily number of people on the street (Voxel51’s PDI metric) and social behaviors over time.
  </div>
</div>
<div className={classes.root}>
  <div className="contentBody">
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <CityCard cityId="chicago" name="Chicago" active={city} url={urls["chicago"]}/>
          <CityCard cityId="dublin" name="Dublin" active={city} url={urls["dublin"]}/>
          <CityCard cityId="london" name="London" active={city} url={urls["london"]}/>
          <CityCard cityId="newjersey" name="New Jersey" active={city} url={urls["newjersey"]}/>
          <CityCard cityId="neworleans" name="New Orleans" active={city} url={urls["neworleans"]}/>
          <CityCard cityId="newyork" name="New York" active={city} url={urls["newyork"]}/>
          <CityCard cityId="prague" name="Prague" active={city} url={urls["prague"]}/>
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
<div class="body_part bg-light-primary body_block--right">
  <div class="body_block__title">
    <h2>Unprecedented Impact on Social Behavior</h2>
  </div>
  <div class="body_block__visual">
    <SB/>
  </div>
  <div class="body_block__text">
    The spread of the coronavirus has caused policymakers in the U.S. and around the globe to implement strict physical distancing orders to slow the rate of infection and thus flatten the growth curve.
    <br/>
    <br/>
    In an effort to bring information and awareness surrounding the impact of this pandemic, Voxel51 is using our AI-powered video understanding capabilities to gather and analyze video data from public street cams around the world.  Our team has developed the <b>Physical Distancing Index (PDI)</b> to measure the impact on social behavior in public spaces. This measure is non-invasive and does not use other data sources like mobile phone signals, which allow only approximate location estimates; instead we focus on specific centralized locations of interest in each city and literally watch what is happening.
    <br/>
    <br/>
    The data in the graphs speaks for itself: coronavirus and the necessary preventative measures across the globe have had an intense impact on daily life. All of the above cities have seen a sharp decline in public social activity during the month of March.
  </div>
</div>

<div class="body_part bg-light-secondary body_block--centerfull">
  <h2 class="body_block__title--left">What is the Physical Distancing Index?</h2>
  <div class="body_block__text">
    Our <a href="https://voxel51.com/platform"> Platform’s </a> ccomputer vision and state-of-the-art deep learning models are able to detect and identify pedestrians, vehicles, and other human-centric objects in the frames of each live street cam video stream every 15 minutes. . Using this raw data, we compute the PDI,  an aggregate statistical measure that captures the average density of human activity within view of the camera over time. Note that PDI is a privacy-preserving measure that does not extract any identifying information about the individuals in the video.
  </div>
</div>

<div class="body_part bg-light-primary body_block--left">
  <div class="body_block__title">
    <h2>Physical Distancing versus Social Distancing</h2>
  </div>
  <div class="body_block__visual">
    <PD />
  </div>
  <div class="body_block__text" align="left">
    <br/>We named the Voxel51 Physical Distancing Index (PDI) in response to the <a href="https://www.forbes.com/sites/carolkinseygoman/2020/03/23/dont-let-physical-distancing-become-social-distancing/#157df7f949e6">World Health Organization’s recommendation </a> to do so. Physical distancing is intended to reduce the spread of the virus between individuals, especially in situations where an individual is carrying the virus but does not show symptoms.  We wholeheartedly believe that it is intensely important to maintain social connections during this time of physical separation.
  </div>
</div>

<div class="bg-footer-dark body_part bg-dark-primary body_block--center body_block--padtop">
  <h2 class="body_block__title">What’s Next?</h2>
  <div class="body_block__text text-secondary-on-dark">
    As this global pandemic progresses, we will continue to provide frequent updates and data analysis to keep you informed. Stay tuned for more! Subscribe to keep updated on the PDI and related topics and check out the project on Github if you'd like to contribute.
  </div>
  <div class="body_block__hook">
    <ul class="list-inline">
      <li>
        <a class="button-primary" href="https://share.hsforms.com/1HZqZoRqsTneuXFm8pVzR1A2ykyk">Subscribe</a>
      </li>
      <li>
        <a class="button-secondary" href="https://github.com/voxel51/pandemic51">Contribute</a>
      </li>
    </ul>
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
