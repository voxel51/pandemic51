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


const cities = {
  "chicago": "http://34.67.136.168/stream/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "london": "http://34.67.136.168/stream/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "http://34.67.136.168/stream/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "http://34.67.136.168/stream/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "http://34.67.136.168/stream/fecnetwork/14191.flv/chunklist_w1339994956.m3u8"
}

export default function Player({city}) {
  const [height, setHeight] = useState(0);
  const [width, setWidth] = useState(0);
  const playerRef = useRef(null);

  const updateSize = () => {
    const parentRef = playerRef.current.parentNode;
    const styles = window.getComputedStyle(parentRef);
    const padding = parseFloat(styles.paddingLeft) + parseFloat(styles.paddingRight);
    const w = parentRef.clientWidth - padding;
    const h = w * 9/16;
    setWidth(w);
    setHeight(h);
  };
  useEffect(() => {
    updateSize();
    window.addEventListener("resize", updateSize);
    return () => {
      window.removeEventListener("resize", updateSize);
    };
  });

  return (
    <div className="detector" ref={playerRef}>
      <ReactHLS url={cities[city]} width={width} height={height}
      videoProps={{muted: true, controls: false, autoPlay: true}}
      />
    </div>
  );
}

Player.propTypes = {
  city: PropTypes.string,
}
