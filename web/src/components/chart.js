/**
 * Chart definitions.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { Component } from "react"
import PropTypes from "prop-types"
import { withStyles } from "@material-ui/core/styles"
import {
  Card,
  CardActions,
  CardContent,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@material-ui/core";
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
  Label,
  Legend,
} from "recharts"
import Async from "react-async"
import debounce from "lodash/debounce"

const timezones = {
  chicago: "America/Chicago",
  dublin: "Europe/Dublin",
  fortlauderdale: "America/New_York",
  london: "Europe/London",
  neworleans: "America/Chicago",
  newjersey: "America/New_York",
  newyork: "America/New_York",
  prague: "Europe/Prague",
  lasvegas: "America/Los_Angeles",
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
  lasvegas: "Las Vegas",
}

const formal = {
  chicago: "Chicago, Illinois, USA",
  dublin: "Dublin, Ireland",
  fortlauderdale: "Fort Lauderdale, Florida, USA",
  london: "London, England",
  neworleans: "New Orleans, Louisiana, USA",
  newjersey: "Seaside Heights, New Jersey, USA",
  newyork: "New York City, New York, USA",
  prague: "Prague, Czech Republic",
  lasvegas: "Las Vegas, Nevada, USA",
}

const shortLabels = {
  pdi: 'PDI',
  temp: 'Temp',
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
        // todo: real data
        let prevTemp = json.data[0] ? json.data[0].pdi / 2 : 20
        json.data.forEach(i => {
          prevTemp = i.temp = prevTemp + Math.random() - 0.48
        })

        this.setState({
          list: json["data"],
          events: json["events"],
          labels: json["labels"],
        }, () => {
            const match = window.location.search.match(/t=(\d+)/)
            if (match) {
              const selectedTime = Number(match[1])
              this.handleClick({ activeLabel: selectedTime })
            }
          }
        )
      })
  }

  formatFullTime(rawTime) {
    return moment
      .unix(rawTime)
      .tz(timezones[this.props.city])
      .format("dddd,  MMM Do, hh:mm A")
  }

  handleClick(event) {
    if (event && event.activeLabel) {
      const data = this.state.labels[event.activeLabel]
      if (!data) {
        return
      }
      this.props.onClick({
        src: data.url,
        time: data.time,
        timestamp: this.formatFullTime(data.time),
        clicked: true,
      })
    }
  }

  handleHover = debounce(event => {
    if (this.props.clicked) return
    if (event && event.activeLabel) {
      const data = this.state.labels[event.activeLabel]
      if (!data) {
        return
      }
      this.props.onClick({
        src: data.url,
        time: data.time,
        timestamp: this.formatFullTime(data.time),
        clicked: false,
      })
    }
  }, 200)

  handleMouseLeave = debounce(event => {
    if (this.props.clicked) return
    this.props.onClick({
      src: null,
      time: null,
      timestamp: null,
      clicked: null,
    })
  }, 200)

  render() {
    const colorPrimary = 'rgb(255, 109, 4)'
    const colorSecondary = 'rgb(109, 4, 255)'
    const { list, events } = this.state
    const { classes, title, city, selectedTime } = this.props

    const contentFormatter = v => {
      if (!v.payload || !v.payload.length) {
        return null
      }
      const item = v.payload[0].payload
      const event = events[item.event]
      const bull = <span className={classes.bullet}>•</span>
      return (
        <Card square style={{ overflow: "visible", opacity: 0.9 }}>
          <CardContent style={{ overflow: "visible" }}>
            <Typography variant="h5" component="h2">
              {this.formatFullTime(v.label)}
            </Typography>
            {v.payload.map(point => (
              <Typography
                variant="h6"
                component="h3"
                style={{ color: point.color }}
              >
                {shortLabels[point.dataKey]} {bull} {point.value.toFixed(2)}
              </Typography>
            ))}
            {event ?
              <Typography variant="body2" component="p">
                {moment
                  .unix(event.time)
                  .tz(timezones[city])
                  .format("MMM Do")}{" "}
                {bull} {event.event}
              </Typography> :
              null
            }
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
            PDI: {formal[city]}
          </Typography>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart
              data={list}
              margin={{ top: 0, right: 5, left: 30, bottom: 0 }}
              cursor="pointer"
              onClick={this.handleClick.bind(this)}
              onMouseUp={this.handleClick.bind(this)}
              onTouchEnd={this.handleClick.bind(this)}
              onTouchMove={this.handleHover.bind(this)}
              onMouseMove={this.handleHover.bind(this)}
              onMouseLeave={this.handleMouseLeave.bind(this)}
            >
              <defs>
                <linearGradient id="colorPdi" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={colorPrimary} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={colorPrimary} stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={colorSecondary} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={colorSecondary} stopOpacity={0} />
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
                label={
                  <Label
                    value="Physical Distancing Index"
                    position="insideLeft"
                    angle={-90}
                    offset={-20}
                    style={{ textAnchor: "middle" }}
                  />
                }
              />
              <YAxis
                dataKey="temp"
                name="Temp"
                orientation="right"
                width={25}
                label={
                  <Label
                    value="Temperature"
                    position="insideLeft"
                    angle={-90}
                    offset={0}
                    style={{ textAnchor: "middle" }}
                  />
                }
              />
              <Tooltip
                content={contentFormatter}
                allowEscapeViewBox={{ x: false, y: false }}
              />
              {Object.keys(events)
                .sort()
                .map(v => (
                  <ReferenceLine x={v} stroke="#666" strokeOpacity={0.3} />
                ))}
              {selectedTime ? (
                <ReferenceLine x={selectedTime} stroke={colorPrimary} />
              ) : null}
              <Area
                type="monotone"
                dataKey="temp"
                stroke={colorSecondary}
                fillOpacity={1}
                fill="url(#colorTemp)"
              />
              <Area
                type="monotone"
                dataKey="pdi"
                stroke={colorPrimary}
                fillOpacity={1}
                fill="url(#colorPdi)"
              />
            </ComposedChart>
          </ResponsiveContainer>
          <HelpTooltip />
          <div className='chart-dropdown'>
            <InputLabel>Second plot:</InputLabel>
            <Select defaultValue='none'>
              <MenuItem className='chart-dropdown-item' value='none'>None</MenuItem>
              <MenuItem className='chart-dropdown-item' value='temp'>Temperature</MenuItem>
            </Select>
          </div>
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
