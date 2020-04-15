/**
 * Data manipulation.
 *
 * Copyright 2020, Voxel51, Inc.
 * voxel51.com
 */

/**
 * Add time-based data from one series to another. Each series must be an array
 * of objects with a "time" key. In the resulting series, the first array's
 * "time" keys are used, and data from newSeries is copied from the closest
 * earlier time point, or the closest later time point if no earlier time
 * exists.
 * @param {Array} series Original series
 * @param {Array} series Series with new data
 * @return {Array}
 */
export function addDataToSeries(series, newSeries) {
  const compareTime = (p1, p2) => p1.time - p2.time
  series = series.slice().sort(compareTime)
  newSeries = newSeries.slice().sort(compareTime)
  let out = []
  let newIndex = 0
  for (let point of series) {
    while (
      newSeries[newIndex + 1] &&
      newSeries[newIndex + 1].time < point.time
    ) {
      newIndex++
    }
    out.push({
      ...newSeries[newIndex],
      ...point, // will overwrite time with value from original series
    })
  }
  return out
}
