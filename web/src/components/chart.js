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

class Chart extends Component {
  state = {
    list: [],
    events: [],
    labels: [],
  }

  componentDidMount() {
    fetch(`https://pdi-service.voxel51.com/api/pdi/${this.props.city}`)
      .then(response => response.json())
      .then(json => {
        this.setState({
          list: json["data"],
          events: json["events"],
          labels: json["labels"],
        })
      })
  }

  handleClick(data) {
    if (data && data.activeLabel) {
      this.props.onClick(this.state.labels[data.activeLabel].url)
    }
  }

  render() {
    const { list, events } = this.state
    const { classes, title, city } = this.props

    const contentFormatter = v => {
      if (!v.payload) {
        return null
      }
      const valid = v.payload.length ? v.payload[0].payload : false
      const event =
        valid && events[valid.event] ? events[valid.event].event : false
      const time = valid && valid.event ? events[valid.event].time : false
      const bull = <span className={classes.bullet}>•</span>
      return (
        <Card square>
          <CardContent>
            <Typography variant="h5" component="h2">
              {moment
                .unix(v.label)
                .tz(timezones[city])
                .format("dddd,  MMM Do, hh:mm A")}
            </Typography>
            <Typography
              variant="h6"
              component="h3"
              style={{ color: "rgb(255, 109, 4)" }}
            >
              PDI: {v.payload.length ? v.payload[0].value.toFixed(2) : "-"}
            </Typography>
            {(() => {
              if (event && time) {
                return (
                  <Typography variant="body2" component="p">
                    {moment
                      .unix(time)
                      .tz(timezones[city])
                      .format("MMM Do")}{" "}
                    {bull} {event}
                  </Typography>
                )
              }
            })()}
          </CardContent>
        </Card>
      )
    }

    return (
      <Card className={classes.root} square>
        <CardContent style={{ position: "relative", width: "100%" }}>
          <Typography
            variant="h4"
            component="h2"
            style={{ marginBottom: "1rem", textAlign: "center" }}
          >
            PDI: {cities[city]}
          </Typography>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart
              width="100%"
              data={list}
              margin={{ top: 0, right: 0, left: 30, bottom: 0 }}
              cursor="pointer"
              onClick={this.handleClick.bind(this)}
            >
              <defs>
                <linearGradient id="colorSdi" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ff6d04" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#ff6d04" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="time"
                domain={["dataMin", "dataMax"]}
                name="Time"
                tickCount={8}
                tickFormatter={unixTime =>
                  moment
                    .unix(unixTime)
                    .tz(timezones[city])
                    .format("M/D")
                }
                type="number"
              />
              <YAxis
                dataKey="pdi"
                name="PDI"
                width={25}
                label={{
                  value: "PDI",
                  angle: -90,
                  position: "insideLeft",
                  offset: -20,
                }}
              />
              <Tooltip content={contentFormatter} />
              <Area
                type="monotone"
                dataKey="pdi"
                stroke="#ff6d04"
                fillOpacity={1}
                fill="url(#colorSdi)"
              />
              <Line dataKey="event" dot={{ stroke: "green", strokeWidth: 2 }} />
            </ComposedChart>
          </ResponsiveContainer>
          <HelpTooltip />
        </CardContent>
      </Card>
    )
  }
}

Chart.propTypes = {
  classes: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired,
}

export default withStyles(styles)(Chart)
