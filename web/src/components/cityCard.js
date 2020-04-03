/**
 * City card components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import Card from "@material-ui/core/Card"
import CardActionArea from "@material-ui/core/CardActionArea"
import CardContent from "@material-ui/core/CardContent"
import CardMedia from "@material-ui/core/CardMedia"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import { Link } from "gatsby"
import React from "react"
import Clock from "react-live-clock"
import Hidden from "@material-ui/core/Hidden"
import { LOCATIONS, TIMEZONES } from "../utils/cities"

const useStyles = makeStyles({
  root: {
    marginBottom: "1rem",
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
  content: { paddingRight: (107 * 16) / 9, paddingLeft: 8 },
  still: {
    margin: 0,
    right: 0,
    width: (107 * 16) / 9,
    height: 107,
    position: "absolute",
  },
  chip: {
    position: "absolute",
    right: 0,
    bottom: 0,
    margin: "0 .5rem .5rem 0",
    padding: ",0.5rem",
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
})

export default function CityCard(props) {
  const classes = useStyles()
  const active = props.active
  const bull = <span className={classes.bullet}>•</span>
  return (
    <Card className={classes.root + (active ? " active-card" : "")} square>
      <CardActionArea>
        <Link to={"/" + props.cityId}>
          <Hidden mdDown>
            <CardMedia
              className={classes.still}
              image={props.url}
              title={LOCATIONS[props.cityId]}
            />

            <CardContent className={classes.content}>
              <Typography variant="h5" component="h2">
                {props.name}
              </Typography>
              <Typography
                variant="h6"
                component="h3"
                className={classes.pos}
                color="textSecondary"
              >
                <Clock
                  format={"hh:mm:ss A"}
                  ticking={true}
                  timezone={TIMEZONES[props.cityId]}
                />
              </Typography>
              <Typography variant="body1" component="p">
                {LOCATIONS[props.cityId]}
              </Typography>
            </CardContent>
          </Hidden>
          <Hidden lgUp>
            <CardContent>
              <Typography variant="h5" component="h2">
                {props.name}
              </Typography>
              <Typography
                variant="h6"
                component="h3"
                className={classes.pos}
                color="textSecondary"
              >
                <Clock
                  format={"hh:mm:ss A"}
                  ticking={true}
                  timezone={TIMEZONES[props.cityId]}
                />
              </Typography>
              <Typography variant="body1" component="p">
                {LOCATIONS[props.cityId]}
              </Typography>
            </CardContent>
          </Hidden>
        </Link>
      </CardActionArea>
    </Card>
  )
}
