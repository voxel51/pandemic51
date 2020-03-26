import React, { useState, useEffect, useRef } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";

const CITIES = {
  "chicago": "http://34.67.136.168/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "london": "http://34.67.136.168/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "http://34.67.136.168/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "http://34.67.136.168/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "http://34.67.136.168/fecnetwork/14191.flv/chunklist_w1339994956.m3u8"
}

const DETECTION_INTERVAL_MS = 100;
const DETECTIONS_TO_SHOW = [
  'person',
];

const modelPromise = cocoSsd.load({base: 'lite_mobilenet_v2'});
modelPromise.then(
  () => console.log('model loaded'),
  (error) => console.log(`unable to load model: ${error.message}`)
);

export default function ClapprPlayer({city}) {
  const [height, setHeight] = useState(0);
  const [width, setWidth] = useState(0);
  const playerRef = useRef(null);
  const canvasRef = useRef(null);

  const createPlayer = () => {
    let player = new Clappr.Player({
      parent: playerRef.current,
      source: CITIES[city],
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
        if (video && !cancelled) {
          const model = await modelPromise;
          if (!cancelled) {
            const predictions = await model.detect(video);
            if (!cancelled) {
              renderPredictions(predictions, video);
            }
          }
        }
      } catch (error) {
        // pass on the error -> the video data is just not available
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
  useEffect(createPlayer, [city]);

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
    const canvasWidth = ctx.canvas.width;
    const canvasHeight = ctx.canvas.height;
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    // Font options.
    const font = "12px sans-serif";
    ctx.font = font;
    ctx.textBaseline = "top";
    const t_template = (from, to) => i => i / from * to;
    const th = t_template(video.videoHeight, canvasHeight);
    const tw = t_template(video.videoWidth, canvasWidth);
    ctx.fillStyle = "#499cef";
    ctx.fillText(`${predictions.length}`, 10, canvasHeight - 18);
    ctx.strokeStyle = "#499cef";
    ctx.lineWidth = 2;
    predictions.forEach(prediction => {
      if (!DETECTIONS_TO_SHOW.includes(prediction.class)) {
        return;
      }
      const x = tw(prediction.bbox[0]);
      const y = th(prediction.bbox[1]);
      const width = tw(prediction.bbox[2]);
      const height = th(prediction.bbox[3]);
      // Throw away any bad detection covering the whole scene or most of it
      if (width*height > 100000) {
        return;
      }
      // Draw the bounding box in the Voxel51 blue.
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
