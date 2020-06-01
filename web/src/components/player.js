/**
 * Live stream components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React, { useState, useEffect, useRef } from "react"
import PropTypes from "prop-types"
import "@tensorflow/tfjs"
import ReactHLS from "react-hls"
import CircularProgress from "@material-ui/core/CircularProgress"
import YouTube from "react-youtube"

const IPCAMS = ["detroit", "annarbor", "ypsilanti"]
const YTCAMS = ["cadiz", "fortworth"]

export default function Player({ city, height, setHeight, children }) {
  const [url, setUrl] = useState(null)
  const [player, setPlayer] = useState(null)
  const [isLoaded, setLoaded] = useState(false)
  const wrapperRef = useRef(null)

  const isIP = c => IPCAMS.indexOf(c) >= 0
  const isYT = c => YTCAMS.indexOf(c) >= 0

  useEffect(() => {
    let cancelled = false
    const updateUrl = async () => {
      let res = await fetch(
        `https://pdi-service.voxel51.com/api/streams/${city}`
      )
      res = await res.json()
      if (!cancelled) {
        setUrl(res.url)
        if (city === "ypsilanti") setTimeout(updateUrl, 60000)
      }
    }
    setUrl(null)
    setLoaded(isYT(city) ? true : false)
    updateUrl()
    return () => {
      cancelled = true
    }
  }, [city])

  const onLoad = () => {
    const callback = () => {
      const tag = isIP(city) ? "img" : "video"
      handleResize(wrapperRef.current.querySelector(tag))
    }
    setLoaded(true)
  }

  const handleResize = v => {
    if (isYT(city)) return
    if (setHeight) {
      const container = v.parentNode.parentNode
      const [h, w] = isIP(city)
        ? [v.naturalHeight, v.naturalWidth]
        : [v.videoHeight, v.videoWidth]
      setHeight((h * container.clientWidth) / w)
    }
  }

  const handleMetadata = e => {
    handleResize(e.target)
  }

  const handleClick = e => {
    e.target.play()
  }

  useEffect(() => {
    const callback = () => {
      let tag = isIP(city) ? "img" : "video"
      tag = isYT(city) ? "iframe" : tag
      handleResize(wrapperRef.current.querySelector(tag))
    }
    window.addEventListener("resize", callback)
    return () => {
      window.removeEventListener("resize", callback)
    }
  }, [wrapperRef.current])

  useEffect(() => {
    if (url && url.includes("youtube")) {
      setPlayer(
        <div class="player-area">
          <iframe
            id="ytplayer"
            type="text/html"
            width="100%"
            height="100%"
            src={url}
            frameborder="0"
          ></iframe>
        </div>
      )
      return
    }
    const videoProps = {
      muted: true,
      controls: false,
      autoPlay: true,
      playsInline: true,
      onLoadedData: onLoad,
      onLoadedMetadata: handleMetadata,
      onClick: handleClick,
    }
    if (isIP(city)) {
      setPlayer(
        <div class="player-area">
          <img onLoad={onLoad} src={url} width="100%" height="100%" />
        </div>
      )
    } else if (window.MediaSource) {
      setPlayer(
        <ReactHLS
          url={url}
          width="100%"
          height="100%"
          videoProps={videoProps}
        />
      )
    } else {
      // likely iOS: https://github.com/video-dev/hls.js/issues/2262
      setPlayer(
        <div class="player-area">
          <video
            onLoad={onLoad}
            src={url}
            width="100%"
            height="100%"
            {...videoProps}
          />
        </div>
      )
    }
  }, [url])

  if (!player) {
    return null
  }
  return (
    <div
      ref={wrapperRef}
      className="video-player-wrapper"
      style={{ height: city === "fortworth" ? "100%" : 0 }}
    >
      {children}
      <div className="video-player" style={{ height }}>
        {isLoaded ? null : <CircularProgress className="loading-icon" />}
        {player}
      </div>
    </div>
  )
}

Player.propTypes = {
  city: PropTypes.string.isRequired,
  height: PropTypes.number,
  setHeight: PropTypes.func,
}
