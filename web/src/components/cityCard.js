import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Clock from 'react-live-clock';
import CardMedia from '@material-ui/core/CardMedia';
import CardActionArea from '@material-ui/core/CardActionArea';
import { Link } from "gatsby";
const useStyles = makeStyles({
  root: {
    marginBottom: '1rem',
    overflow: "visible",
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
  content: {
    paddingLeft: (99.5 * 16/9) + 16
  },
  still: {
    margin: 0,
    left: 0,
    width: 99.5 * 16/9,
    height: 99.5,
    position: "absolute",
  }
});

const timezones = {
  "chicago": "America/Chicago",
  "dublin": "Europe/Dublin",
  "london": "Europe/London",
  "neworleans": "America/Chicago",
  "newjersey": "America/New_York",
  "newyork": "America/New_York",
  "prague": "Europe/Prague"
}

export default function CityCard(props) {
  const classes = useStyles();
  const active = props.cityId === props.active && props.cityId !== undefined;
  return (
    <Card className={classes.root} square>
      <CardActionArea>
        <CardMedia
          className={classes.still + (active ? " active-card" : "")}
          image="https://material-ui.com/static/images/cards/contemplative-reptile.jpg"
          title="Contemplative Reptile"
        />
        <Link to={"/" + props.cityId}>
        <CardContent className={classes.content}>
          <Typography variant="h5" component="h2">
            {props.name}
          </Typography>
          <Typography className={classes.pos} color="textSecondary">
            <Clock format={'HH:mm:ss A'} ticking={true} timezone={timezones[props.cityId]} />
          </Typography>
          <Typography variant="body2" component="p">
            Some metric
          </Typography>
        </CardContent>
      </Link>
      </CardActionArea>
      </Card>
    );
}
