import React, { Component } from "react";
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
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

const TABLE_LIST = [
	{
		name: 'Page A', uv: 4000
	},
	{
		name: 'Page B', uv: 3000
	},
	{
		name: 'Page C', uv: 2000
	},
	{
		name: 'Page D', uv: 2780
	},
	{
		name: 'Page E', uv: 1890
	},
	{
		name: 'Page F', uv: 2390
	},
	{
		name: 'Page G', uv: 3490
	}
];

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
    list: [...TABLE_LIST]
  };

  render() {
    const { list } = this.state;
    const { classes, title } = this.props;
    return (
      <Card className={classes.root} square>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
<AreaChart width={730} height={250} data={list}
  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
  <defs>
    <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#ff6d04" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#ff6d04" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
  <Area type="monotone" dataKey="uv" stroke="#ff6d04" fillOpacity={1} fill="url(#colorUv)" />
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
