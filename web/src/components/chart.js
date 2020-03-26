import React, { Component } from "react";
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
  Tooltip,
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

    fetch(`http://34.67.136.168/api/data/${this.props.city}`)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        this.setState({
          list: json["data"],
          events: json["events"]
        })
      });
  }

  render() {
    const { list, events } = this.state;
    const { classes, title, city } = this.props;
    return (
      <Card className={classes.root} square>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
<AreaChart width={730} height={250} data={list}
  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
  <defs>
    <linearGradient id="colorSdi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#ff6d04" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#ff6d04" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis         dataKey = 'time'
        domain = {['auto', 'auto']}
        name = 'Time'
        tickCount={8}
        tickFormatter = {(unixTime) => moment.unix(unixTime).tz(timezones[city]).format('M/D')}
        type = 'number'/>
      <YAxis dataKey = 'sdi' name = 'SDI' />
      <Tooltip
        formatter={ (v, n, p) => {
          return [v, "Detections"]
      }}
      labelFormatter={ val => {
        return moment.unix(val).tz(timezones[city]).format("dddd,  MMM Do, hh:mm A");
      }}/>
  {events.map((value, idx) => {
          return <ReferenceLine x={value.time} stroke="green" label={value.event} alwaysShow={true}/>
        })}
  <Area type="monotone" dataKey="sdi" stroke="#ff6d04" fillOpacity={1} fill="url(#colorSdi)" />
</AreaChart>
      </ResponsiveContainer>
      </CardContent>
      </Card>
    );
  }
}

Chart.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Chart);
