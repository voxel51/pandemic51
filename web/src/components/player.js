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
  "chicago": "https://pdi-service.voxel51.com/stream/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "london": "https://pdi-service.voxel51.com/stream/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "https://pdi-service.voxel51.com/stream/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "https://pdi-service.voxel51.com/stream/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "https://pdi-service.voxel51.com/stream/fecnetwork/14191.flv/chunklist_w1339994956.m3u8"
}

export default function Player({city}) {
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    setPlayer(
      <ReactHLS url={cities[city]} width='100%' height='100%'
        videoProps={{muted: true, controls: false, autoPlay: true}}
      />
    );
  }, [city])

  if (!player) {
    return null;
  }

  return (
    <div className="detector">
      {player}
    </div>
  );
}

Player.propTypes = {
  city: PropTypes.string,
}
