import React, { useState, useEffect, useRef } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";

const DETECTION_INTERVAL_MS = 1000;
const DETECTIONS_TO_SHOW = [
  'person',
];

export default function ClapprPlayer({source}) {
  const [height, setHeight] = useState(0);
  const [width, setWidth] = useState(0);
  const playerRef = useRef(null);
  const canvasRef = useRef(null);
  // only call load() once per instance (todo: call it once ever?)
  const [modelPromise] = useState(() => cocoSsd.load());

  const createPlayer = () => {
    let player = new Clappr.Player({
      parent: playerRef.current,
      source: source,
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
    detectFrame();

    return function cleanup() {
      cancelled = true;
      player.destroy();
    }
  };
  useEffect(createPlayer, [source]);

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
      if (!DETECTIONS_TO_SHOW.includes(prediction.class)) {
        return;
      }
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
  source: PropTypes.string,
}
