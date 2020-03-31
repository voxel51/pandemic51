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
  Label,
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
  average: "Etc/GMT"
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
  average: "Average"
}

const styles = theme => ({
  root: {
    width: "100%",
    overflow: "visible",
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
  "#7da043",
  "#cccccc"
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
        this.setState({
          data: json.data,
        })
      })
  }

  render() {
    const { data } = this.state
    const { classes, title, city } = this.props

    return (
      <Card className={classes.root} square>
        <CardContent
          style={{ position: "relative", width: "100%", overflow: "visible" }}
        >
          <Typography
            variant="h4"
            component="h2"
            style={{ marginBottom: "3rem", textAlign: "center" }}
          >
            Uniformly Sampled Comparison
          </Typography>
          <ResponsiveContainer width="100%" height={400}>
            <ComposedChart
              data={data}
              margin={{ top: 5, right: 0, left: 40, bottom: 0 }}
            >
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
                tickFormatter={v =>
                  v.toLocaleString("en", { style: "percent" })
                }
                label={
                  <Label
                    value="Normalized PDI"
                    position="insideLeft"
                    angle={-90}
                    offset={-30}
                    style={{ textAnchor: "middle" }}
                  />
                }
              />
              <Tooltip
                allowEscapeViewBox={{ x: true, y: true }}
                formatter={(v, n, p) => {
                  return [
                    v.toLocaleString("en", { style: "percent" }),
                    cities[n],
                  ]
                }}
                labelFormatter={v =>
                  moment
                    .unix(v)
                    .tz("Etc/GMT")
                    .format("dddd,  MMM Do, hh:mm A z")
                }
              />
              {Object.keys(timezones)
                .sort()
                .map((val, i) => (
                  <Area
                    type="monotone"
                    dataKey={val}
                    stroke={val === "average" ? "#ff6d04" : colors[i]}
                    strokeWidth={val === "average" ? 6 : 3}
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
