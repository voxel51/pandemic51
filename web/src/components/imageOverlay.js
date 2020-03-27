/**
 * Image overlay components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { useState, useEffect, useRef } from "react";
import PropTypes from 'prop-types'
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import CircularProgress from '@material-ui/core/CircularProgress';

export default function ImageOverlay({src, onClose}) {
  const [isLoaded, setLoaded] = useState(false);

  useEffect(() => setLoaded(false), [src]);

  const handleLoad = () => {
    setLoaded(true);
  };

  if (!src) {
    return null;
  }

  const imageStyle = {
    display: isLoaded ? 'block' : 'none',
  };

  return (
    <div className="image-overlay-wrapper">
      <div className="image-overlay">
        <img src={src} onLoad={handleLoad} style={imageStyle}/>
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
        <IconButton aria-label="close" className="close-button" onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </div>
    </div>
  );
}

ImageOverlay.propTypes = {
  src: PropTypes.string,
  onClose: PropTypes.func.isRequired,
};
