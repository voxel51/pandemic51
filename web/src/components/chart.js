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
    list: []
  };

  componentDidMount() {

    fetch(`http://34.67.136.168/api/${this.props.city}/data`)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        this.setState({ list: json["data"] })
      });
  }

  render() {
    const { list } = this.state;
    const { classes, title, city } = this.props;
    return (
      <Card className={classes.root} square>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
<AreaChart width={730} height={250} data={list}
  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
  <defs>
    <linearGradient id="sdi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#ff6d04" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#ff6d04" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis         dataKey = 'time'
        domain = {['auto', 'auto']}
        name = 'Time'
        tickFormatter = {(unixTime) => moment(unixTime).tz(timezones[city]).format('hh:mm A M D')}
        type = 'number'/>
  <YAxis dataKey = 'sdi' name = 'SDI' />
  <Tooltip />
  <Area type="monotone" dataKey="sdi" stroke="#ff6d04" fillOpacity={1} fill="url(#colorUv)" />
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
