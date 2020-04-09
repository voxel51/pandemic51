/**
 * Image overlay components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { useState, useEffect, useRef } from "react"
import PropTypes from "prop-types"
import IconButton from "@material-ui/core/IconButton"
import CloseIcon from "@material-ui/icons/Close"
import ShareIcon from "@material-ui/icons/Share"
import CircularProgress from "@material-ui/core/CircularProgress"
import Modal from "@material-ui/core/Modal"
import Card from "@material-ui/core/Card"
import CardContent from "@material-ui/core/CardContent"
import Typography from "@material-ui/core/Typography"
import Box from "@material-ui/core/Box"
import Button from "@material-ui/core/Button"
import { CopyToClipboard } from "react-copy-to-clipboard"

export default function ImageOverlay({
  src,
  height,
  timestamp,
  clicked,
  onClose,
  onNavigate,
}) {
  console.log({onNavigate})
  const [isLoaded, setLoaded] = useState(false)
  const [isCopied, setCopied] = useState(false)
  const [open, setOpen] = useState(false)
  const text = useRef(null)
  useEffect(() => setLoaded(false), [src])

  const handleOpen = () => {
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
  }

  const handleLoad = () => {
    setLoaded(true)
  }

  if (!src) {
    return null
  }

  const imageStyle = {
    display: isLoaded ? "block" : "none",
  }

  const body = (
    <Card square style={{ maxWidth: "100%", boxShadow: "none" }}>
      <CardContent>
        <Typography
          variant="h3"
          component="h2"
          style={{ marginBottom: "2rem" }}
        >
          Share this snapshot!
        </Typography>
        <Box
          className="share-box"
          display="flex"
          justifyContent="space-between"
          style={{ maxWidth: "100%" }}
        >
          <Typography
            ref={text}
            variant="h5"
            component="p"
            color="textSecondary"
            style={{
              border: "2px",
              lineHeight: "32px",
              marginRight: 8,
              whiteSpace: "nowrap",
            }}
          >
            {isCopied ? "Copied to clipboard!" : window.location.href}
          </Typography>
          <CopyToClipboard
            text={window.location.href}
            onCopy={() => {
              setCopied(true)
              setTimeout(() => setCopied(false), 1000)
            }}
          >
            <Button
              variant="contained"
              style={{ background: "#FF6D04", borderRadius: 0 }}
              square
            >
              <Typography variant="h5" component="p" style={{ color: "#fff" }}>
                Copy
              </Typography>
            </Button>
          </CopyToClipboard>
        </Box>
      </CardContent>
    </Card>
  )

  return (
    <div className="image-overlay-wrapper">
      <div className="image-overlay" style={{ height }}>
        <img src={src} onLoad={handleLoad} style={imageStyle} />
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
        {timestamp ? <div className="image-timestamp">{timestamp}</div> : null}
        {clicked ? (
          <React.Fragment>
            <div className="buttons">
              <IconButton
                aria-label="share"
                className="share-button"
                onClick={handleOpen}
              >
                <ShareIcon />
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
              <IconButton
                aria-label="close"
                className="close-button"
                onClick={onClose}
              >
                <CloseIcon />
              </IconButton>
            </div>
            {onNavigate ? (
              <React.Fragment>
                <a className="frame-nav frame-nav-prev" title="Previous image">&laquo;</a>
                <a className="frame-nav frame-nav-next" title="Next image">&raquo;</a>
              </React.Fragment>
            ) : null}
          </React.Fragment>
        ) : null}
      </div>
    </div>
  )
}

ImageOverlay.propTypes = {
  src: PropTypes.string,
  height: PropTypes.number,
  timestamp: PropTypes.string,
  clicked: PropTypes.bool,
  onClose: PropTypes.func.isRequired,
  onNavigate: PropTypes.func,
}
