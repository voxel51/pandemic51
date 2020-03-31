/**
 * Chart definitions.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { Component } from "react"
import PropTypes from "prop-types"
import { withStyles } from "@material-ui/core/styles"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import Typography from "@material-ui/core/Typography"
import Divider from "@material-ui/core/Divider"
import moment from "moment"
import HelpTooltip from "./help"
import {
  ResponsiveContainer,
  ReferenceLine,
  AreaChart,
  Area,
  stop,
  defs,
  linearGradient,
  XAxis,
  YAxis,
  CartesianGrid,
  ComposedChart,
  Scatter,
  Tooltip,
  Line,
  Legend,
} from "recharts"
import Async from "react-async"

const timezones = {
  chicago: "America/Chicago",
  dublin: "Europe/Dublin",
  fortlauderdale: "America/New_York",
  london: "Europe/London",
  neworleans: "America/Chicago",
  newjersey: "America/New_York",
  newyork: "America/New_York",
  prague: "Europe/Prague",
}

const cities = {
  chicago: "Chicago",
  dublin: "Dublin",
  fortlauderdale: "Fort Lauderdale",
  london: "London",
  neworleans: "New Orleans",
  newjersey: "New Jersey",
  newyork: "New York",
  prague: "Prague",
}

const styles = theme => ({
  root: {
    width: "100%",
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
})

const colors = [
  "#7eacd9",
  "#1f5972",
  "#938516",
  "#a170e0",
  "#88807f",
  "#d93be0",
  "#f39da0",
]

class BigChart extends Component {
  state = {
    list: [],
    events: [],
    labels: [],
  }

  componentDidMount() {
    fetch(`https://pdi-service.voxel51.com/api/pdi-all`)
      .then(response => response.json())
      .then(json => {
        const data = {}
        for (const city in json.cities) {
          const cityTimes = json.cities[city].time
          const cityPdis = json.cities[city].normalized_pdi
          for (const i in cityTimes) {
            if (data[cityTimes[i]] === undefined)
              data[cityTimes[i]] = { time: cityTimes[i] }
            data[cityTimes[i]][city] = cityPdis[i]
          }
        }
        const array = []
        for (const point in data) {
          array.push(data[point])
        }
        console.log(array)
        this.setState({
          data: array,
        })
      })
  }

  render() {
    const { data } = this.state
    const { classes, title, city } = this.props

    return (
      <Card className={classes.root} square>
        <CardContent style={{ position: "relative", width: "100%" }}>
          <Typography
            variant="h4"
            component="h2"
            style={{ marginBottom: "1rem", textAlign: "center" }}
          >
            Comparison
          </Typography>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart
              data={data}
              margin={{ top: 0, right: 0, left: 30, bottom: 0 }}
            >
              <defs>
                {Object.keys(timezones)
                  .sort()
                  .map((val, i) => {
                    return (
                      <linearGradient
                        id={"color" + String(i)}
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                      >
                        <stop
                          offset="5%"
                          stopColor={colors[i]}
                          stopOpacity={0.8}
                        />
                        <stop
                          offset="95%"
                          stopColor={colors[i]}
                          stopOpacity={0}
                        />
                      </linearGradient>
                    )
                  })}
              </defs>
              <XAxis
                dataKey="time"
                domain={["dataMin", "dataMax"]}
                name="Time"
                tickCount={8}
                tickFormatter={unixTime =>
                  moment
                    .unix(unixTime)
                    .tz(timezones.london)
                    .format("M/D")
                }
                type="number"
              />
              <YAxis
                dataKey="pdi"
                name="PDI"
                width={25}
                domain={[0, 1]}
                label={{
                  value: "PDI",
                  angle: -90,
                  position: "insideLeft",
                  offset: -20,
                }}
              />
              <Tooltip />
              {Object.keys(timezones)
                .sort()
                .map((val, i) => (
                  <Area
                    type="monotone"
                    dataKey={val}
                    stroke={colors[i]}
                    fillOpacity={1}
                    fill={`url(#color${String(colors[i])})`}
                  />
                ))}
            </ComposedChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    )
  }
}

BigChart.propTypes = {
  classes: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired,
}

export default withStyles(styles)(BigChart)
