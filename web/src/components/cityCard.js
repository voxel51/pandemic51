import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Clock from 'react-live-clock';
import CardActionArea from '@material-ui/core/CardActionArea';
import { Link } from "gatsby";
const useStyles = makeStyles({
  root: {
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

export default function CityCard(props) {
  const classes = useStyles();
  const highlighted = Boolean(props.highlighted);
  return (
    <Card className={classes.root} square>
      <CardActionArea>
        <Link to={"/" + props.name}>
        <CardContent>
          <Typography variant="h5" component="h2">
            {props.name}
          </Typography>
          <Typography className={classes.pos} color="textSecondary">
            <Clock format={'HH:mm:ss'} ticking={true} timezone={'US/Pacific'} />
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
