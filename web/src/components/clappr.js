import React, { useRef, useLayoutEffect, useState } from "react";
import Clappr from 'clappr';
import PropTypes from 'prop-types'
import createReactClass from 'create-react-class';



export default createReactClass({
  propTypes: {
    source: PropTypes.string
  },

  getInitialState() {
    return { height: 0 };
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

  componentDidMount: function() {
    this.change(this.props);
    let node = this.refs.player.parentNode;
    var styles = window.getComputedStyle(node);
    var padding = parseFloat(styles.paddingLeft) + parseFloat(styles.paddingRight);
    const h = (node.clientWidth - padding) * 9/16;
    this.setState({ height: h});
    window.addEventListener("resize", e => {
      var styles = window.getComputedStyle(node);
      var padding = parseFloat(styles.paddingLeft) + parseFloat(styles.paddingRight);
      const h = (node.clientWidth - padding) * 9/16;
      this.setState({ height: h});
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
    return (
      <div ref="player" style={{height: String(this.state.height) + "px"}}></div>
    );
  }
});
