import React from "react"
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import SEO from "../components/seo"
import Grid from '@material-ui/core/Grid';
import Img from 'gatsby-image';
import { useStaticQuery, graphql } from "gatsby"
import Paper from '@material-ui/core/Paper';
import {Divider} from '@material-ui/core';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) =>
  createStyles({
    root: {
      maxWidth: "400px",
      flexGrow: 1,
      margin: "auto"
    },
    paper: {
      padding: theme.spacing(2),
      textAlign: 'center',
      color: theme.palette.text.secondary,
    },
    divide: {
      margin: "1rem 0"
    }
  }),
);

const NotFoundPage = () => {
  const data = useStaticQuery(graphql`
    query {
      site {
        siteMetadata {
          title
        }
      }
      file(relativePath: { eq: "logo.png" }) {
        childImageSharp {
          fluid {
            ...GatsbyImageSharpFluid
          }
        }
      }
    }
  `);

  const classes = useStyles();

  return (
  <Grid className={classes.root} container spacing={8} justify="center" alignItems="center">
    <Grid item xs={12}>
          <Paper className={classes.paper} square>
            <Img className="logo" fluid={data.file.childImageSharp.fluid} alt=""/>
            <Divider className={classes.divide}/>
            <Typography variant="h5" component="h2">
              404: Not found
          </Typography>
          </Paper>

      <SEO title="404: Not found" />
    </Grid>
  </Grid>
  )
}

export default NotFoundPage
