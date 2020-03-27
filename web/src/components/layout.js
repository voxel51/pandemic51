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
import {
  withStyles,
  makeStyles,
  createStyles,
  Theme,
} from "@material-ui/core/styles"
import Paper from "@material-ui/core/Paper"
import Grid from "@material-ui/core/Grid"
import Card from "@material-ui/core/Card"
import CardContent from "@material-ui/core/CardContent"
import Img from "gatsby-image"
import CityCard from "./cityCard"
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
    const { classes, children, city } = this.props
    const { urls } = this.state

    return (
      <div className={classes.wrapper}>
        <Helmet>
          <meta name="referrer" content="no-referrer" />
        </Helmet>
        <Header />
        <div className="cta-wrapper">
          <div className="cta">
            <h2 class="body_block__title">
              Measuring the Social Impact of the Coronavirus Pandemic
            </h2>
            <div class="body_block__text">
              The Physical Distancing Index (PDI), created by Voxel51, uses
              computer vision to track how the Coronavirus and governing
              policies are impacting the social behavior of people in various
              cities, in real-time.
            </div>
          </div>
        </div>
        <div className="cta-wrapper bg-light-primary">
          <div className="cta">
            <div class="body_block__text">
              Click on the city cards on the left to pull up a live video stream from a city of your choice. Then, hover over the graph to view information about relevant news events from the city, as well as snapshots from the stream with detections from the computer vision models overlaid. Scroll down to read more about the PDI metric and the impact of Coronavirus on society.
            </div>
          </div>
        </div>
        <div className={classes.root}>
          <div className="contentBody">
            <Grid container spacing={4}>
              <Grid item xs={12} md={4}>
                <CityCard
                  cityId="chicago"
                  name="Chicago"
                  active={city}
                  url={urls["chicago"]}
                />
                <CityCard
                  cityId="dublin"
                  name="Dublin"
                  active={city}
                  url={urls["dublin"]}
                />
                <CityCard
                  cityId="london"
                  name="London"
                  active={city}
                  url={urls["london"]}
                />
                <CityCard
                  cityId="newjersey"
                  name="New Jersey"
                  active={city}
                  url={urls["newjersey"]}
                />
                <CityCard
                  cityId="neworleans"
                  name="New Orleans"
                  active={city}
                  url={urls["neworleans"]}
                />
                <CityCard
                  cityId="newyork"
                  name="New York"
                  active={city}
                  url={urls["newyork"]}
                />
                <CityCard
                  cityId="prague"
                  name="Prague"
                  active={city}
                  url={urls["prague"]}
                />
              </Grid>
              <Grid item xs={12} md={8}>
                <Hidden smDown>
                  <Grid container spacing={4}>
                    <Grid item md={12}>
                      <Chart
                        title="Physical Distancing Index (PDI)"
                        city={city}
                        // todo: use correct image url
                        onClick={_ => this.setState({ src: _ })}
                      />
                    </Grid>
                  </Grid>
                </Hidden>
                <Grid container spacing={4}>
                  <Grid
                    item
                    xs={12}
                    className="detector-container"
                    style={{ boxSizing: "content-box" }}
                  >
                    <Player city={city} />
                    <ImageOverlay
                      src={this.state.src}
                      onClose={e => {
                        e.stopPropagation()
                        this.setState({ src: null })
                      }}
                    />
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </div>
        </div>
        <div className="cta-wrapper bg-light-primary">
          <div className="cta">
              <h2 class="body_block__title" style={{color: "rgb(23, 25, 28)"}}>
                Unprecedented Impact to Social Behavior
              </h2>
              <div class="body_block__text">
                <br/>
              The spread of the Coronavirus has caused policymakers in the US and around the globe to implement strict physical distancing to slow the rate of infection and thus flatten the growth curve.
              <br/>
              <br/>
              In an effort to bring information and awareness surrounding the impact of this pandemic, Voxel51 is using our AI-powered video understanding capabilities to gather and analyze video data from public streams across the world.  Our team has developed the <span className="black-highlight">Physical Distancing Index (PDI)</span> to measure the impact on social behavior in public spaces. This measure is non-invasive and does not use other data sources like mobile phone signals, which allow only approximate location estimates; instead we focus on specific centralized locations of interest in each city and literally watch what is happening.
<br/><br/>
The data in the graphs speaks for itself: Coronavirus and the necessary preventative measures across the globe have had an intense impact on daily life. All of the above cities have seen a sharp decline in public social activity during the month of March.
            </div>
          </div>
        </div>
        <div className="cta-wrapper gray">
          <div className="cta">
              <h2 class="body_block__title" style={{color: "rgb(23, 25, 28)"}}>
              What is the Physical Distancing Index?
              </h2>
              <div class="body_block__text">
                <br/>
                This website monitors video streams using <span className="orange-higlight">our Platform’s</span> computer vision engine to detect pedestrians, vehicles, and other human-centric objects in view of the camera. Using state-of-the-art deep learning models, we transform the raw frames from the video feed into a set of “positive hits” that we represent as rectangles in the video frame.  If you hover over the data point in the graph above, you will see the actual detection output for that specific video frame.
        <br/><br/>
We compute the PDI for each city from images sampled every 15 minutes from each video stream. Using this raw data, we compute an aggregate statistical measure that captures the average density of human activity within view of the camera over time. Note that PDI is a privacy-preserving measure that does not extract any identifying information about the individuals in the video.

            </div>
          </div>
        </div>
        <div className="cta-wrapper bg-light-primary">
          <div className="cta">
            <h2 class="body_block__title" style={{color: "rgb(23, 25, 28)"}}>
              Physical Distancing versus Social Distancing
              </h2>
              <div class="body_block__text">
                We have named our measure the Physical Distancing Index in response to the <span className="orange-highlight">World Health Organization’s recommendation</span> to do so. This physical distancing is intended to reduce the spread of the virus between individuals, especially in situations where an individual is carrying the virus but does not yet show symptoms.  We wholeheartedly agree that, in this time of physical separation, it is intensely important to maintain social connections.
            </div>
          </div>
        </div>
        <div className="cta-wrapper">
          <div className="cta">
            <h2 class="body_block__title">
              What’s Next?
              </h2>
              <div class="body_block__text">
                <br/>
                As this global pandemic progresses, we will continue to provide frequent updates and data analysis to keep you informed. Stay tuned for more!
            </div>
          </div>
        </div>
        <Footer />
      </div>
    )
  }
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
  classes: PropTypes.node.isRequired,
}

export default withStyles(styles)(Layout)
