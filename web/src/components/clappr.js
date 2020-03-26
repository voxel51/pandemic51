import React, { useState, useEffect, useRef } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";

const cities = {
  "chicago": "http://34.67.136.168/stream/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "london": "http://34.67.136.168/stream/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "http://34.67.136.168/stream/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "http://34.67.136.168/stream/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "http://34.67.136.168/stream/fecnetwork/14191.flv/chunklist_w1339994956.m3u8"
}

const DETECTION_INTERVAL_MS = 1000;

export default function ClapprPlayer({city}) {
  const [height, setHeight] = useState(0);
  const [width, setWidth] = useState(0);
  const playerRef = useRef(null);
  // only call load() once per instance (todo: call it once ever?)

  const createPlayer = () => {
    let player = new Clappr.Player({
      parent: playerRef.current,
      source: cities[city],
      width: '100%',
      height: '100%',
      mute: true,
      autoPlay: true,
      allowUserInteraction: false,
      hideMediaControl: true,
      hideVolumeBar: true,
      chromeless: true,
      hlsjsConfig: {
        enableWorker: true
      }
    });


    return function cleanup() {
      player.destroy();
    }
  };
  useEffect(createPlayer, [city, width, height]);

  const updateSize = () => {
    const parentRef = playerRef.current.parentNode.parentNode;
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
    <div className="detector">
      <div ref={playerRef}
        style={{width, height}}>
      </div>
    </div>
  );
}

ClapprPlayer.propTypes = {
  city: PropTypes.string,
}
