/**
 * Middle components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React from "react"
import SB from "./sb"

const Middle = () => {
  return (
    <>
      <div class="body_part bg-light-secondary body_block--right">
        <div class="body_block__title">
          <h2>Unprecedented Impact on Social Behavior</h2>
        </div>
        <div class="body_block__visual">
          <SB />
        </div>
        <div class="body_block__text">
          The spread of the coronavirus has caused policymakers in the U.S. and
          around the globe to implement strict physical distancing orders to
          slow the rate of infection and thus flatten the growth curve.
          <br />
          <br />
          In an effort to bring information and awareness surrounding the impact
          of this pandemic, Voxel51 is using our AI-powered video understanding
          capabilities to gather and analyze video data from public street cams
          around the world. Our team has developed the{" "}
          <b>Physical Distancing Index (PDI)</b> to measure the impact on social
          behavior in public spaces. This measure is non-invasive and does not
          use other data sources like mobile phone signals, which allow only
          approximate location estimates; instead we focus on specific
          centralized locations of interest in each city and literally watch
          what is happening.
          <br />
          <br />
          The data in the graphs speaks for itself: coronavirus and the
          necessary preventative measures across the globe have had an intense
          impact on daily life. All of the above cities have seen a sharp
          decline in public social activity during the month of March.
        </div>
      </div>

      <div class="body_part bg-light-primary body_block--centerfull">
        <h2 class="body_block__title--left">
          What is the Physical Distancing Index?
        </h2>
        <div class="body_block__text">
          Our <a href="https://voxel51.com/platform"> Platform’s </a> computer
          vision and state-of-the-art deep learning models are able to detect
          and identify pedestrians, vehicles, and other human-centric objects in
          the frames of each live street cam video stream in real-time. Using
          images sampled from each video stream every 15 minutes, we compute the
          Physical Distancing Index or PDI, an aggregate statistical measure
          that captures the average density of human activity within view of the
          camera over time. Outputs of the detections, or positive hits, in the
          video streams are represented in the data points on the graph above.
          Note that PDI is a privacy-preserving measure that does not extract
          any identifying information about the individuals in the video.
        </div>
      </div>
    </>
  )
}

export default Middle
