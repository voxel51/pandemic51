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
import CityCard from "./cityCard"
import MobileCityCard from "./mobileCityCard"
import "./layout.css"
import "./../utils/typography"
import Player from "./player"
import Chart from "./chart"
import BigChart from "./bigChart"
import Hidden from "@material-ui/core/Hidden"
import ImageOverlay from "./imageOverlay"
import Header from "./header"
import Middle from "./middle"
import Footer from "./footer"
import Typography from "@material-ui/core/Typography"

const CITIES = {
  dublin: "Dublin",
  london: "London",
  newjersey: "New Jersey",
  newyork: "New York",
  prague: "Prague",
  fortlauderdale: "Fort Lauderdale",
}

const styles = {
  wrapper: {
    display: "flex",
    minHeight: "100vh",
    flexDirection: "column",
  },
  root: {
    width: "100%",
    paddingTop: "10rem",
    paddingBottom: "10rem",
  },
}

class Layout extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: {},
    }
  }
  componentDidMount() {
    fetch("https://pdi-service.voxel51.com/api/snapshots")
      .then(response => response.json())
      .then(json => {
        this.setState({ data: json["data"] })
      })
  }

  render() {
    const { classes, children, city } = this.props
    const { data, height } = this.state
    const setHeight = height => this.setState({ height })
    return (
      <div className={classes.wrapper}>
        <Helmet>
          <meta name="referrer" content="no-referrer" />
        </Helmet>
        <Header />
        <div className={classes.root}>
          <div className="contentBody">
            <Hidden smDown>
              <Grid container spacing={4}>
                <Grid item xs={12} md={4}>
                  {Object.keys(CITIES)
                    .sort()
                    .map(cityId => (
                      <CityCard
                        key={cityId}
                        cityId={cityId}
                        name={CITIES[cityId]}
                        active={city == cityId}
                        url={
                          data && data[cityId] ? data[cityId]["url"] : undefined
                        }
                      />
                    ))}
                </Grid>
                <Grid item xs={12} md={8}>
                  <Grid container spacing={4}>
                    <Grid item md={12}>
                      <Chart
                        title="Physical Distancing Index (PDI)"
                        city={city}
                        onClick={src => this.setState({ src })}
                      />
                    </Grid>
                  </Grid>
                  <Grid container spacing={4}>
                    <Grid item xs={12} className="media-container">
                      <Player
                        city={city}
                        height={height}
                        setHeight={setHeight}
                      />
                      <ImageOverlay
                        src={this.state.src}
                        height={height}
                        onClose={e => {
                          e.stopPropagation()
                          this.setState({ src: null })
                        }}
                      />
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Hidden>
            <Hidden mdUp>
              <div className="mobileContent">
                <Chart
                  title="Physical Distancing Index (PDI)"
                  city={city}
                  // todo: use correct image url
                  onClick={_ => this.setState({ src: _ })}
                />
                <Player city={city} height={height} setHeight={setHeight}>
                  <ImageOverlay
                    src={this.state.src}
                    height={height}
                    onClose={e => {
                      e.stopPropagation()
                      this.setState({ src: null })
                    }}
                  />
                </Player>
                <Grid container spacing={4} style={{ marginTop: "1rem" }}>
                  {Object.keys(CITIES)
                    .sort()
                    .map(cityId => (
                      <Grid item xs={6}>
                        <MobileCityCard
                          key={cityId}
                          cityId={cityId}
                          name={CITIES[cityId]}
                          active={city == cityId}
                          url={
                            data && data[cityId]
                              ? data[cityId]["url"]
                              : undefined
                          }
                        />
                      </Grid>
                    ))}
                </Grid>
              </div>
            </Hidden>
          </div>
        </div>
        <Middle />
        <div className={classes.root + " bg-light-primary"}>
          <div className="big-chart-body contentBody">
            <div class="body_block__title--left">
              <h2>Comparing the Response</h2>
            </div>
            With the far-reaching impact of the coronavirus around the world, we
            were interested to compare data from each city to see the
            differences in PDI relative to each city over time. But because the
            geographical size and the rate of human activity is vastly different
            in each city (or street cam view), we must account for these
            differences. As such, we needed to normalize the data, or create a
            common starting point in order to make a fair comparison so that we
            could examine the differences over time. To normalize the PDIs, we
            set the maximum value for each location to 100%, and scaled the
            other values accordingly. The comparison chart below plots the
            normalized PDIs.
            <br />
            <br />
            Consider the Times Square and Seaside Heights feeds; the Times
            Square area is physically much larger and generally occupied by more
            people year round, whereas the Seaside Heights location is sparsely
            populated in the winter but densely in the summer.
            <br />
            <br />
            What insights can we derive from this comparison? Clearly all
            locations we are monitoring showed a similar trend corresponding
            with the spread of the virus and local statutes limiting movement.
            The Prague response, for example, was the earliest significant drop
            (March 8th). The Seaside Heights feed was steadily trending downward
            until the recent weekend with good weather but has again fallen off
            at the start of the work-week.
            <br />
            <br />
            <BigChart />
          </div>
        </div>
        <Footer />
      </div>
    )
  }
}

/*


  */

Layout.propTypes = {
  children: PropTypes.node.isRequired,
  classes: PropTypes.node.isRequired,
}

export default withStyles(styles)(Layout)
