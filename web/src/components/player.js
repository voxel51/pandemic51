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

const cities = {
  "chicago": "https://pdi-service.voxel51.com/stream/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "fortlauderdale": "https://pdi-service/voxel51.com/stream/fecnetwork/windjammerHD2.flv/chunklist_w199477428.m3u8",
  "london": "https://pdi-service.voxel51.com/stream/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "https://pdi-service.voxel51.com/stream/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "https://pdi-service.voxel51.com/stream/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "https://pdi-service.voxel51.com/stream/fecnetwork/14191.flv/chunklist_w1339994956.m3u8",
}

export default function Player({city, height, setHeight}) {
  const [player, setPlayer] = useState(null);
  const [isLoaded, setLoaded] = useState(false);
  const wrapperRef = useRef(null);

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
        url={cities[city]}
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
  }, [city])

  if (!player) {
    return null;
  }
  return (
    <div ref={wrapperRef} className="video-player-wrapper">
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
