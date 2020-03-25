import React, { useRef, useLayoutEffect, useState } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import createReactClass from 'create-react-class';
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import "@tensorflow/tfjs";

export default createReactClass({
  propTypes: {
    source: PropTypes.string
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
      model.detect(video).then(predictions => {
        this.renderPredictions(predictions, video);
        setTimeout(() => {
          requestAnimationFrame(() => {
            this.detectFrame(video, model);
          });
        }, 1000);
      });
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
      source: props.source,
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
