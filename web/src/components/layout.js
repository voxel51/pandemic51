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
import Footer from "./footer"
import Typography from "@material-ui/core/Typography"

const CITIES = {
  dublin: "Dublin",
  london: "London",
  newjersey: "New Jersey",
  neworleans: "New Orleans",
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
                        // todo: use correct image url
                        onClick={_ => this.setState({ src: _ })}
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
        <Footer />
      </div>
    )
  }
}

  /*

        <div className={classes.root + " bg-light-primary"}>
          <div className="contentBody">
            <BigChart/>
          </div>
          </div>

  */

Layout.propTypes = {
  children: PropTypes.node.isRequired,
  classes: PropTypes.node.isRequired,
}

export default withStyles(styles)(Layout)
