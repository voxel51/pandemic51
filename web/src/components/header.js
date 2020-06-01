/**
 * Header components.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import { Link } from "gatsby"
import PropTypes from "prop-types"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons"
import React from "react"

class Header extends React.Component {
  constructor() {
    super()
    this.onClick = this.handleClick.bind(this)
    this.state = {
      nav: false,
      mobile: null,
      rendered: false,
    }
  }

  handleClick(event) {
    event.preventDefault()
    this.setState({ nav: !this.state.nav })
  }

  componentDidMount() {
    if (typeof window !== `undefined`) {
      const computed = window
        .getComputedStyle(this.refs.mobile)
        .getPropertyValue("display")
      if (computed === "block" && this.state.mobile === null) {
        this.setState({ mobile: true, rendered: true })
      } else {
        this.setState({ rendered: true })
      }
    }
  }

  render() {
    let menu = this.state.mobile === null ? "flex" : "none"
    menu = this.state.mobile && this.state.nav ? "block" : menu
    const off = this.state.mobile && this.state.nav ? "block" : "none"
    const on = this.state.mobile && !this.state.nav ? "block" : "none"
    let obj = {}
    let objM = {}
    if (this.state.rendered) {
      obj.display = on
      objM.display = menu
    }
    const site = "https://voxel51.com"
    return (
      <>
        <nav id="nav__main" class="nav__main stay_at_top">
          <div class="nav__main__logo">
            <a href={site}>
              <img src="https://voxel51.com/images/logo/voxel51-logo-horz-color-600dpi.png" />
            </a>
          </div>

          <div id="nav__main__mobilebutton--on" style={obj} ref="mobile">
            <a href="#" onClick={this.onClick}>
              <FontAwesomeIcon icon={faBars} />
            </a>
          </div>

          <div id="nav__main__mobilebutton--off" style={{ display: off }}>
            <a href="#" onClick={this.onClick}>
              <FontAwesomeIcon icon={faTimes} />
            </a>
          </div>

          <div id="nav__main__items" style={objM}>
            <div class="nav__item nav__dropdown">
              <span class="nav__dropdown__trigger">Products</span>
              <div class="nav__item nav__dropdown__menu has-arrows">
                <div class="arrow-up--light-primary arrow-left20"></div>
                <ul>
                  <li>
                    <a href={`${site}/overview`}>Overview</a>
                  </li>
                  <li class="nav__category">Tools</li>
                  <li class="nav__category--item">
                    <a href={`${site}/fiftyone`}>FiftyOne</a>
                  </li>
                  <li class="nav__category--item">
                    <a href={`${site}/platform`}>Deployment</a>
                  </li>
                  <li class="nav__category--item">
                    <a href={`${site}/senses`}>Senses</a>
                  </li>
                  <li class="nav__category">Applications</li>
                  <li class="nav__category--item">
                    <a href="/">PDI</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="nav__item nav__dropdown">
              <span class="nav__dropdown__trigger">Solutions</span>
              <div class="nav__item nav__dropdown__menu has-arrows">
                <div class="arrow-up--light-primary arrow-left20"></div>
                <ul>
                  <li>
                    <a href={`${site}/lifecycle`}>ML Lifecycle</a>
                  </li>
                  <li class="nav__category">Use Cases</li>
                  <li class="nav__category--item">
                    <a href={`${site}/usecases/automotive`}>Automotive</a>
                  </li>
                  <li class="nav__category--item">
                    <a href={`${site}/usecases/research`}>Research</a>
                  </li>
                  <li class="nav__category--item">
                    <a href={`${site}/usecases/advertising`}>Advertising</a>
                  </li>
                  <li class="nav__category--item">
                    <a href={`${site}/usecases/other`}>Other Industries</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="nav__item nav__dropdown">
              <span class="nav__dropdown__trigger">About Us</span>
              <div class="nav__item nav__dropdown__menu has-arrows">
                <div class="arrow-up--light-primary arrow-left20"></div>
                <ul>
                  <li>
                    <a href={`${site}/ourstory`}>Our Story</a>
                  </li>
                  <li>
                    <a href={`${site}/press`}>Press &amp; News</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="nav__item">
              <a href="https://blog.voxel51.com/">Blog</a>
            </div>
            <div class="nav__spacer"></div>
            <div class="nav__item nav__item--brand">
              <a target="_blank" href="https://meetings.hubspot.com/michael908">
                Schedule Demo
              </a>
            </div>
            <div class="nav__divider">|</div>
            <div class="nav__item nav__dropdown">
              <span class="nav__dropdown__trigger">Login</span>
              <div class="nav__item nav__dropdown__menu has-arrows">
                <div class="arrow-up--light-primary arrow-left20"></div>
                <ul>
                  <li>
                    <a href="https://console.voxel51.com/login">
                      Platform Console
                    </a>
                  </li>
                  <li>
                    <a href="https://scoop.voxel51.com/">Scoop</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </nav>
        <div class="bg-header-dark-fancy2 body_part bg-dark-primary body_block--centerfull force-pad-y3">
          <h2 class="body_block__title">
            Measuring the Social Impact of the <br />
            Coronavirus Pandemic
          </h2>
          <div class="body_block__text" align="center">
            Voxel51 is tracking the impact of the coronavirus global pandemic on
            social behavior, using a metric we developed called the{" "}
            <b>Voxel51 Physical Distancing Index (PDI)</b>. The PDI helps people
            understand how the coronavirus is changing human activity in
            real-time around the world. Using our cutting-edge computer vision
            models and live video streams from some of the most visited streets
            in the world, the PDI captures the average amount of human activity
            and social distancing behaviors in major cities over time.
          </div>
        </div>
      </>
    )
  }
}

export default Header
