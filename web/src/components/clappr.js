import React, { useRef, useLayoutEffect, useState } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import createReactClass from 'create-react-class';
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";

const cities = {
  "chicago": "http://34.67.136.168/fecnetwork/13661.flv/chunklist_w2061640580.m3u8",
  "dublin": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/4054.flv/chunklist.m3u8",
  "london": "http://34.67.136.168/fecnetwork/AbbeyRoadHD1.flv/chunklist_w99014656.m3u8",
  "newjersey": "http://34.67.136.168/fecnetwork/5173.flv/chunklist_w246713699.m3u8",
  "neworleans": "http://34.67.136.168/fecnetwork/4280.flv/chunklist_w2121039669.m3u8",
  "newyork": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv/chunklist.m3u8",
  "prague": "http://34.67.136.168/fecnetwork/14191.flv/chunklist_w1339994956.m3u8"
}

export default createReactClass({
  propTypes: {
    city: PropTypes.string
  },

  getInitialState() {
    return {
      height: 0,
      width: 0
    };
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    let changed = (nextProps.source != this.props.source);
    changed = changed || nextState.height != this.state.height;
    this.props = nextProps;
    this.state = nextState;
    if (changed) {
      this.change(nextProps);
    }
    return changed;
  },

  componentDidMount: async function() {
    this.change(this.props);
    const video = this.refs.player.childNodes[0].childNodes[0].childNodes[2];

    const videoPromise = new Promise((resolve, reject) => {
      video.onloadedmetadata = () => {
        resolve();
      };
    });
    const parentRef = this.refs.player.parentNode.parentNode;
    const update = () => {
      const styles = window.getComputedStyle(parentRef);
      const padding = parseFloat(styles.paddingLeft) + parseFloat(styles.paddingRight);
      const w = parentRef.clientWidth - padding;
      const h = w * 9/16;
      this.setState({
        height: h,
        width: w
      });
    };
    update();
    window.addEventListener("resize", update);
    return;
    const model = await cocoSsd.load();
    videoPromise
      .then(() => {
        this.detectFrame(video, model);
      })
      .catch(error => {
        console.error(error);
      });
  },

  componentWillUnmount: function() {
    this.destroyPlayer();
  },

  destroyPlayer() {
    if (this.player) {
      this.player.destroy();
    }
    this.player = null;
  },

  detectFrame: function(video, model) {
      const next = () => {
        setTimeout(() => {
          requestAnimationFrame(() => {
            this.detectFrame(video, model);
          });
        }, 1000);
      };
      if (this.player) {
        model.detect(video).then(predictions => {
          this.renderPredictions(predictions, video);
          next();
        });
      };
      next();
  },

  renderPredictions: function(predictions, video) {
    const ctx = this.refs.canvas.getContext("2d");
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    // Font options.
    const font = "16px sans-serif";
    ctx.font = font;
    ctx.textBaseline = "top";
    const t_template = (from, to) => i => i / from * to;
    const th = t_template(video.videoHeight, this.state.height);
    const tw = t_template(video.videoWidth, this.state.width);
    predictions.forEach(prediction => {
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
  },

  change: function(props) {
    if (this.player) {
      this.destroyPlayer();
    }
    this.player = new Clappr.Player({
      parent: this.refs.player,
      source: cities[props.city],
      width: '100%',
      height: '100%',
      mute: true,
      autoPlay: true,
      allowUserInteraction: false,
      hideMediaControl: true,
      hideVolumeBar: true,
      chromeless: true,
      hlsjsConfig: {
        enableWorker: true,
        xhrSetup: (xhr) => {
          xhr.setRequestHeader("Origin", "https://eartcam.com");
        }
      }
    });
  },

  render: function() {
    const style = {}
    const toPixels = (str) => String(str) + "px";
    for (let [key, value] of Object.entries(this.state)) {
      style[key] = toPixels(value);
    }
    return (
      <div className="detector">
        <div ref="player"
          style={style}>
      </div>
      <canvas
        className="boxes"
          ref="canvas"
          width={this.state.width}
          height={this.state.height}
        />
      </div>
    );
  }
});
