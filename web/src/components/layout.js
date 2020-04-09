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
import { CITIES } from "../utils/cities"

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
      overlayData: {},
      selectedTime: null,
    }
    this.openOverlay = this.openOverlay.bind(this)
    this.closeOverlay = this.closeOverlay.bind(this)
  }
  componentDidMount() {
    fetch("https://pdi-service.voxel51.com/api/snapshots")
      .then(response => response.json())
      .then(json => {
        this.setState({ data: json["data"] })
      })
  }

  openOverlay(overlayData) {
    const selectedTime = overlayData.clicked ? overlayData.time : null
    this.setState({
      overlayData,
      selectedTime,
    })
    window.history.pushState(
      null,
      "",
      selectedTime ? `?t=${selectedTime}` : window.location.href.split("?")[0]
    )
  }

  closeOverlay(e) {
    e.stopPropagation()
    this.setState({
      overlayData: {},
      selectedTime: null,
    })
    window.history.pushState(null, "", window.location.href.split("?")[0])
  }

  render() {
    const { classes, children, city } = this.props
    const { data, height } = this.state
    const setHeight = height => this.setState({ height })
    const cardListHeight = this.refs.chartContainer
      ? (this.refs.chartContainer.scrollHeight / Object.keys(CITIES).length) *
          7 -
        10
      : 820
    return (
      <div className={classes.wrapper}>
        <Helmet>
          <meta name="referrer" content="no-referrer" />
        </Helmet>
        <Header />
        <div className={"body_part body_part--centerfull bg-light-primary"}>
          <Hidden smDown>
            <Grid container spacing={4}>
              <Grid
                item
                xs={12}
                md={4}
                ref="chartContainer"
                style={{
                  paddingTop: 0,
                  maxHeight: cardListHeight,
                  overflowY: "auto",
                  marginTop: 16,
                }}
              >
                {Object.keys(CITIES).map(cityId => (
                  <CityCard
                    key={cityId}
                    cityId={cityId}
                    name={CITIES[cityId]}
                    active={city == cityId}
                    url={data && data[cityId] ? data[cityId]["url"] : undefined}
                  />
                ))}
              </Grid>
              <Grid item xs={12} md={8}>
                <Grid container spacing={4}>
                  <Grid item md={12}>
                    <Chart
                      title="Physical Distancing Index (PDI)"
                      city={city}
                      onClick={this.openOverlay}
                      clicked={this.state.overlayData.clicked}
                      selectedTime={this.state.selectedTime}
                    />
                  </Grid>
                </Grid>
                <Grid container spacing={4}>
                  <Grid item xs={12} className="media-container">
                    <Player city={city} height={height} setHeight={setHeight}>
                      <ImageOverlay
                        {...this.state.overlayData}
                        height={height}
                        onClose={this.closeOverlay}
                        onNavigate={()=>{}}
                      />
                    </Player>
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
                clicked={this.state.overlayData.clicked}
                onClick={this.openOverlay}
                selectedTime={this.state.selectedTime}
              />
              <Player city={city} height={height} setHeight={setHeight}>
                <ImageOverlay
                  {...this.state.overlayData}
                  height={height}
                  onClose={this.closeOverlay}
                  onNavigate={()=>{}}
                />
              </Player>
              <Grid container spacing={4}>
                {Object.keys(CITIES).map(cityId => (
                  <Grid key={cityId} item xs={6}>
                    <MobileCityCard
                      key={cityId}
                      cityId={cityId}
                      name={CITIES[cityId]}
                      active={city == cityId}
                      url={
                        data && data[cityId] ? data[cityId]["url"] : undefined
                      }
                    />
                  </Grid>
                ))}
              </Grid>
            </div>
          </Hidden>
        </div>
        <Middle />
        <div className={"body_part body_part--centerfull bg-light-secondary"}>
          <div class="body_block__title--left">
            <h2>Comparing the Response</h2>
          </div>
          With the far-reaching impact of the coronavirus around the world, we
          were interested to compare data from each city to see the differences
          in PDI relative to each city over time. But because the geographical
          size and the rate of human activity is vastly different in each city
          (or street cam view), we must account for these differences. As such,
          we needed to normalize the data, or create a common starting point in
          order to make a fair comparison so that we could examine the
          differences over time. To normalize the PDIs, we set the maximum value
          for each location to 100%, and scaled the other values accordingly.
          The comparison chart below plots the normalized PDIs.
          <br />
          <br />
          Consider the Times Square and Seaside Heights feeds; the Times Square
          area is physically much larger and generally occupied by more people
          year round, whereas the Seaside Heights location is sparsely populated
          in the winter but densely in the summer.
          <br />
          <br />
          What insights can we derive from this comparison? Clearly all
          locations we are monitoring showed a similar trend corresponding with
          the spread of the virus and local statutes limiting movement. The
          Prague response, for example, was the earliest significant drop (March
          8th). The Seaside Heights feed was steadily trending downward until
          the recent weekend with good weather but has again fallen off at the
          start of the work-week.
          <br />
          <br />
          <BigChart />
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
