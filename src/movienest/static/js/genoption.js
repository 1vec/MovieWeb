function genOption_pie(resource, serieName, optTitle){
  data = []
  for (prop in resource) {
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  var option = {
    title: optTitle,
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c}"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    xAxis: {
      show: false
    },
    yAxis: {
      show: false
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },

    series: [{
      name: serieName,
      label: {
        normal: {
          show: true,
          formatter: '{b} {c}'
        },
      },
      type: 'pie',
      radius: '55%',
      data: data
    }]
  }
  return option
}

function genOption_wordCloud(resource, serieName, optTitle){
  data = []
  for (prop in resource) {
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  var option = {
    title: optTitle,
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c}"
    },
    series: [{
      name: serieName,
      type: 'wordCloud',
      shape: 'circle',
      // maskImage: maskImage,
      left: 'center',
      top: 'center',
      width: '70%',
      height: '80%',
      right: null,
      bottom: null,
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        normal: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          // Color can be a callback function or a color string
          color: function () {
            // Random color
            return 'rgb(' + [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160)
            ].join(',') + ')';
          }
        },
        emphasis: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: data
    }]
  }
  return option
}

function genOption_funnel(resource, serieName, optTitle){
  data = []
  minValue = resource[0][1]
  maxValue = resource[0][1]
  for (prop in resource) {
    value = resource[prop][1]
    minValue = value < minValue ? value : minValue
    minValue = value > minValue ? value : minValue
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  console.log(data)
  var option = {
    title: optTitle,
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c}"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },

    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },
    calculable: true,
    series: [
      {
        name: serieName,
        type: 'funnel',
        left: '20%',
        top: 60,
        //x2: 80,
        bottom: 60,
        width: '70%',
        // height: {totalHeight} - y - y2,
        min: minValue,
        max: maxValue,
        minSize: '55%',
        maxSize: '60%',
        sort: 'descending',
        gap: 1,
        label: {
          normal: {
            show: true,
            position: 'inside',
            formatter: '{b} ({c})'
          },
          emphasis: {
            textStyle: {
              fontSize: 20
            }
          }
        },
        labelLine: {
          normal: {
            length: 10,
            lineStyle: {
              width: 1,
              type: 'solid'
            }
          }
        },
        itemStyle: {
          normal: {
            borderColor: '#fff',
            borderWidth: 1
          }
        },
        data: data
      }]
  }
  return option
}

function genOption_line(resource, optTitle){
  data = []
  xAxis = resource[0]
  data = resource[1]
  legend = []
  series = []
  for (prop in data) {
    legend.push(prop)
    series.push({
      name: prop,
      type: 'line',
      data: data[prop]
    })
  }
  var option = {
    title: optTitle,
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: legend
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },
    xAxis: {
      data: xAxis
    },
    yAxis: {},
    series: series
  }
  return option
}


