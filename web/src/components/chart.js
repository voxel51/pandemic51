import React, { Component } from "react";
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

const TABLE_LIST = [
	{
		name: 'Page A', uv: 4000, pv: 2400, amt: 2400,
	},
	{
		name: 'Page B', uv: 3000, pv: 1398, amt: 2210,
	},
	{
		name: 'Page C', uv: 2000, pv: 9800, amt: 2290,
	},
	{
		name: 'Page D', uv: 2780, pv: 3908, amt: 2000,
	},
	{
		name: 'Page E', uv: 1890, pv: 4800, amt: 2181,
	},
	{
		name: 'Page F', uv: 2390, pv: 3800, amt: 2500,
	},
	{
		name: 'Page G', uv: 3490, pv: 4300, amt: 2100,
	}
];

const styles = theme => ({
  root: {
    minWidth: 275,
    margin: '1rem 0'
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
    list: [...TABLE_LIST]
  };

  render() {
    const { list } = this.state;
    const { classes } = this.props;
    return (
      <Card className={classes.root} square>
        <CardContent>
        <LineChart
          width={600}
          height={300}
          data={list}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
  				<CartesianGrid strokeDasharray="3 3" />
					<XAxis dataKey="name" interval="preserveEnd" />
					<YAxis interval="preserveEnd" />
					<Legend />
					<Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
					<Line type="monotone" dataKey="uv" stroke="#82ca9d" />
        </LineChart>
      </CardContent>
      </Card>
    );
  }
}

Chart.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Chart);
