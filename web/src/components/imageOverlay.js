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
import CircularProgress from "@material-ui/core/CircularProgress"

export default function ImageOverlay({ src, height, onClose }) {
  const [isLoaded, setLoaded] = useState(false)

  useEffect(() => setLoaded(false), [src])

  const handleLoad = () => {
    setLoaded(true)
  }

  if (!src) {
    return null
  }

  const imageStyle = {
    display: isLoaded ? "block" : "none",
  }

  return (
    <div className="image-overlay-wrapper">
      <div className="image-overlay" style={{ height }}>
        <img src={src} onLoad={handleLoad} style={imageStyle} />
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
      </div>
    </div>
  )
}

ImageOverlay.propTypes = {
  src: PropTypes.string,
  height: PropTypes.number,
  onClose: PropTypes.func.isRequired,
}
