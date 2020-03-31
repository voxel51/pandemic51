import React from "react"
import { makeStyles } from "@material-ui/core/styles"
import Modal from "@material-ui/core/Modal"
import HelpIcon from "@material-ui/icons/Help"
import IconButton from "@material-ui/core/IconButton"
import Card from "@material-ui/core/Card"
import CardContent from "@material-ui/core/CardContent"
import Typography from "@material-ui/core/Typography"
import Hidden from "@material-ui/core/Hidden"

export default function SimpleModal() {
  const [open, setOpen] = React.useState(false)

  const handleOpen = () => {
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
  }

  const body = (
    <Card square style={{ width: 400, boxShadow: "none" }}>
      <CardContent>
        <Typography
          variant="h3"
          component="h2"
          style={{ marginBottom: "2rem" }}
        >
          How to use the graph
        </Typography>
        <Typography variant="h5" component="p" color="textSecondary">
          <Hidden smDown>
            Click on live video streams from some of the world’s most visited
            streets to see how different cities react to physical distancing.
            Touch the graph to view a day-by-day timeline of the average
            daily number of people on the street (Voxel51’s PDI metric) and
            social behaviors over time.
          </Hidden>
          <Hidden mdUp>
            Click on live video streams from some of the world’s most visited
            streets to see how different cities react to physical distancing.
            Click on the graph to view a day-by-day timeline of the average
            daily number of people on the street (Voxel51’s PDI metric) and
            social behaviors over time. An image of our detections from the time will overlay the video stream.
          </Hidden>
        </Typography>
        <SimpleModal />
      </CardContent>
    </Card>
  )

  return (
    <div>
      <IconButton
        type="button"
        onClick={handleOpen}
        style={{ position: "absolute", top: 0, right: 0 }}
      >
        <HelpIcon />
      </IconButton>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="graph help"
        aria-describedby="graph help"
        style={{
          border: "none",
          margin: "auto",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {body}
      </Modal>
    </div>
  )
}
