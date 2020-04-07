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
} from "@material-ui/core"
import moment from "moment"
import HelpTooltip from "./help"
import { FORMAL, TIMEZONES } from "../utils/cities"
import { addDataToSeries } from "../utils/data"
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

const plotOptions = {
  pdi: {
    name: 'PDI',
    abbr: 'PDI',
    primary: true,
  },
  cases: {
    name: 'Number of cases',
    abbr: 'Cases',
  },
  deaths: {
    name: 'Number of deaths',
    abbr: 'Deaths',
  },
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
    secondPlot: localStorage.secondPlot || 'none',
    metadata: {}
  }

  componentDidMount() {
    fetch(`https://pdi-service.voxel51.com/api/pdi/${this.props.city}`)
      .then(response => response.json())
      .then(json => {
        json.data = addDataToSeries(json.data, json.cases)
        json.data = addDataToSeries(json.data, json.deaths)

        this.setState({
          list: json["data"],
          events: json["events"],
          labels: json["labels"],
          metadata: json["metadata"]
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
      .tz(TIMEZONES[this.props.city])
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

  handlePlotChange(event) {
    const secondPlot = event.target.value;
    this.setState({ secondPlot })
    localStorage.secondPlot = secondPlot;
  }

  render() {
    const colorPrimary = 'rgb(255, 109, 4)'
    const colorSecondary = 'rgb(109, 4, 255)'
    const { list, events, secondPlot, metadata } = this.state
    const { classes, title, city, selectedTime } = this.props

    const formatNumber = n => {
      if (Math.round(n) == n) {
        return n
      }
      return n.toFixed(2)
    }

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
                key={point.dataKey}
                variant="h6"
                component="h3"
                style={{ color: point.color }}
              >
                {plotOptions[point.dataKey].abbr} {bull} {formatNumber(point.value)}
              </Typography>
            ))}
            {event ?
              <Typography variant="body2" component="p">
                {moment
                  .unix(event.time)
                  .tz(TIMEZONES[city])
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
        <CardContent style={{ position: "relative", width: "100%", paddingBottom: 12 }}>
          <Typography
            variant="h4"
            component="h2"
            style={{ marginBottom: "1rem", textAlign: "center" }}
          >
            PDI: {FORMAL[city]}
          </Typography>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart
              data={list}
              margin={{ top: 0, right: 20, left: 30, bottom: 0 }}
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
                <linearGradient id="colorSecond" x1="0" y1="0" x2="0" y2="1">
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
                    .tz(TIMEZONES[city])
                    .format("M/D")
                }
                type="number"
              />
              <YAxis
                dataKey="pdi"
                yAxisId="pdi"
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
              {plotOptions[secondPlot] ? (
                <YAxis
                  dataKey={secondPlot}
                  yAxisId="secondary"
                  name={plotOptions[secondPlot].name}
                  orientation="right"
                  mirror={true}
                  label={
                    <Label
                      value={plotOptions[secondPlot].name}
                      position="right"
                      angle={-90}
                      offset={10}
                      style={{ textAnchor: "middle" }}
                    />
                  }
                />
              ) : null}
              <Tooltip
                content={contentFormatter}
                allowEscapeViewBox={{ x: false, y: false }}
              />
              {Object.keys(events)
                .sort()
                .map(v => (
                  <ReferenceLine x={v} key={v} stroke="#666" strokeOpacity={0.3} yAxisId="pdi" />
                ))}
              {selectedTime ? (
                <ReferenceLine x={selectedTime} stroke={colorPrimary} yAxisId="pdi" />
              ) : null}
              {plotOptions[secondPlot] ? (
                <Area
                  key={secondPlot}
                  yAxisId="secondary"
                  type="monotone"
                  dataKey={secondPlot}
                  stroke={colorSecondary}
                  fillOpacity={1}
                  fill="url(#colorSecond)"
                />
              ) : null}
              <Area
                yAxisId="pdi"
                type="monotone"
                dataKey="pdi"
                stroke={colorPrimary}
                fillOpacity={1}
                fill="url(#colorPdi)"
              />
            </ComposedChart>
          </ResponsiveContainer>
          <HelpTooltip />
          <div className='chart-footer'>
            <div className='chart-dropdown'>
            <InputLabel style={{lineHeight: "100%", display: "table-cell", verticalAlign: "middle", height: 40}}>Show:</InputLabel>
            <Select value={this.state.secondPlot} onChange={this.handlePlotChange.bind(this)}>
              <MenuItem className='chart-dropdown-item' value='none'>PDI only</MenuItem>
              {Object.entries(plotOptions).map(([key, option]) => (
                option.primary ? null : (
                  <MenuItem className='chart-dropdown-item' key={key} value={key}>{option.name}</MenuItem>
                )
              ))}
            </Select>
          </div>
            <Typography variant="h6" component="p" color="textSecondary">
              {metadata[secondPlot]}<br/>
              <span>
                <i>Source: <a href="https://coronavirus.jhu.edu/map.html" target="_blank">https://coronavirus.jhu.edu/map.html</a></i></span>
            </Typography>
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
