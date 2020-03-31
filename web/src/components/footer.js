/**
 * Footer components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import {
  faFacebook,
  faGithub,
  faLinkedin,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons"
import SB from "./sb"
import PD from "./pd"

const Footer = props => (
  <>
    <div class="body_part bg-light-primary body_block--right">
      <div class="body_block__title">
        <h2>Unprecedented Impact on Social Behavior</h2>
      </div>
      <div class="body_block__visual">
        <SB />
      </div>
      <div class="body_block__text">
        The spread of the coronavirus has caused policymakers in the U.S. and
        around the globe to implement strict physical distancing orders to slow
        the rate of infection and thus flatten the growth curve.
        <br />
        <br />
        In an effort to bring information and awareness surrounding the impact
        of this pandemic, Voxel51 is using our AI-powered video understanding
        capabilities to gather and analyze video data from public street cams
        around the world. Our team has developed the{" "}
        <b>Physical Distancing Index (PDI)</b> to measure the impact on social
        behavior in public spaces. This measure is non-invasive and does not use
        other data sources like mobile phone signals, which allow only
        approximate location estimates; instead we focus on specific centralized
        locations of interest in each city and literally watch what is
        happening.
        <br />
        <br />
        The data in the graphs speaks for itself: coronavirus and the necessary
        preventative measures across the globe have had an intense impact on
        daily life. All of the above cities have seen a sharp decline in public
        social activity during the month of March.
      </div>
    </div>

    <div class="body_part bg-light-secondary body_block--centerfull">
      <h2 class="body_block__title--left">
        What is the Physical Distancing Index?
      </h2>
      <div class="body_block__text">
        Our <a href="https://voxel51.com/platform"> Platform’s </a> computer
        vision and state-of-the-art deep learning models are able to detect and
        identify pedestrians, vehicles, and other human-centric objects in the
        frames of each live street cam video stream every 15 minutes. . Using
        this raw data, we compute the PDI, an aggregate statistical measure that
        captures the average density of human activity within view of the camera
        over time. Note that PDI is a privacy-preserving measure that does not
        extract any identifying information about the individuals in the video.
      </div>
    </div>

    <div class="body_part bg-light-primary body_block--left">
      <div class="body_block__title">
        <h2>Physical Distancing versus Social Distancing</h2>
      </div>
      <div class="body_block__visual">
        <PD />
      </div>
      <div class="body_block__text" align="left">
        <br />
        We named the Voxel51 Physical Distancing Index (PDI) in response to the{" "}
        <a target="_blank" href="https://www.forbes.com/sites/carolkinseygoman/2020/03/23/dont-let-physical-distancing-become-social-distancing/#157df7f949e6">
          World Health Organization’s recommendation{" "}
        </a>{" "}
        to do so. Physical distancing is intended to reduce the spread of the
        virus between individuals, especially in situations where an individual
        is carrying the virus but does not show symptoms. We wholeheartedly
        believe that it is intensely important to maintain social connections
        during this time of physical separation.
      </div>
    </div>

    <div class="bg-footer-dark body_part bg-dark-primary body_block--center body_block--padtop">
      <h2 class="body_block__title">What’s Next?</h2>
      <div class="body_block__text text-secondary-on-dark">
        As this global pandemic progresses, we will continue to provide frequent
        updates and data analysis to keep you informed. Stay tuned for more!
        Subscribe to keep updated on the PDI and related topics and check out
        the project on Github if you'd like to contribute.
      </div>
      <div class="body_block__hook">
        <ul class="list-inline">
          <li>
            <a
              class="button-primary"
              target="_blank"
              href="https://share.hsforms.com/1HZqZoRqsTneuXFm8pVzR1A2ykyk"
            >
              Subscribe
            </a>
          </li>
          <li>
            <a
              class="button-secondary"
              target="_blank"
              href="https://github.com/voxel51/pandemic51"
            >
              Contribute
            </a>
          </li>
        </ul>
      </div>
    </div>
    <footer class="body_part footer">
      <div class="footer__logo">
        <img src="https://voxel51.com/images/logo/voxel51-logo-horz-color-600dpi.png" />
      </div>

      <div class="footer__address">
        410 N 4th Ave, 3rd Floor
        <br />
        Ann Arbor, MI 48104
      </div>

      <div class="footer__contact">
        <a href="mailto:info@voxel51.com">info@voxel51.com</a>
        <br />
        734-489-1134
      </div>

      <div class="footer__links">
        <div class="footer__links--col1">
          <a href="https://voxel51.com/">Home</a>
          <a href="https://voxel51.com/platform">Platform</a>
          <a href="https://voxel51.com/platform/#pricing">Platform Pricing</a>
          <a href="https://voxel51.com/platform/faq">Platform FAQ</a>
          <a href="https://voxel51.com/annotation">Annotation</a>
        </div>
        <div class="footer__links--col2">
          <a href="https://voxel51.com/usecases">Use Cases</a>
          <a href="https://voxel51.com/ourstory">Our Story</a>
          <a href="https://voxel51.com/careers">Careers</a>
          <a href="https://voxel51.com/press">Press</a>
          <a href="https://blog.voxel51.com/">Blog</a>
        </div>
        <div class="footer__links--col3">
          <a href="https://console.voxel51.com/login">Platform Login</a>
          <a href="https://scoop.voxel51.com/">Scoop Login</a>
          <a href="https://demo.voxel51.com">Scoop Demo</a>
          <a href="https://status.voxel51.com/">System Status</a>
        </div>
      </div>

      <div class="footer__icons">
        <ul class="list-inline">
          <li>
            <a target="_blank" href="https://www.linkedin.com/company/voxel51/">
              <FontAwesomeIcon icon={faLinkedin} />
            </a>
          </li>
          <li>
            <a target="_blank" href="https://github.com/voxel51/">
              <FontAwesomeIcon icon={faGithub} />
            </a>
          </li>
          <li>
            <a target="_blank" href="https://twitter.com/voxel51">
              <FontAwesomeIcon icon={faTwitter} />
            </a>
          </li>
          <li>
            <a target="_blank" href="https://www.facebook.com/voxel51/">
              <FontAwesomeIcon icon={faFacebook} />
            </a>
          </li>
        </ul>
      </div>

      <div class="footer__copyright">
        <ul class="list-inline">
          <li>© 2020 Voxel51 Inc.</li>
          <li>
            <a href="https://voxel51.com/privacy">Privacy Policy</a>
          </li>
          <li>
            <a href="https://voxel51.com/terms">Terms of Service</a>
          </li>
        </ul>
      </div>
    </footer>
  </>
)

export default Footer
