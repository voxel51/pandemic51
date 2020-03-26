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
  const canvasRef = useRef(null);
  // only call load() once per instance (todo: call it once ever?)
  const [modelPromise] = useState(() => cocoSsd.load());

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

    const video = playerRef.current.querySelector('video');
    const videoPromise = new Promise((resolve, reject) => {
      video.onloadeddata = () => resolve(video);
      video.onerror = reject;
    });
    // used to clean up when this component unmounts
    let cancelled = false;

    const detectFrame = async () => {
      if (cancelled) {
        return;
      }
      try {
        const video = await videoPromise;
        if (video) {
          const model = await modelPromise;
          const predictions = await model.detect(video);
          renderPredictions(predictions, video);
        }
      } finally {
        setTimeout(() => {
          requestAnimationFrame(detectFrame);
        }, DETECTION_INTERVAL_MS);
      };
    };
    // detectFrame();

    return function cleanup() {
      cancelled = true;
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

  const renderPredictions = (predictions, video) => {
    const ctx = canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    // Font options.
    const font = "16px sans-serif";
    ctx.font = font;
    ctx.textBaseline = "top";
    const t_template = (from, to) => i => i / from * to;
    const th = t_template(video.videoHeight, height);
    const tw = t_template(video.videoWidth, width);
    predictions.forEach(prediction => {
      console.log(prediction);
      if (prediction.class !== 'person') return;
      const x = tw(prediction.bbox[0]);
      const y = th(prediction.bbox[1]);
      const width = tw(prediction.bbox[2]);
      const height = th(prediction.bbox[3]);
      // Draw the bounding box.
      ctx.strokeStyle = "#00FFFF";
      ctx.lineWidth = 1;
      ctx.strokeRect(x, y, width, height);
    });
  };

  return (
    <div className="detector">
      <div ref={playerRef}
        style={{width, height}}>
      </div>
      <canvas
        ref={canvasRef}
        className="boxes"
        width={width}
        height={height}
      />
    </div>
  );
}

ClapprPlayer.propTypes = {
  city: PropTypes.string,
}
