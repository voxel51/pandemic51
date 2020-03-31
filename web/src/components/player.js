/**
 * Live stream components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { useState, useEffect, useRef } from "react";
import PropTypes from 'prop-types'
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";
import ReactHLS from 'react-hls';
import CircularProgress from '@material-ui/core/CircularProgress';

export default function Player({city, height, setHeight, children}) {
  const [url, setUrl] = useState(null);
  const [player, setPlayer] = useState(null);
  const [isLoaded, setLoaded] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    const updateUrl = async () => {
      let res = await fetch(`https://pdi-service.voxel51.com/api/streams/${city}`);
      res = await res.json();
      if (!cancelled) {
        setUrl(res.url);
      }
    };
    setUrl(null);
    setLoaded(false);
    updateUrl();
    return () => {
      cancelled = true;
    };
  }, [city]);

  const onLoad = () => {
    setLoaded(true);
  };

  const handleResize = (video) => {
    if (setHeight) {
      const container = video.parentNode.parentNode;
      setHeight(video.videoHeight * container.clientWidth / video.videoWidth);
    }
  };

  const handleMetadata = (e) => {
    handleResize(e.target);
  };

  useEffect(() => {
    const callback = () => {
      handleResize(wrapperRef.current.querySelector('video'));
    }
    window.addEventListener('resize', callback);
    return () => {
      window.removeEventListener('resize', callback);
    }
  }, [wrapperRef.current]);

  useEffect(() => {
    setPlayer(
      <ReactHLS
        url={url}
        width='100%'
        height='100%'
        videoProps={{
          muted: true,
          controls: false,
          autoPlay: true,
          onLoadedData: onLoad,
          onLoadedMetadata: handleMetadata,
        }}
      />
    );
  }, [url])

  if (!player) {
    return null;
  }
  return (
    <div ref={wrapperRef} className="video-player-wrapper">
      {children}
      <div className="video-player" style={{height}}>
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
        {player}
      </div>
    </div>
  );
}

Player.propTypes = {
  city: PropTypes.string.isRequired,
  height: PropTypes.number,
  setHeight: PropTypes.func,
}
