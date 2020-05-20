/**
 * Site index.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */
import React from "react"
import { Link } from "gatsby"

import Layout from "../components/layout"
import SEO from "../components/seo"

const IndexPage = () => (
  <>
    <SEO />
    <Layout city="newyork" />
  </>
)

export default IndexPage
