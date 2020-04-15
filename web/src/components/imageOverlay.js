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
import ArrowBackIosIcon from "@material-ui/icons/ArrowBackIos"
import ArrowForwardIosIcon from "@material-ui/icons/ArrowForwardIos"
import { HotKeys } from "react-hotkeys"
const keyMap = {
  NEXT: "right",
  PREV: "left",
}

export default function ImageOverlay({
  src,
  height,
  setHeight,
  timestamp,
  clicked,
  onClose,
  onNavigate,
}) {
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

  const handleLoad = e => {
    setLoaded(true)
    if (setHeight) {
      const img = e.target
      const container = img.parentNode.parentNode
      setHeight((img.naturalHeight * container.clientWidth) / img.naturalWidth)
    }
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
  const shortcutHandlers = {
    PREV: () => onNavigate(-1),
    NEXT: () => onNavigate(1),
  }

  return (
    <div className="image-overlay-wrapper">
      <div className="image-overlay" style={{ height }}>
        <img src={src} onLoad={handleLoad} style={imageStyle} />
        <div className="image-overlay-nav">
          {onNavigate && clicked ? (
            <IconButton
              aria-label="previous"
              className="image-overlay-back"
              onClick={() => onNavigate(-1)}
            >
              <ArrowBackIosIcon />
            </IconButton>
          ) : null}
          <div
            className="image-overlay-timestamp"
            style={
              !clicked
                ? { width: "100%", margin: "1rem auto", textAlign: "center" }
                : {}
            }
          >
            {timestamp ? timestamp.toUpperCase() : null}

            {clicked ? (
              <CloseIcon
                aria-label="close"
                className="close-button"
                onClick={onClose}
              />
            ) : null}
          </div>
          {onNavigate && clicked ? (
            <>
              <IconButton
                aria-label="next"
                className="image-overlay-forward"
                onClick={() => onNavigate(1)}
              >
                <ArrowForwardIosIcon />
              </IconButton>
              <IconButton
                aria-label="share"
                className="share-button"
                onClick={handleOpen}
              >
                <ShareIcon />
              </IconButton>
            </>
          ) : null}
        </div>
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
        {clicked ? (
          <React.Fragment>
            <div className="buttons">
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
          </React.Fragment>
        ) : null}
      </div>
    </div>
  )
}

ImageOverlay.propTypes = {
  src: PropTypes.string,
  height: PropTypes.number,
  setHeight: PropTypes.func,
  timestamp: PropTypes.string,
  clicked: PropTypes.bool,
  onClose: PropTypes.func.isRequired,
  onNavigate: PropTypes.func,
}
