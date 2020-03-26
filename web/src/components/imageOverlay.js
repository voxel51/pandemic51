import React, { useState, useEffect, useRef } from "react";
import PropTypes from 'prop-types'
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

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
    <div className="image-overlay">
      <img src={src} onLoad={handleLoad} style={imageStyle}/>
      <IconButton aria-label="close" className="close-button" onClick={onClose}>
        <CloseIcon />
      </IconButton>
    </div>
  );
}

ImageOverlay.propTypes = {
  src: PropTypes.string,
  onClose: PropTypes.func.isRequired,
};
