import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

const Header = (props) => (
<nav id="nav__main" class="nav__main stay_at_top">
      <div class="nav__main__logo">
        <a href="https://voxel51.com">
          <img src="https://voxel51.com/images/logo/voxel51-logo-horz-color-600dpi.png"/>
        </a>
      </div>

      <div id="nav__main__mobilebutton--on">
        <a href="javascript:void(0);" onclick="navMobileButton()">
          <i class="fa fa-bars"></i>
        </a>
      </div>

      <div id="nav__main__mobilebutton--off">
        <a href="javascript:void(0);" onclick="navMobileButton()">
          <i class="fa fa-times"></i>
        </a>
      </div>

      <div id="nav__main__items">
        <div class="nav__item">
          <a href="https://voxel51.com/platform">Platform</a>
        </div>
        <div class="nav__item">
          <a href="https://voxel51.com/annotation">Annotation</a>
        </div>
        <div class="nav__item">
          <a href="https://voxel51.com/usecases">Use Cases</a>
        </div>
        <div class="nav__item nav__dropdown">
          <span class="nav__dropdown__trigger">About Us</span>
          <div class="nav__item nav__dropdown__menu has-arrows">
            <div class="arrow-up--light-primary arrow-left20"></div>
            <ul>
              <li><a href="https://voxel51.com/ourstory">Our Story</a>
            </li><li><a href="https://voxel51.com/press">Press &amp; News</a>
            </li></ul>
          </div>
        </div>
        <div class="nav__item">
          <a href="https://voxel51.com/careers">Careers</a>
        </div>
        <div class="nav__item">
          <a href="https://blog.voxel51.com/">Blog</a>
        </div>
        <div class="nav__spacer">
        </div>
        <div class="nav__item nav__item--brand">
          <a target="_blank" href="https://meetings.hubspot.com/michael908">Schedule Demo</a>
        </div>
        <div class="nav__divider">
          |
        </div>
        <div class="nav__item nav__dropdown">
          <span class="nav__dropdown__trigger">Login</span>
          <div class="nav__item nav__dropdown__menu has-arrows">
            <div class="arrow-up--light-primary arrow-left20"></div>
            <ul>
              <li><a href="https://console.voxel51.com/login">Platform Console</a>
              </li><li><a href="https://scoop.voxel51.com/login">Scoop</a>
            </li></ul>
          </div>
        </div>

      </div>
    </nav>
)


export default Header
