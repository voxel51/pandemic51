import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

const Footer = (props) => (
<footer class="body_part footer">

          <div class="footer__logo">
            <img src="https://voxel51.com/images/logo/voxel51-logo-horz-color-600dpi.png"/>
          </div>

          <div class="footer__address">
            410 N 4th Ave, 3rd Floor
            <br/>
            Ann Arbor, MI 48104
          </div>

          <div class="footer__contact">
            <a href="mailto:info@voxel51.com">info@voxel51.com</a>
            <br/>
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
                <a href="https://www.linkedin.com/company/voxel51/">
                  <i class="fa fa-linkedin"></i>
                </a>
              </li>
              <li>
                <a href="https://github.com/voxel51/">
                  <i class="fa fa-github"></i>
                </a>
              </li>
              <li>
                <a href="https://twitter.com/voxel51">
                  <i class="fa fa-twitter"></i>
                </a>
              </li>
              <li>
                <a href="https://www.facebook.com/voxel51/">
                  <i class="fa fa-facebook"></i>
                </a>
              </li>
            </ul>
          </div>

          <div class="footer__copyright">
            <ul class="list-inline">
              <li>
                © 2020 Voxel51 Inc.
              </li>
              <li>
                <a href="https://voxel51.com/privacy">Privacy Policy</a>
              </li>
              <li>
                <a href="https://voxel51.com/terms">Terms of Service</a>
              </li>
            </ul>
          </div>

      </footer>
)


export default Footer
