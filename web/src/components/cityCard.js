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
import { BETA, NEW, LOCATIONS, TIMEZONES } from "../utils/cities"
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
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
    padding: "0.5rem",
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
  tickerWrapper: {
    position: "absolute",
    top: "0.5rem",
    right: 0,
    width: (107*16)/9,
    display: "flex",
    justifyContent: "space-between",
  },
  ticker: {
    padding: "0.5rem",
    margin: "0 .5rem 0 .5rem",
    fontSize: "0.7rem",
    borderRadius: "2px"
  },
  tickerContent: {
    margin: 0,
    padding: 0,
    paddingBottom: "0 !important"
  }
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
              <div className={classes.tickerWrapper}>
              <Card square className={classes.ticker}>
                <CardContent className={classes.tickerContent}>
                    <Typography
                      variant="body1"
                      component="p"
                      style={{fontSize: "1rem", lineHeight: "17px"}}
                    >
                      MAX {props.max < 0 ? <ArrowDropDownIcon fontSize="medium" style={{color: "rgb(255, 109, 4)", margin: "-3"}}/>
                        :
                          <ArrowDropUpIcon fontSize="medium" style={{color: "rgb(255, 109, 4)", margin: "-3"}}/>
                        }

<span style={{color: "rgb(255, 109, 4)"}}>
  {" "}{props.max ? (Math.abs(props.max * 100)).toFixed(0) + "%" : null}
</span>
                    </Typography>
                </CardContent>
              </Card>
              <Card square className={classes.ticker}>
                <CardContent className={classes.tickerContent}>
                    <Typography
                      variant="body1"
                      component="p"
                      style={{fontSize: "1rem", lineHeight: "17px"}}
                    >
                      LAST WEEK {props.week < 0 ? <ArrowDropDownIcon fontSize="medium" style={{color: "rgb(255, 109, 4)", margin: "-3"}}/>
                        :
                          <ArrowDropUpIcon fontSize="medium" style={{color: "rgb(255, 109, 4)", margin: "-3"}}/>
                        }
<span style={{color: "rgb(255, 109, 4)"}}>
  {" "}{props.week ? (Math.abs(props.week * 100)).toFixed(0) + "%" : null}
</span>
                    </Typography>
                </CardContent>
              </Card>
            </div>
              {NEW[props.cityId] || BETA[props.cityId] ? (
                <Card
                  square
                  className={classes.chip}
                  style={{ color: "#fff", background: "rgb(255, 109, 4)", borderRadius: "3px" }}
                >
                  <CardContent style={{ padding: 0 }}>
                    <Typography
                      variant="body1"
                      component="p"
                      style={{ fontWeight: "bold" }}
                    >
                      {NEW[props.cityId] ? <>NEW</> : <>BETA</>} FEED
                    </Typography>
                  </CardContent>
                </Card>
              ) : null}
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
              {NEW[props.cityId] || BETA[props.cityId] ? (
                <Card square className={classes.chip}>
                  <CardContent style={{ padding: 0 }}>
                    <Typography
                      variant="body1"
                      component="p"
                      style={{ color: "#fff", background: "rgb(255, 109, 4)", borderRadius: "3px" }}
                    >
                      {NEW[props.cityId] ? <>NEW</> : <>BETA</>} FEED
                    </Typography>
                  </CardContent>
                </Card>
              ) : null}
            </CardContent>
          </Hidden>
        </Link>
      </CardActionArea>
    </Card>
  )
}
