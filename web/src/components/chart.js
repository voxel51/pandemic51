import React, { Component, Text } from "react";
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import moment from 'moment'
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
  Legend
} from "recharts";
import Async from "react-async";

const timezones = {
  "chicago": "America/Chicago",
  "dublin": "Europe/Dublin",
  "london": "Europe/London",
  "neworleans": "America/Chicago",
  "newjersey": "America/New_York",
  "newyork": "America/New_York",
  "prague": "Europe/Prague"
}

const styles = theme => ({
  root: {
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});


class Chart extends Component {
  state = {
    list: [],
    events: []
  };

  componentDidMount() {

    fetch(`http://34.67.136.168/api/pdi/${this.props.city}`)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        this.setState({
          list: json["data"],
          events: json["events"]
        })
      });
  }

  handleClick(data) {
    if (data) {
      console.log('chart clicked at', data.activeLabel);
      this.props.onClick('some-image-url');
    }
  }

  render() {
    const { list, events } = this.state;
    const { classes, title, city } = this.props;



    const contentFormatter = v => {
      const valid = v.payload.length ? v.payload[0].payload : false;
      const event = valid ? events[valid.event].event : "-";
      const time = valid ? events[valid.event].time : "-";
      return (
        <Card square>
          <CardContent>
            <Typography variant="h5" component="h2">
              {moment.unix(v.label).tz(timezones[city]).format("dddd,  MMM Do, hh:mm A")}
            </Typography>
            <Typography color="textSecondary">
              {v.payload.length ? v.payload[0].value : "-"} Detections
            </Typography>
            <Typography variant="body2" component="p">
              {moment.unix(time).tz(timezones[city]).format("MMM Do")} - {event}
            </Typography>
          </CardContent>
        </Card>
      )
    }

    return (
      <Card className={classes.root} square>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
<ComposedChart width={730} height={250} data={list}
  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
  cursor="pointer"
  onClick={this.handleClick.bind(this)}>
  <defs>
    <linearGradient id="colorSdi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#ff6d04" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#ff6d04" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis
        dataKey = 'time'
        domain = {['dataMin', 'dataMax']}
        name = 'Time'
        tickCount={8}
        tickFormatter = {(unixTime) => moment.unix(unixTime).tz(timezones[city]).format('M/D')}
        type = 'number'/>
      <YAxis dataKey = 'pdi' name = 'PDI' />
      <Tooltip content={contentFormatter}/>
      <Area type="monotone" dataKey="pdi" stroke="#ff6d04" fillOpacity={1} fill="url(#colorSdi)" />
      <Line dataKey="event" dot={{ stroke: 'green', strokeWidth: 2 }} />
</ComposedChart>
      </ResponsiveContainer>
      </CardContent>
      </Card>
    );
  }
}

Chart.propTypes = {
  classes: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default withStyles(styles)(Chart);
