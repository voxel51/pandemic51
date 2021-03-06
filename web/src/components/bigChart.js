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
import { HISCITIES, COLORS, TIMEZONES } from "../utils/cities"

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

class BigChart extends Component {
  state = {
    data: [],
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

    const contentFormatter = v => {
      if (!v.payload) {
        return null
      }
      const bull = <span className={classes.bullet}>•</span>
      return (
        <Card square style={{ overflow: "visible", opacity: 0.9 }}>
          <CardContent style={{ overflow: "visible" }}>
            <Typography variant="h5" component="h2">
              {moment
                .unix(v.label)
                .tz("Etc/GMT")
                .format("dddd,  MMM Do, hh:mm A z")}
            </Typography>
            {v.payload
              .sort((a, b) => {
                if (a.dataKey === "average") return -1
                if (b.dataKey === "average") return 1
                if (!a.value && !b.value) return 0
                if (!a.value) return -1
                if (!b.value) return 1
                return b.value - a.value
              })
              .map((v, i) => {
                if (!v.value) return
                return (
                  <Typography
                    key={v.dataKey}
                    variant="h5"
                    component="h3"
                    style={{ color: v.color }}
                  >
                    {{ ...HISCITIES, average: "Average" }[v.dataKey]} {bull}{" "}
                    {v.value.toLocaleString("en", { style: "percent" })}
                  </Typography>
                )
              })}
          </CardContent>
        </Card>
      )
    }
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
            Comparison of PDI Across Locations
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
                    .tz("Etc/GMT")
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
                    value="PDI Percentile"
                    position="insideLeft"
                    angle={-90}
                    offset={-30}
                    style={{ textAnchor: "middle" }}
                  />
                }
              />
              <Tooltip
                allowEscapeViewBox={{ x: false, y: false }}
                content={contentFormatter}
                formatter={(v, n, p) => {
                  return [
                    v.toLocaleString("en", { style: "percent" }),
                    { ...HISCITIES, average: "Average" }[n],
                  ]
                }}
                labelFormatter={v =>
                  moment
                    .unix(v)
                    .tz("Etc/GMT")
                    .format("dddd,  MMM Do, hh:mm A z")
                }
              />
              {Object.keys({ ...HISCITIES, average: "average" })
                .sort()
                .map((val, i) => (
                  <Line
                    key={val}
                    type="monotone"
                    dataKey={val}
                    stroke={val === "average" ? "#ff6d04" : COLORS[i]}
                    strokeWidth={val === "average" ? 8 : 3}
                    strokeOpacity={val === "average" ? 1 : 0.5}
                    fill={`url(#color${String(COLORS[i])})`}
                    dot={false}
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
