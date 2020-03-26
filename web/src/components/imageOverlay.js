import React, { useState, useEffect, useRef } from "react";
import PropTypes from 'prop-types'
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

export default function ImageOverlay({src, onClose}) {
  if (!src) {
    return null;
  }
  return (
    <div className="image-overlay">
      <img src={src}/>
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
